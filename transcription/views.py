import json
import os
import subprocess
import time
import tempfile

import soundfile as sf
import numpy as np
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from vosk import Model, KaldiRecognizer
from .models import Transcript, TranscriptionSession
try:
    import torch
    import torchaudio
    from transformers import AutoProcessor, AutoModelForCTC
except ImportError:  # Optional deps for Swahili wav2vec2.
    torch = None
    torchaudio = None
    AutoProcessor = None
    AutoModelForCTC = None

MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'mainapp', 'vosk-model-small-en-us-0.15')
)
_model = None
SWAHILI_MODEL_ID = 'RareElf/swahili-wav2vec2-asr'
_sw_processor = None
_sw_model = None

def _get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError('Vosk model not found. Download and place in: ' + MODEL_PATH)
        _model = Model(MODEL_PATH)
    return _model


def _get_swahili_model():
    global _sw_processor, _sw_model
    if _sw_processor is None or _sw_model is None:
        if AutoProcessor is None or AutoModelForCTC is None or torch is None:
            raise RuntimeError('Swahili model dependencies missing. Install torch, torchaudio, transformers.')
        _sw_processor = AutoProcessor.from_pretrained(SWAHILI_MODEL_ID)
        _sw_model = AutoModelForCTC.from_pretrained(SWAHILI_MODEL_ID)
        _sw_model.eval()
    return _sw_processor, _sw_model


def transcribe_view(request):
    return render(request, 'transcription/transcribe.html')


@csrf_exempt
def _transcribe_wav_path(path):
    with sf.SoundFile(path) as f:
        rec = KaldiRecognizer(_get_model(), f.samplerate)
        parts = []
        while True:
            data = f.read(4000, dtype='int16')
            if data.size == 0:
                break
            if data.ndim > 1:
                data = np.mean(data, axis=1).astype('int16')
            if rec.AcceptWaveform(data.tobytes()):
                res = rec.Result()
                try:
                    parts.append(json.loads(res).get('text', '').strip())
                except json.JSONDecodeError:
                    parts.append(res.strip())
        final_res = rec.FinalResult()
        try:
            parts.append(json.loads(final_res).get('text', '').strip())
        except json.JSONDecodeError:
            parts.append(final_res.strip())
    return ' '.join(p for p in parts if p).strip()


def _transcribe_swahili_wav2vec2(path):
    if torchaudio is None or torch is None:
        raise RuntimeError('Swahili model dependencies missing. Install torch, torchaudio, transformers.')
    processor, model = _get_swahili_model()
    waveform, sample_rate = torchaudio.load(path)
    if waveform.ndim > 1:
        waveform = waveform.mean(dim=0, keepdim=True)
    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(sample_rate, 16000)
        waveform = resampler(waveform)
    with torch.no_grad():
        inputs = processor(waveform.squeeze(0), sampling_rate=16000, return_tensors='pt', padding=True)
        logits = model(**inputs).logits
        pred_ids = torch.argmax(logits, dim=-1)
        text = processor.batch_decode(pred_ids)[0]
    return text.strip()

def offline_transcribe(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        model_choice = request.POST.get('asr_model', 'en_vosk')
        suffix = os.path.splitext(audio_file.name)[1].lower()
        temp_in = None
        temp_wav = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix or '.input') as tmp:
                for chunk in audio_file.chunks():
                    tmp.write(chunk)
                temp_in = tmp.name

            if suffix != '.wav':
                temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
                ffmpeg_cmd = ['ffmpeg', '-y', '-i', temp_in, '-ac', '1', '-ar', '16000', temp_wav]
                try:
                    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except FileNotFoundError:
                    return JsonResponse({'error': 'FFmpeg not found. Install ffmpeg or upload WAV files.'}, status=400)
                except subprocess.CalledProcessError:
                    return JsonResponse({'error': 'FFmpeg failed to convert audio.'}, status=400)
                input_path = temp_wav
            else:
                input_path = temp_in

            start_time = time.time()
            if model_choice == 'sw_wav2vec2':
                raw_text = _transcribe_swahili_wav2vec2(input_path)
                language = 'sw'
            else:
                raw_text = _transcribe_wav_path(input_path)
                language = 'en'
            elapsed = time.time() - start_time

            # Get audio duration
            duration = None
            if os.path.exists(input_path):
                try:
                    with sf.SoundFile(input_path) as f:
                        duration = len(f) / float(f.samplerate)
                except:
                    pass

            # Save transcript to database if user is authenticated
            transcript = None
            if request.user.is_authenticated:
                transcript = Transcript.objects.create(
                    user=request.user,
                    title=f"Transcription {timezone.now().strftime('%Y-%m-%d %H:%M')}",
                    original_audio=audio_file,
                    transcript_text=raw_text,
                    language=language,
                    duration=duration,
                    processing_time=elapsed
                )

            last = {
                'latency': elapsed,
                'timestamp': timezone.now().isoformat(),
            }
            request.session['last_transcribe_metrics'] = last
            return JsonResponse({
                'transcript': raw_text,
                'latency': elapsed,
                'transcript_id': transcript.id if transcript else None,
            })
        except Exception as exc:
            return JsonResponse({'error': f'Audio processing failed: {exc}'}, status=400)
        finally:
            if temp_in and os.path.exists(temp_in):
                try:
                    os.remove(temp_in)
                except OSError:
                    pass
            if temp_wav and os.path.exists(temp_wav):
                try:
                    os.remove(temp_wav)
                except OSError:
                    pass
    return JsonResponse({'error': 'Invalid request'}, status=400)

