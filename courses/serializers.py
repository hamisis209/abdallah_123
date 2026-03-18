from rest_framework import serializers
from .models import Course, Topic, Lesson, Quiz, Question, QuizAttempt, UserProgress

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'code', 'level', 'is_active']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'slug', 'description', 'form', 'order', 'is_active']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'objectives', 'key_points', 'examples', 'order', 'is_active']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'options', 'correct_answer', 'explanation', 'points', 'order']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'time_limit', 'passing_score', 'is_active', 'questions']

class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['id', 'score', 'total_questions', 'percentage', 'passed', 'answers', 'started_at', 'completed_at']

class UserProgressSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()

    class Meta:
        model = UserProgress
        fields = ['id', 'course', 'completed_lessons', 'completed_topics', 'current_lesson', 'enrollment_date', 'last_activity', 'progress_percentage']