import time

import soundfile as sf

from django.shortcuts import render

from transcription.views import _transcribe_wav_path

from accounts.models import Profile


def dashboard_view(request):
    profile = None
    if request.user.is_authenticated:
        profile, _created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'core/dashboard.html', {'profile': profile})


def performance_view(request):
    result = None
    last_metrics = request.session.get('last_transcribe_metrics')
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        reference = request.POST.get('reference', '').strip()
        if reference:
            start = time.time()
            with sf.SoundFile(audio_file) as f:
                duration = len(f) / float(f.samplerate)
            audio_file.seek(0)
            transcript = _transcribe_wav_path(audio_file)
            elapsed = time.time() - start
            wer = _wer(reference, transcript)
            cer = _cer(reference, transcript)
            rtf = elapsed / duration if duration else 0
            result = {
                'wer': wer,
                'cer': cer,
                'latency': elapsed,
                'rtf': rtf,
                'transcript': transcript,
            }
        else:
            result = {'error': 'Reference text is required.'}
    return render(request, 'core/performance.html', {
        'result': result,
        'last_metrics': last_metrics,
    })


def _levenshtein(a, b):
    if a == b:
        return 0
    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        curr = [i]
        for j, cb in enumerate(b, start=1):
            insert = curr[j - 1] + 1
            delete = prev[j] + 1
            replace = prev[j - 1] + (0 if ca == cb else 1)
            curr.append(min(insert, delete, replace))
        prev = curr
    return prev[-1]


def _wer(ref, hyp):
    ref_words = ref.split()
    hyp_words = hyp.split()
    if not ref_words:
        return 0.0
    return _levenshtein(ref_words, hyp_words) / float(len(ref_words))


def _cer(ref, hyp):
    if not ref:
        return 0.0
    return _levenshtein(list(ref), list(hyp)) / float(len(ref))

