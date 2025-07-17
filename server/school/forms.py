from django import forms
from .models import Courses, SessionYearModel


class DateInput(forms.DateInput):
    input_type = "date"


TAILWIND_INPUT_CLASS = "block w-full px-4 py-2 text-sm border rounded-md shadow-sm focus:outline-none focus:ring focus:ring-indigo-300"

class AddStudentForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=50,
        widget=forms.EmailInput(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    password = forms.CharField(
        label="Password",
        max_length=50,
        widget=forms.PasswordInput(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    username = forms.CharField(
        label="Username",
        max_length=50,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    address = forms.CharField(
        label="Address",
        max_length=50,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT_CLASS})
    )

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    course_id = forms.ChoiceField(
        label="Course",
        choices=[],
        widget=forms.Select(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    gender = forms.ChoiceField(
        label="Gender",
        choices=gender_list,
        widget=forms.Select(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    session_year_id = forms.ChoiceField(
        label="Session Year",
        choices=[],
        widget=forms.Select(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    profile_pic = forms.FileField(
        label="Profile Pic",
        required=False,
        widget=forms.FileInput(attrs={"class": TAILWIND_INPUT_CLASS})
    )

    def __init__(self, *args, **kwargs):
        super(AddStudentForm, self).__init__(*args, **kwargs)
        self.fields['course_id'].choices = [
            (course.id, course.course_name) for course in Courses.objects.all()
        ]
        self.fields['session_year_id'].choices = [
            (session.id, f"{session.session_start_year} to {session.session_end_year}")
            for session in SessionYearModel.objects.all()
        ]


class EditStudentForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=50,
        widget=forms.EmailInput(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    username = forms.CharField(
        label="Username",
        max_length=50,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    address = forms.CharField(
        label="Address",
        max_length=50,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT_CLASS})
    )

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    course_id = forms.ChoiceField(
        label="Course",
        choices=[],
        widget=forms.Select(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    gender = forms.ChoiceField(
        label="Gender",
        choices=gender_list,
        widget=forms.Select(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    session_year_id = forms.ChoiceField(
        label="Session Year",
        choices=[],
        widget=forms.Select(attrs={"class": TAILWIND_INPUT_CLASS})
    )
    profile_pic = forms.FileField(
        label="Profile Pic",
        required=False,
        widget=forms.FileInput(attrs={"class": TAILWIND_INPUT_CLASS})
    )

    def __init__(self, *args, **kwargs):
        super(EditStudentForm, self).__init__(*args, **kwargs)
        self.fields['course_id'].choices = [
            (course.id, course.course_name) for course in Courses.objects.all()
        ]
        self.fields['session_year_id'].choices = [
            (session.id, f"{session.session_start_year} to {session.session_end_year}")
            for session in SessionYearModel.objects.all()
        ]
