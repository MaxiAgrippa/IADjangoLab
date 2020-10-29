from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Topic, Course, Student, Order


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index0.html', {'top_list': top_list})


def about(request):
    return render(request, 'myapp/about0.html')


def detail(request, topic_id):
    topic_local = get_object_or_404(Topic, pk=topic_id)
    courses = Course.objects.filter(topic=topic_id)
    topic_name = topic_local.name.upper()
    topic_length = str(topic_local.length) + ' weeks'
    return render(request, 'myapp/detail0.html',
                  {'topic_name': topic_name, 'topic_length': topic_length, 'courses': courses})
