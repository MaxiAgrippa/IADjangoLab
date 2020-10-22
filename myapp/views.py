from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Topic, Course, Student, Order


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    course_list = Course.objects.all().order_by('-title')[:5]
    response = HttpResponse()
    heading1 = '<p>' + 'List of topics: ' + '</p>'
    response.write(heading1)
    for topic in top_list:
        para = '<p>' + str(topic.id) + ': ' + str(topic) + '</p>'
        response.write(para)
    heading1 = '<p>' + 'List of courses: ' + '</p>'
    for course in course_list:
        para = '<p> Course title: ' + str(course.title) + '; Price: ' + str(course.price) + '</p>'
        response.write(para)
    return response


def about(request):
    response = HttpResponse()
    para = '<p>This is an E-learning Website! Search our Topics to find all available Courses.</p>'
    response.write(para)
    return response


def detail(request, topic_id):
    topic_local = get_object_or_404(Topic, pk=topic_id)
    courses = Course.objects.filter(topic=topic_id)
    response = HttpResponse()
    para = '<p>' + topic_local.name.upper() + '<p>'
    response.write(para)
    para = '<p> ' + str(topic_local.length) + ' weeks <p>'
    response.write(para)
    for course in courses:
        para = '<p> Course title: ' + str(course.title) + '</p>'
        response.write(para)
    return response
