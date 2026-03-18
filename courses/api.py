from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course, Topic, Lesson, Quiz, QuizAttempt, UserProgress
from .serializers import (
    CourseSerializer, TopicSerializer, LessonSerializer,
    QuizSerializer, QuizAttemptSerializer, UserProgressSerializer
)

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer

    @action(detail=True, methods=['get'])
    def topics(self, request, pk=None):
        course = self.get_object()
        topics = course.topics.filter(is_active=True)
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        course = self.get_object()
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            course=course
        )
        serializer = UserProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.filter(is_active=True)
    serializer_class = TopicSerializer

    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        topic = self.get_object()
        lessons = topic.lessons.filter(is_active=True)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.filter(is_active=True)
    serializer_class = LessonSerializer

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        lesson = self.get_object()
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            course=lesson.topic.course
        )
        progress.completed_lessons.add(lesson)
        progress.current_lesson = lesson
        progress.save()
        serializer = UserProgressSerializer(progress)
        return Response(serializer.data)

class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quiz.objects.filter(is_active=True)
    serializer_class = QuizSerializer

    @action(detail=True, methods=['post'])
    def submit_attempt(self, request, pk=None):
        quiz = self.get_object()
        answers = request.data.get('answers', {})

        # Calculate score
        total_questions = quiz.questions.count()
        correct_answers = 0

        for question in quiz.questions.all():
            user_answer = answers.get(str(question.id))
            if user_answer == question.correct_answer:
                correct_answers += 1

        score = correct_answers
        percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        passed = percentage >= quiz.passing_score

        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            passed=passed,
            answers=answers
        )

        serializer = QuizAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserProgressViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserProgressSerializer
    queryset = UserProgress.objects.all()

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        progress_items = self.get_queryset()
        summary = []
        for progress in progress_items:
            summary.append({
                'course': CourseSerializer(progress.course).data,
                'progress_percentage': progress.progress_percentage,
                'completed_lessons_count': progress.completed_lessons.count(),
                'total_lessons_count': progress.course.topics.filter(is_active=True).count(),
            })
        return Response(summary)