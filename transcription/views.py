import os

import soundfile as sf
from django.http import JsonResponse
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
def offline_transcribe(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        with sf.SoundFile(audio_file) as f:
            rec = KaldiRecognizer(_get_model(), f.samplerate)
            transcript = ''
            while True:
                data = f.read(4000, dtype='int16')
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    res = rec.Result()
                    transcript += res
            transcript += rec.FinalResult()
        return JsonResponse({'transcript': transcript})
    return JsonResponse({'error': 'Invalid request'}, status=400)

