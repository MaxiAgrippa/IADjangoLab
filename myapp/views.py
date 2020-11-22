from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Topic, Course, Student, Order, Review
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def index(request):
    if request.session.get('last_login'):
        top_list = Topic.objects.all().order_by('id')[:10]
        student_name = request.user.get_username()
        return render(request, 'myapp/index.html', {'top_list': top_list, 'student_name': student_name})
    else:
        http_response = HttpResponse()
        http_response.write('<html> Your last login was more than one hour ago. </html>')
        return http_response


def about(request):
    student_name = request.user.get_username()
    if request.session.get('about_visits'):
        request.session['about_visits'] += 1
        request.session.set_expiry(300)
        about_visits = request.session['about_visits']
    else:
        request.session['about_visits'] = 1
        request.session.set_expiry(300)
        about_visits = request.session['about_visits']
    return render(request, 'myapp/about.html', {'student_name': student_name, 'about_visits': about_visits})


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
                for top in topics:
                    if top.courses.filter(price__lte=max_price).count() != 0:
                        course_list.append((top, list(top.courses.filter(price__lte=max_price))))
                return render(request, 'myapp/results.html',
                              {'course_list': course_list, 'name': name, 'length': length})
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
    student_name = request.user.get_username()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save(commit=True)
            student = order.student
            status = order.order_status
            order.save()
            if status == 1:
                for c in order.courses.all():
                    student.registered_courses.add(c)
            return render(request, 'myapp/order_response.html',
                          {'courses': courses, 'order': order, 'student_name': student_name})
        else:
            return render(request, 'myapp/place_order.html', {'form': form, 'student_name': student_name})
    else:
        form = OrderForm()
        return render(request, 'myapp/place_order.html', {'form': form, 'student_name': student_name})


def review(request):
    student_name = request.user.get_username()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 5 >= rating >= 1:
                course = form.cleaned_data['course']
                c = Course.objects.get(title=course.title)
                c.num_reviews += 1
                c.save()
                f = form.save()
                f.save()
                top_list = Topic.objects.all().order_by('id')[:10]
                return render(request, 'myapp/index.html', {'top_list': top_list, 'student_name': student_name})
            else:
                form = ReviewForm()
                message = 'You must enter a rating between 1 and 5!'
                return render(request, 'myapp/review.html',
                              {'form': form, 'student_name': student_name, 'message': message})
        else:
            form = ReviewForm()
            return render(request, 'myapp/review.html', {'form': form, 'student_name': student_name})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form, 'student_name': student_name})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(datetime.today()) + str(datetime.now())
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


@login_required
def myaccount(request):
    user_name = request.user.get_username()
    student = Student.objects.filter(username=user_name)
    if student:
        firstname = student.first_name
        lastname = student.last_name
        interested_in = student.interested_in
        registered_courses = student.registered_courses
        topic_list = []
        for topic in interested_in:
            topic_list.append(topic)
        course_list = []
        for course in registered_courses:
            course_list.append(course)
        return render(request, 'myapp/myaccount.html',
                      {'firstname': firstname, 'lastname': lastname, 'topic_list': topic_list, 'course_list': course_list})
    else:
        return render(request, 'myapp/myaccount.html', {'message': 'You are not a registered student!'})


def register(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            interested_in = form.cleaned_data['interested_in']
            level = form.cleaned_data['level']
            address = form.cleaned_data['address']
            province = form.cleaned_data['province']
            registered_courses = form.cleaned_data['registered_courses']
            form.save()
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    request.session['last_login'] = str(datetime.today()) + str(datetime.now())
                    request.session.set_expiry(3600)
                    return HttpResponseRedirect(reverse('myapp:index'))
                else:
                    return HttpResponse('Your account is disabled.')
            else:
                return HttpResponse('Invalid login details.')
        else:
            form = StudentRegisterForm()
            return render(request, 'myapp/register.html', {'form': form})
    else:
        form = StudentRegisterForm()
        return render(request, 'myapp/register.html', {'form': form})
