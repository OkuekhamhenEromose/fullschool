from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
import datetime
from .models import CustomUser, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult


class StudentHomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        student_obj = Students.objects.get(admin=request.user.id)
        total_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
        attendance_present = AttendanceReport.objects.filter(
            student_id=student_obj, status=True).count()
        attendance_absent = AttendanceReport.objects.filter(
            student_id=student_obj, status=False).count()
        
        course_obj = Courses.objects.get(id=student_obj.course_id.id)
        total_subjects = Subjects.objects.filter(course_id=course_obj).count()
        
        subject_name = []
        data_present = []
        data_absent = []
        subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
        
        for subject in subject_data:
            attendance = Attendance.objects.filter(subject_id=subject.id)
            attendance_present_count = AttendanceReport.objects.filter(
                attendance_id__in=attendance, status=True, student_id=student_obj.id).count()
            attendance_absent_count = AttendanceReport.objects.filter(
                attendance_id__in=attendance, status=False, student_id=student_obj.id).count()
            
            subject_name.append(subject.subject_name)
            data_present.append(attendance_present_count)
            data_absent.append(attendance_absent_count)
            
        context = {
            "total_attendance": total_attendance,
            "attendance_present": attendance_present,
            "attendance_absent": attendance_absent,
            "total_subjects": total_subjects,
            "subject_name": subject_name,
            "data_present": data_present,
            "data_absent": data_absent
        }
        return render(request, "student_template/student_home_template.html", context)


class StudentViewAttendance(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        student = Students.objects.get(admin=request.user.id)
        course = student.course_id
        subjects = Subjects.objects.filter(course_id=course)
        
        context = {
            "subjects": subjects
        }
        return render(request, "student_template/student_view_attendance.html", context)


class StudentViewAttendancePost(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        try:
            start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            
            subject_obj = Subjects.objects.get(id=subject_id)
            user_obj = CustomUser.objects.get(id=request.user.id)
            stud_obj = Students.objects.get(admin=user_obj)

            attendance = Attendance.objects.filter(
                attendance_date__range=(start_date_parse, end_date_parse),
                subject_id=subject_obj
            )
            
            attendance_reports = AttendanceReport.objects.filter(
                attendance_id__in=attendance,
                student_id=stud_obj
            )

            context = {
                "subject_obj": subject_obj,
                "attendance_reports": attendance_reports
            }

            return render(request, 'student_template/student_attendance_data.html', context)
        
        except Exception as e:
            messages.error(request, f"Error processing request: {str(e)}")
            return redirect('student_view_attendance')


class StudentApplyLeave(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        student_obj = Students.objects.get(admin=request.user.id)
        leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
        
        context = {
            "leave_data": leave_data
        }
        return render(request, 'student_template/student_apply_leave.html', context)


class StudentApplyLeaveSave(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(
                student_id=student_obj,
                leave_date=leave_date,
                leave_message=leave_message,
                leave_status=0
            )
            leave_report.save()
            messages.success(request, "Applied for Leave.")
        except Exception as e:
            messages.error(request, f"Failed to Apply Leave: {str(e)}")
        
        return redirect('student_apply_leave')


class StudentFeedback(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        student_obj = Students.objects.get(admin=request.user.id)
        feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
        
        context = {
            "feedback_data": feedback_data
        }
        return render(request, 'student_template/student_feedback.html', context)


class StudentFeedbackSave(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        feedback = request.POST.get('feedback_message')
        student_obj = Students.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(
                student_id=student_obj,
                feedback=feedback,
                feedback_reply=""
            )
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
        except Exception as e:
            messages.error(request, f"Failed to Send Feedback: {str(e)}")
        
        return redirect('student_feedback')


class StudentProfile(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=request.user.id)
        student = Students.objects.get(admin=user)

        context = {
            "user": user,
            "student": student
        }
        return render(request, 'student_template/student_profile.html', context)


class StudentProfileUpdate(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password and password.strip():
                customuser.set_password(password)
            customuser.save()

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()
            
            messages.success(request, "Profile Updated Successfully")
        except Exception as e:
            messages.error(request, f"Failed to Update Profile: {str(e)}")
        
        return redirect('student_profile')


class StudentViewResult(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        student = Students.objects.get(admin=request.user.id)
        student_result = StudentResult.objects.filter(student_id=student.id)
        
        context = {
            "student_result": student_result,
        }
        return render(request, "student_template/student_view_result.html", context)