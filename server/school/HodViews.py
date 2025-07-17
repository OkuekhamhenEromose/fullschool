from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from datetime import datetime

from .forms import AddStudentForm, EditStudentForm
from .models import (CustomUser, Staffs, Courses, Subjects, Students, 
                    SessionYearModel, FeedBackStudent, FeedBackStaffs, 
                    LeaveReportStudent, LeaveReportStaff, Attendance, 
                    AttendanceReport, StudentResult)


class AdminHomeView(LoginRequiredMixin, TemplateView):
    template_name = "hod_template/home_content.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Basic counts
        context['all_student_count'] = Students.objects.all().count()
        context['subject_count'] = Subjects.objects.all().count()
        context['course_count'] = Courses.objects.all().count()
        context['staff_count'] = Staffs.objects.all().count()

        # Course data
        course_all = Courses.objects.all()
        context['course_name_list'] = []
        context['subject_count_list'] = []
        context['student_count_list_in_course'] = []

        for course in course_all:
            subjects = Subjects.objects.filter(course_id=course.id).count()
            students = Students.objects.filter(course_id=course.id).count()
            context['course_name_list'].append(course.course_name)
            context['subject_count_list'].append(subjects)
            context['student_count_list_in_course'].append(students)

        # Subject data
        subject_all = Subjects.objects.all()
        context['subject_list'] = []
        context['student_count_list_in_subject'] = []
        
        for subject in subject_all:
            course = Courses.objects.get(id=subject.course_id.id)
            student_count = Students.objects.filter(course_id=course.id).count()
            context['subject_list'].append(subject.subject_name)
            context['student_count_list_in_subject'].append(student_count)

        # Staff attendance data
        context['staff_attendance_present_list'] = []
        context['staff_attendance_leave_list'] = []
        context['staff_name_list'] = []

        staffs = Staffs.objects.all()
        for staff in staffs:
            subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
            attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
            leaves = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
            context['staff_attendance_present_list'].append(attendance)
            context['staff_attendance_leave_list'].append(leaves)
            context['staff_name_list'].append(staff.admin.first_name)

        # Student attendance data
        context['student_attendance_present_list'] = []
        context['student_attendance_leave_list'] = []
        context['student_name_list'] = []

        students = Students.objects.all()
        for student in students:
            attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
            absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
            leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
            context['student_attendance_present_list'].append(attendance)
            context['student_attendance_leave_list'].append(leaves + absent)
            context['student_name_list'].append(student.admin.first_name)

        return context


class AddStaffView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "hod_template/add_staff_template.html")

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=2
            )
            user.staffs.address = address
            user.save()
            messages.success(request, "Staff Added Successfully!")
        except Exception as e:
            messages.error(request, f"Failed to Add Staff: {str(e)}")
        
        return redirect('add_staff')


class ManageStaffView(LoginRequiredMixin, ListView):
    model = Staffs
    template_name = "hod_template/manage_staff_template.html"
    context_object_name = "staffs"


class EditStaffView(LoginRequiredMixin, View):
    def get(self, request, staff_id, *args, **kwargs):
        staff = Staffs.objects.get(admin=staff_id)
        context = {
            "staff": staff,
            "id": staff_id
        }
        return render(request, "hod_template/edit_staff_template.html", context)

    def post(self, request, staff_id, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Staff Updated Successfully.")
        except Exception as e:
            messages.error(request, f"Failed to Update Staff: {str(e)}")
        
        return redirect('edit_staff', staff_id=staff_id)


class DeleteStaffView(LoginRequiredMixin, View):
    def get(self, request, staff_id, *args, **kwargs):
        staff = Staffs.objects.get(admin=staff_id)
        try:
            staff.delete()
            messages.success(request, "Staff Deleted Successfully.")
        except Exception as e:
            messages.error(request, f"Failed to Delete Staff: {str(e)}")
        return redirect('manage_staff')


class AddCourseView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "hod_template/add_course_template.html")

    def post(self, request, *args, **kwargs):
        course = request.POST.get('course')
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Course Added Successfully!")
        except Exception as e:
            messages.error(request, f"Failed to Add Course: {str(e)}")
        return redirect('add_course')


