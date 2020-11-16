from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Topic, Course, Student, Order
from .forms import *

from django.http import HttpResponse


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    student_name = request.user.get_username()
    return render(request, 'myapp/index.html', {'top_list': top_list, 'student_name': student_name})


def about(request):
    student_name = request.user.get_username()
    return render(request, 'myapp/about.html', {'student_name': student_name})


def detail(request, topic_id):
    student_name = request.user.get_username()
    topic_local = get_object_or_404(Topic, pk=topic_id)
    courses = Course.objects.filter(topic=topic_id)
    topic_name = topic_local.name.upper()
    topic_length = str(topic_local.length) + ' weeks'
    return render(request, 'myapp/detail.html',
                  {'topic_name': topic_name, 'topic_length': topic_length, 'courses': courses, 'student_name': student_name})


def findcourses(request):
    # breakpoint()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            length = form.cleaned_data['length']
            max_price = form.cleaned_data['max_price']
            if length != 0:
                topics = Topic.objects.filter(length=length)
                course_list = []
                topic_list = []
                for top in topics:
                    if top.courses.filter(price__lte=max_price).count() != 0:
                        course_list.append((top, list(top.courses.filter(price__lte=max_price))))
                return render(request, 'myapp/results.html',
                              {'course_list': course_list, 'name': name, 'length': length, 'topic_list': topic_list})
            else:
                topics = Topic.objects.all()
                course_list = []
                topics.distinct('name')
                for top in topics:
                    if top.courses.filter(price__lte=max_price).count() != 0:
                        course_list.append((top, list(top.courses.filter(price__lte=max_price))))
                return render(request, 'myapp/results.html',
                              {'course_list': course_list, 'name': name, 'length': length})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        student_name = request.user.get_username()
        return render(request, 'myapp/findcourses.html', {'form': form, 'student_name': student_name})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save(commit=False)
            student = order.student
            status = order.order_status
            order.save()
            if status == 1:
                for c in order.courses.all():
                    student.registered_courses.add(c)
            return render(request, 'myapp/order_response.html', {'courses': courses, 'order': order})
        else:
            return render(request, 'myapp/place_order.html', {'form': form})

    else:
        form = OrderForm()
        return render(request, 'myapp/place_order.html', {'form': form})
