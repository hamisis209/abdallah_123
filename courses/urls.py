from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/form/<str:form_name>/', views.form_topics, name='form_topics'),
    path('notes/<int:course_id>/form/<str:form_name>/<str:topic_slug>/', views.topic_notes, name='topic_notes'),
    path('past-papers/', views.past_papers_home, name='past_papers_home'),
    path('necta/past-papers/', views.necta_past_papers, name='necta_past_papers'),
    path('necta/past-papers/<str:form_name>/', views.necta_past_papers_form, name='necta_past_papers_form'),
    path('annual/past-papers/', views.annual_past_papers, name='annual_past_papers'),
    path('annual/past-papers/<str:form_name>/', views.annual_past_papers_form, name='annual_past_papers_form'),
    path('joint/past-papers/', views.joint_past_papers, name='joint_past_papers'),
    path('joint/past-papers/<str:form_name>/', views.joint_past_papers_form, name='joint_past_papers_form'),
]