class ManageCourseView(LoginRequiredMixin, ListView):
    model = Courses
    template_name = 'hod_template/manage_course_template.html'
    context_object_name = 'courses'


class EditCourseView(LoginRequiredMixin, View):
    def get(self, request, course_id, *args, **kwargs):
        course = Courses.objects.get(id=course_id)
        context = {
            "course": course,
            "id": course_id
        }
        return render(request, 'hod_template/edit_course_template.html', context)

    def post(self, request, course_id, *args, **kwargs):
        course_name = request.POST.get('course')
        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, "Course Updated Successfully.")
        except Exception as e:
            messages.error(request, f"Failed to Update Course: {str(e)}")
        return redirect('edit_course', course_id=course_id)


class DeleteCourseView(LoginRequiredMixin, View):
    def get(self, request, course_id, *args, **kwargs):
        course = Courses.objects.get(id=course_id)
        try:
            course.delete()
            messages.success(request, "Course Deleted Successfully.")
        except Exception as e:
            messages.error(request, f"Failed to Delete Course: {str(e)}")
        return redirect('manage_course')


class ManageSessionView(LoginRequiredMixin, ListView):
    model = SessionYearModel
    template_name = "hod_template/manage_session_template.html"
    context_object_name = "session_years"


class AddSessionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "hod_template/add_session_template.html")

    def post(self, request, *args, **kwargs):
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            sessionyear = SessionYearModel(
                session_start_year=session_start_year,
                session_end_year=session_end_year
            )
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
        except Exception as e:
            messages.error(request, f"Failed to Add Session Year: {str(e)}")
        return redirect("add_session")


class EditSessionView(LoginRequiredMixin, View):
    def get(self, request, session_id, *args, **kwargs):
        session_year = SessionYearModel.objects.get(id=session_id)
        context = {
            "session_year": session_year
        }
        return render(request, "hod_template/edit_session_template.html", context)

    def post(self, request, session_id, *args, **kwargs):
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()
            messages.success(request, "Session Year Updated Successfully.")
        except Exception as e:
            messages.error(request, f"Failed to Update Session Year: {str(e)}")
        return redirect('edit_session', session_id=session_id)


class DeleteSessionView(LoginRequiredMixin, View):
    def get(self, request, session_id, *args, **kwargs):
        session = SessionYearModel.objects.get(id=session_id)
        try:
            session.delete()
            messages.success(request, "Session Deleted Successfully.")
        except Exception as e:
            messages.error(request, f"Failed to Delete Session: {str(e)}")
        return redirect('manage_session')


class AddStudentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = AddStudentForm()
        context = {
            "form": form
        }
        return render(request, 'hod_template/add_student_template.html', context)

    def post(self, request, *args, **kwargs):
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            session_year_id = form.cleaned_data['session_year_id']
            course_id = form.cleaned_data['course_id']
            gender = form.cleaned_data['gender']

            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    user_type=3
                )
                user.students.address = address
                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj
                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session_year_obj
                user.students.gender = gender
                user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Student Added Successfully!")
            except Exception as e:
                messages.error(request, f"Failed to Add Student: {str(e)}")
        else:
            messages.error(request, "Form validation failed!")
        return redirect('add_student')


class ManageStudentView(LoginRequiredMixin, ListView):
    model = Students
    template_name = 'hod_template/manage_student_template.html'
    context_object_name = 'students'


