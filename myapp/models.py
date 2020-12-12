from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    length = models.IntegerField(default=12)

    def __str__(self):
        return self.name


class Course(models.Model):
    Min_Price = 50.00
    Max_Price = 500.00
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Min_Price), MaxValueValidator(Max_Price)])
    for_everyone = models.BooleanField(default=True)
    optional = models.TextField(default='')
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title



class Student(User):   
    def img_path(instance, filename):
        now = datetime.datetime.now()
        dt_string = now.strftime("%d%m%Y%H%M%S") 
        return 'Profile_Image/user_{0}/{1}{2}'.format(instance.username,dt_string, filename) 
    
    LVL_CHOICES = [('HS', 'High School'), ('UG', 'Undergraduate'), ('PG', 'Postgraduate'), ('ND', 'No Degree')]
    level = models.CharField(choices=LVL_CHOICES, max_length=2, default='HS')
    # Make the field address in Student model ‘optional’.
    address = models.CharField(max_length=300, blank=True)
    province = models.CharField(max_length=2, default='ON')
    registered_courses = models.ManyToManyField(Course, blank=True)
    interested_in = models.ManyToManyField(Topic)
    photo = models.ImageField(upload_to=img_path, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name




class Order(models.Model):
    ORDER_STATE = [(0, 'Cancelled'), (1, 'Confirmed'), (2, 'On Hold')]
    courses = models.ManyToManyField(Course)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    # choices of valid values = {0,1}.
    def order_status_validators(value):
        if (value != 0) and (value != 1):
            raise ValidationError(gettext_lazy('%(value)s is not 0 or 1'), params={'value': value}, )

    order_status = models.IntegerField(choices=ORDER_STATE, default=1, validators=[order_status_validators])
    order_date = models.DateField(default=timezone.now)

    def __str__(self):
        courses_str = ''
        for course in self.courses.all():
            courses_str += course.title + ' '
        order_status_local = self.ORDER_STATE[self.order_status][1]
        return self.student.first_name + ' ' + self.student.last_name + ' ' + courses_str + order_status_local

    def total_cost(self):
        courses = self.courses.all()
        total_price = 0
        for course in courses:
            total_price += course.price
        print(total_price)
        return total_price

    def total_items(self):
        courses = self.courses.all()
        total_num=0
        for course in courses:
            total_num+=1
        return str(total_num)



class Review(models.Model):
    reviewer = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.reviewer + ' ' + self.course.title + ' ' + str(self.rating) + ' ' + self.comments + ' ' + str(
            self.date)
