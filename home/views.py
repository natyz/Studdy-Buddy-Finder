from django.views import generic
from django.contrib.auth import logout
from django.http import JsonResponse

from .models import Home
from .models import Login
from .models import Listings
import json
from django.shortcuts import redirect, render


class HomeView(generic.CreateView):
    model = Home
    template_name = 'home/home.html'
    fields = '__all__'


class LoginView(generic.CreateView):
    model = Login
    template_name = 'home/login.html'
    fields = '__all__'


def logout_view(request):
    logout(request)
    return redirect('/login')


# @app.route('/listings')
def listings_view(request):
    majors = ['African American & African Studies', 'American Studies', 'Anthropology', 'Art History', 'Art, Studio',
              'Astronomy', 'Astronomy-Physics', 'Biology', 'Chemistry', 'Chinese Language & Literature', 'Classics',
              'Cognitive Science', 'Comparative Literature', 'Computer Science', 'Drama', 'East Asian Studies',
              'Economics', 'English', 'Environmental Sciences', 'Environmental Thought & Practice', 'French', 'German',
              'Global Studies', 'History', 'Human Biology', 'Italian', 'Japanese Language & Literature',
              'Jewish Studies', 'Latin American Studies', 'Linguistics', 'Mathematics', 'Media Studies',
              'Medieval Studies', 'Middle Eastern and South Asian Languages and Cultures', 'Music', 'Neuroscience',
              'Philosophy', 'Physics', 'Political and Social Thought', 'Political Philosophy, Policy, and Law',
              'Politics', 'Psychology', 'Religious Studies', 'Slavic Languages and Literatures', 'Sociology',
              'South Asian Studies', 'Spanish', 'Statistics', 'Women, Gender, and Sexuality',
              'School of Engineering and Applied Science', 'Aerospace Engineering', 'Biomedical Engineering',
              'Chemical Engineering', 'Civil Engineering', 'Computer Engineering', 'Computer Science',
              'Electrical Engineering', 'Engineering Science', 'Mechanical Engineering', 'Systems Engineering',
              'Mcintire School of Commerce', 'Accounting', 'Finance', 'Information Technology', 'Management',
              'Marketing', 'School of Architecture', 'Architectural History', 'Architecture',
              'Urban & Environmental Planning', 'School of Nursing', 'Bachelor of Science in Nursing (BSN)',
              'RN to BSN', 'Batten School of Leadership and Public Policy', 'B.A. in Public Policy and Leadership',
              'Accelerated B.A./Master of Public Policy (MPP) Program',
              'Accelerated B.A./Master of Public Policy (MPP) Program', 'Curry School of Education', 'Kinesiology',
              'Speech Communications Disorders', 'Youth & Social Innovation', 'Teacher Education majors (B.S.Ed.)',
              'Early Childhood Education', 'Elementary Education', 'Special Education',
              'Teacher Education (post-graduate Master of Teaching)', 'Elementary Education', 'English Education',
              'English as a Second Language Education', 'Foreign Language Education', 'Mathematics Education',
              'Science Education', 'Social Studies Education', 'Special Education']
    return JsonResponse(json.dumps(majors))


# https://project-1-08.herokuapp.com/complete/google-oauth2/
