from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Topic, Course, Student, Order
from .forms import SearchForm


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list})


def about(request):
    return render(request, 'myapp/about.html')


def detail(request, topic_id):
    topic_local = get_object_or_404(Topic, pk=topic_id)
    courses = Course.objects.filter(topic=topic_id)
    topic_name = topic_local.name.upper()
    topic_length = str(topic_local.length) + ' weeks'
    return render(request, 'myapp/detail.html',
                  {'topic_name': topic_name, 'topic_length': topic_length, 'courses': courses})


def findcourses(request):
    # breakpoint()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            length = form.cleaned_data['length']
            max_price = form.cleaned_data['max_price']
            if length is not None:
                topics = Topic.objects.filter(length=length)
                courselist = []
                for top in topics:
                    courselist = courselist + list(top.courses.filter(price__lt=max_price))
                return render(request, 'myapp/results.html', {'courselist': courselist, 'name': name, 'length': length})
            else:
                courselist = []
                courses = Course.objects.filter(price__lt=max_price)
                courselist += list(courses)
                return render(request, 'myapp/results.html', {'courselist': courselist, 'name': name, 'length': length})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findcourses.html', {'form': form})
