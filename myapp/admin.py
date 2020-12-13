from django.contrib import admin
from .models import Topic, Course, Student, Order, Review


def reduce_course_price(modeladmin, request, queryset):
    for course in queryset:
        price = course.price
        price *= 0.9
        course.price = price
        course.save()


class CourseAdmin(admin.ModelAdmin):
    fields = [('title', 'topic'), ('price', 'num_reviews', 'for_everyone')]
    list_display = ('title', 'topic', 'price')
    actions = [reduce_course_price]


class OrderAdmin(admin.ModelAdmin):
    fields = ['courses', ('student', 'order_status', 'order_date')]
    list_display = ('id', 'student', 'order_status', 'order_date', 'total_items')

class StudentAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'level', 'registered_courses']
    list_display = ['first_name', 'last_name', 'level','get_registered_course']
    
    def get_registered_course(self, obj):
        return "\n".join([rc.title  + "   " for rc in obj.registered_courses.all()])



class CourseInline(admin.TabularInline):
    model = Course


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'length')
    inlines = [CourseInline, ]


# Register your models here.
admin.site.register(Topic, TopicAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
