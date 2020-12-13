from django import forms
from datetime import datetime
from myapp.models import Order, Review, Student, Course


class SearchForm(forms.Form):
    LENGTH_CHOICES = [
        (8, '8 Weeks'),
        (10, '10 Weeks'),
        (12, '12 Weeks'),
        (14, '14 Weeks'),
    ]
    name = forms.CharField(max_length=100, required=False, label='Student Name')
    length = forms.TypedChoiceField(widget=forms.RadioSelect, choices=LENGTH_CHOICES, coerce=int,
                                    label='Preferred course duration:', required=False, empty_value=0)
    max_price = forms.IntegerField(label='Maximum Price', min_value=0)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courses', 'student', 'order_status']
        widgets = {'courses': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        labels = {'student': u'Student Name', }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = {'reviewer', 'course', 'rating', 'comments'}
        widgets = {'courses': forms.RadioSelect()}
        labels = {'reviewer': u'Please enter a valid email', 'rating': u'Rating: An integer between 1 (worst) and 5 (best)'}


class StudentRegisterForm(forms.ModelForm):
    class Meta:
        LVL_CHOICES = [('HS', 'High School'), ('UG', 'Undergraduate'), ('PG', 'Postgraduate'), ('ND', 'No Degree')]
        model = Student
        fields = {'username', 'email', 'password', 'interested_in', 'first_name', 'last_name','photo'}
        widgets = {'level': forms.TypedChoiceField(widget=forms.RadioSelect, choices=LVL_CHOICES, empty_value='HS'),
                   'address': forms.CharField(max_length=300, required=False),
                   'province': forms.CharField(max_length=2, empty_value='ON'),
                   'registered_courses': forms.ModelMultipleChoiceField(required=False, queryset=Course.objects.all())}

    LVL_CHOICES = [('HS', 'High School'), ('UG', 'Undergraduate'), ('PG', 'Postgraduate'), ('ND', 'No Degree')]
    level = forms.TypedChoiceField(label='Level', widget=forms.RadioSelect, choices=LVL_CHOICES, empty_value='HS')
    address = forms.CharField(label='Address', max_length=300, required=False)
    province = forms.CharField(label='Province', max_length=2, empty_value='ON')
    registered_courses = forms.ModelMultipleChoiceField(label='Registered Courses', required=False,
                                                        queryset=Course.objects.all())
    field_order = ['username', 'email', 'password','interested_in', 'first_name', 'last_name','level', 'address','province','registered_courses','photo']