class EditStudentView(LoginRequiredMixin, View):
    def get(self, request, student_id, *args, **kwargs):
        request.session['student_id'] = student_id
        student = Students.objects.get(admin=student_id)
        form = EditStudentForm()
        
        form.fields['email'].initial = student.admin.email
        form.fields['username'].initial = student.admin.username
        form.fields['first_name'].initial = student.admin.first_name
        form.fields['last_name'].initial = student.admin.last_name
        form.fields['address'].initial = student.address
        form.fields['course_id'].initial = student.course_id.id
        form.fields['gender'].initial = student.gender
        form.fields['session_year_id'].initial = student.session_year_id.id

        context = {
            "id": student_id,
            "username": student.admin.username,
            "form": form
        }
        return render(request, "hod_template/edit_student_template.html", context)

    def post(self, request, student_id, *args, **kwargs):
        if request.session.get('student_id') is None:
            return redirect('manage_student')

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            course_id = form.cleaned_data['course_id']
            gender = form.cleaned_data['gender']
            session_year_id = form.cleaned_data['session_year_id']

            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                student_model = Students.objects.get(admin=student_id)
                student_model.address = address
                course = Courses.objects.get(id=course_id)
                student_model.course_id = course
                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                student_model.session_year_id = session_year_obj
                student_model.gender = gender
                if profile_pic_url is not None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                
                del request.session['student_id']
                messages.success(request, "Student Updated Successfully!")
            except Exception as e:
                messages.error(request, f"Failed to Update Student: {str(e)}")
        else:
            messages.error(request, "Form validation failed!")
        
        return redirect('edit_student', student_id=student_id)


class DeleteStudentView(LoginRequiredMixin, View):
    def get(self, request, student_id, *args, **kwargs):
        student = Students.objects.get(admin=student_id)
        try:
            student.delete()
            messages.success(request, "Student Deleted Successfully.")
        except Exception as e:
            messages.error(request, f"Failed to Delete Student: {str(e)}")
        return redirect('manage_student')


class AddSubjectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        courses = Courses.objects.all()
        staffs = CustomUser.objects.filter(user_type='2')
        context = {
            "courses": courses,
            "staffs": staffs
        }
        return render(request, 'hod_template/add_subject_template.html', context)

    def post(self, request, *args, **kwargs):
        subject_name = request.POST.get('subject')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')

        try:
            course = Courses.objects.get(id=course_id)
            staff = CustomUser.objects.get(id=staff_id)
            subject = Subjects(
                subject_name=subject_name,
                course_id=course,
                staff_id=staff
            )
            subject.save()
            messages.success(request, "Subject Added Successfully!")
        except Exception as e:
            messages.error(request, f"Failed to Add Subject: {str(e)}")
        return redirect('add_subject')


class ManageSubjectView(LoginRequiredMixin, ListView):
    model = Subjects
    template_name = 'hod_template/manage_subject_template.html'
    context_object_name = 'subjects'


class EditSubjectView(LoginRequiredMixin, View):
    def get(self, request, subject_id, *args, **kwargs):
        subject = Subjects.objects.get(id=subject_id)
        courses = Courses.objects.all()
        staffs = CustomUser.objects.filter(user_type='2')
        context = {
            "subject": subject,
            "courses": courses,
            "staffs": staffs,
            "id": subject_id
        }
        return render(request, 'hod_template/edit_subject_template.html', context)

    def post(self, request, subject_id, *args, **kwargs):
        subject_name = request.POST.get('subject')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            subject.save()
            messages.success(request, "Subject Updated Successfully.")
        except Exception as e:
            messages.error(request, f"Failed to Update Subject: {str(e)}")
        return redirect('edit_subject', subject_id=subject_id)


class DeleteSubjectView(LoginRequiredMixin, View):
    def get(self, request, subject_id, *args, **kwargs):
        subject = Subjects.objects.get(id=subject_id)
        try:
            subject.delete()
            messages.success(request, "Subject Deleted Successfully.")
        except Exception as e:
            messages.error(request, f"Failed to Delete Subject: {str(e)}")
        return redirect('manage_subject')


@method_decorator(csrf_exempt, name='dispatch')
class CheckEmailExistView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        user_obj = CustomUser.objects.filter(email=email).exists()
        return HttpResponse(user_obj)


@method_decorator(csrf_exempt, name='dispatch')
class CheckUsernameExistView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        user_obj = CustomUser.objects.filter(username=username).exists()
        return HttpResponse(user_obj)


class StudentFeedbackMessageView(LoginRequiredMixin, ListView):
    model = FeedBackStudent
    template_name = 'hod_template/student_feedback_template.html'
    context_object_name = 'feedbacks'


