import time

import soundfile as sf

from django.shortcuts import render
from django.db.models import Q
from courses.models import Course, Topic, Lesson
from transcription.models import Transcript

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
    if last_metrics and last_metrics.get('latency') is not None:
        latency = last_metrics['latency']
        last_metrics = dict(last_metrics)
        # Latency target is < 1.0s, so fill more when closer to 0.
        last_metrics['latency_pct'] = max(0.0, min(100.0, (1.0 - min(latency, 1.0)) * 100.0))
        last_metrics['latency_band'] = _latency_band(latency)
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
                # WER target is 0.0, so show "closer to zero" as a fuller bar.
                'wer_pct': max(0.0, min(100.0, (1.0 - wer) * 100.0)),
                # Latency target is < 1.0s, so fill more when closer to 0.
                'latency_pct': max(0.0, min(100.0, (1.0 - min(elapsed, 1.0)) * 100.0)),
                'wer_band': _wer_band(wer),
                'latency_band': _latency_band(elapsed),
            }
        else:
            result = {'error': 'Reference text is required.'}
    return render(request, 'core/performance.html', {
        'result': result,
        'last_metrics': last_metrics,
    })


def search_view(request):
    query = request.GET.get('q', '').strip()
    results = {
        'courses': [],
        'topics': [],
        'lessons': [],
        'transcripts': [],
    }

    if query:
        # Search courses
        results['courses'] = Course.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(code__icontains=query)
        ).filter(is_active=True)[:10]

        # Search topics
        results['topics'] = Topic.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).filter(is_active=True).select_related('course')[:10]

        # Search lessons
        results['lessons'] = Lesson.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(objectives__icontains=query)
        ).filter(is_active=True).select_related('topic', 'topic__course')[:10]

        # Search transcripts (only user's own)
        if request.user.is_authenticated:
            results['transcripts'] = Transcript.objects.filter(
                Q(title__icontains=query) | Q(transcript_text__icontains=query)
            ).filter(user=request.user)[:10]

    context = {
        'query': query,
        'results': results,
        'total_results': sum(len(v) for v in results.values())
    }
    return render(request, 'core/search.html', context)
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


def _wer_band(wer):
    if wer > 0.59:
        return 'danger'
    if 0.35 <= wer <= 0.59:
        return 'warning'
    return 'success'


def _latency_band(latency):
    if latency > 1.0:
        return 'danger'
    if latency == 1.0:
        return 'warning'
    return 'success'

