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

MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'mainapp', 'vosk-model-small-en-us-0.15')
)
_model = None

def _get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError('Vosk model not found. Download and place in: ' + MODEL_PATH)
        _model = Model(MODEL_PATH)
    return _model


def transcribe_view(request):
    return render(request, 'transcription/transcribe.html')


@csrf_exempt
def _transcribe_wav_path(path):
    with sf.SoundFile(path) as f:
        rec = KaldiRecognizer(_get_model(), f.samplerate)
        parts = []
        # Larger chunks reduce Python overhead without changing recognition logic.
        while True:
            data = f.read(16000, dtype='int16')
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


def offline_transcribe(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
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
            raw_text = _transcribe_wav_path(input_path)
            elapsed = time.time() - start_time
            last = {
                'latency': elapsed,
                'timestamp': timezone.now().isoformat(),
            }
            request.session['last_transcribe_metrics'] = last
            return JsonResponse({'transcript': raw_text, 'latency': elapsed})
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