@method_decorator(csrf_exempt, name='dispatch')
class StudentFeedbackMessageReplyView(View):
    def post(self, request, *args, **kwargs):
        feedback_id = request.POST.get('id')
        feedback_reply = request.POST.get('reply')

        try:
            feedback = FeedBackStudent.objects.get(id=feedback_id)
            feedback.feedback_reply = feedback_reply
            feedback.save()
            return HttpResponse("True")
        except:
            return HttpResponse("False")


class StaffFeedbackMessageView(LoginRequiredMixin, ListView):
    model = FeedBackStaffs
    template_name = 'hod_template/staff_feedback_template.html'
    context_object_name = 'feedbacks'


@method_decorator(csrf_exempt, name='dispatch')
class StaffFeedbackMessageReplyView(View):
    def post(self, request, *args, **kwargs):
        feedback_id = request.POST.get('id')
        feedback_reply = request.POST.get('reply')

        try:
            feedback = FeedBackStaffs.objects.get(id=feedback_id)
            feedback.feedback_reply = feedback_reply
            feedback.save()
            return HttpResponse("True")
        except:
            return HttpResponse("False")


class StudentLeaveView(LoginRequiredMixin, ListView):
    model = LeaveReportStudent
    template_name = 'hod_template/student_leave_view.html'
    context_object_name = 'leaves'


class StudentLeaveApproveView(LoginRequiredMixin, View):
    def get(self, request, leave_id, *args, **kwargs):
        leave = LeaveReportStudent.objects.get(id=leave_id)
        leave.leave_status = 1
        leave.save()
        return redirect('student_leave_view')


class StudentLeaveRejectView(LoginRequiredMixin, View):
    def get(self, request, leave_id, *args, **kwargs):
        leave = LeaveReportStudent.objects.get(id=leave_id)
        leave.leave_status = 2
        leave.save()
        return redirect('student_leave_view')


class StaffLeaveView(LoginRequiredMixin, ListView):
    model = LeaveReportStaff
    template_name = 'hod_template/staff_leave_view.html'
    context_object_name = 'leaves'


class StaffLeaveApproveView(LoginRequiredMixin, View):
    def get(self, request, leave_id, *args, **kwargs):
        leave = LeaveReportStaff.objects.get(id=leave_id)
        leave.leave_status = 1
        leave.save()
        return redirect('staff_leave_view')


class StaffLeaveRejectView(LoginRequiredMixin, View):
    def get(self, request, leave_id, *args, **kwargs):
        leave = LeaveReportStaff.objects.get(id=leave_id)
        leave.leave_status = 2
        leave.save()
        return redirect('staff_leave_view')


class AdminViewAttendanceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        subjects = Subjects.objects.all()
        session_years = SessionYearModel.objects.all()
        context = {
            "subjects": subjects,
            "session_years": session_years
        }
        return render(request, "hod_template/admin_view_attendance.html", context)


@method_decorator(csrf_exempt, name='dispatch')
class AdminGetAttendanceDatesView(View):
    def post(self, request, *args, **kwargs):
        subject_id = request.POST.get("subject")
        session_year = request.POST.get("session_year_id")

        subject_model = Subjects.objects.get(id=subject_id)
        session_model = SessionYearModel.objects.get(id=session_year)
        attendance = Attendance.objects.filter(
            subject_id=subject_model,
            session_year_id=session_model
        )

        list_data = [{
            "id": attendance_single.id,
            "attendance_date": str(attendance_single.attendance_date),
            "session_year_id": attendance_single.session_year_id.id
        } for attendance_single in attendance]

        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdminGetAttendanceStudentView(View):
    def post(self, request, *args, **kwargs):
        attendance_date = request.POST.get('attendance_date')
        attendance = Attendance.objects.get(id=attendance_date)
        attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)

        list_data = [{
            "id": student.student_id.admin.id,
            "name": f"{student.student_id.admin.first_name} {student.student_id.admin.last_name}",
            "status": student.status
        } for student in attendance_data]

        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


class AdminProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=request.user.id)
        context = {
            "user": user
        }
        return render(request, 'hod_template/admin_profile.html', context)


class AdminProfileUpdateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password and password.strip():
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
        except Exception as e:
            messages.error(request, f"Failed to Update Profile: {str(e)}")
        return redirect('admin_profile')


class StaffProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pass


class StudentProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pass