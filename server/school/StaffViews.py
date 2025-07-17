from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
import json
from .models import CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel, Attendance, AttendanceReport, LeaveReportStaff, FeedBackStaffs, StudentResult


class StaffHomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        subjects = Subjects.objects.filter(staff_id=request.user.id)
        course_id_list = []
        
        for subject in subjects:
            course = Courses.objects.get(id=subject.course_id.id)
            course_id_list.append(course.id)

        final_course = list(set(course_id_list))  # Remove duplicates using set
        students_count = Students.objects.filter(course_id__in=final_course).count()
        subject_count = subjects.count()
        
        attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
        staff = Staffs.objects.get(admin=request.user.id)
        leave_count = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()

        subject_list = []
        attendance_list = []
        for subject in subjects:
            attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
            subject_list.append(subject.subject_name)
            attendance_list.append(attendance_count1)

        students_attendance = Students.objects.filter(course_id__in=final_course)
        student_list = []
        student_list_attendance_present = []
        student_list_attendance_absent = []
        
        for student in students_attendance:
            attendance_present_count = AttendanceReport.objects.filter(
                status=True, student_id=student.id).count()
            attendance_absent_count = AttendanceReport.objects.filter(
                status=False, student_id=student.id).count()
            student_list.append(f"{student.admin.first_name} {student.admin.last_name}")
            student_list_attendance_present.append(attendance_present_count)
            student_list_attendance_absent.append(attendance_absent_count)

        context = {
            "students_count": students_count,
            "attendance_count": attendance_count,
            "leave_count": leave_count,
            "subject_count": subject_count,
            "subject_list": subject_list,
            "attendance_list": attendance_list,
            "student_list": student_list,
            "attendance_present_list": student_list_attendance_present,
            "attendance_absent_list": student_list_attendance_absent
        }
        return render(request, "staff_template/staff_home_template.html", context)


class StaffTakeAttendanceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        subjects = Subjects.objects.filter(staff_id=request.user.id)
        session_years = SessionYearModel.objects.all()
        context = {
            "subjects": subjects,
            "session_years": session_years
        }
        return render(request, "staff_template/take_attendance_template.html", context)


class StaffApplyLeaveView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        staff_obj = Staffs.objects.get(admin=request.user.id)
        leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
        context = {
            "leave_data": leave_data
        }
        return render(request, "staff_template/staff_apply_leave_template.html", context)


class StaffApplyLeaveSaveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(
                staff_id=staff_obj,
                leave_date=leave_date,
                leave_message=leave_message,
                leave_status=0
            )
            leave_report.save()
            messages.success(request, "Applied for Leave.")
        except Exception as e:
            messages.error(request, f"Failed to Apply Leave: {str(e)}")
        
        return redirect('staff_apply_leave')


class StaffFeedbackView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "staff_template/staff_feedback_template.html")


class StaffFeedbackSaveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        feedback = request.POST.get('feedback_message')
        staff_obj = Staffs.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStaffs(
                staff_id=staff_obj,
                feedback=feedback,
                feedback_reply=""
            )
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
        except Exception as e:
            messages.error(request, f"Failed to Send Feedback: {str(e)}")
        
        return redirect('staff_feedback')


class StaffUpdateAttendanceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        subjects = Subjects.objects.filter(staff_id=request.user.id)
        session_years = SessionYearModel.objects.all()
        context = {
            "subjects": subjects,
            "session_years": session_years
        }
        return render(request, "staff_template/update_attendance_template.html", context)


class StaffProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=request.user.id)
        staff = Staffs.objects.get(admin=user)
        context = {
            "user": user,
            "staff": staff
        }
        return render(request, 'staff_template/staff_profile.html', context)


class StaffProfileUpdateView(LoginRequiredMixin, View):
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

            staff = Staffs.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()
            messages.success(request, "Profile Updated Successfully")
        except Exception as e:
            messages.error(request, f"Failed to Update Profile: {str(e)}")
        
        return redirect('staff_profile')


class StaffAddResultView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        subjects = Subjects.objects.filter(staff_id=request.user.id)
        session_years = SessionYearModel.objects.all()
        context = {
            "subjects": subjects,
            "session_years": session_years,
        }
        return render(request, "staff_template/add_result_template.html", context)


class StaffAddResultSaveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        student_admin_id = request.POST.get('student_list')
        assignment_marks = request.POST.get('assignment_marks')
        exam_marks = request.POST.get('exam_marks')
        subject_id = request.POST.get('subject')

        try:
            student_obj = Students.objects.get(admin=student_admin_id)
            subject_obj = Subjects.objects.get(id=subject_id)

            check_exist = StudentResult.objects.filter(
                subject_id=subject_obj,
                student_id=student_obj
            ).exists()
            
            if check_exist:
                result = StudentResult.objects.get(
                    subject_id=subject_obj,
                    student_id=student_obj
                )
                result.subject_assignment_marks = assignment_marks
                result.subject_exam_marks = exam_marks
                result.save()
                messages.success(request, "Result Updated Successfully!")
            else:
                result = StudentResult(
                    student_id=student_obj,
                    subject_id=subject_obj,
                    subject_exam_marks=exam_marks,
                    subject_assignment_marks=assignment_marks
                )
                result.save()
                messages.success(request, "Result Added Successfully!")
                
        except Exception as e:
            messages.error(request, f"Failed to Add Result: {str(e)}")
        
        return redirect('staff_add_result')


# AJAX View Classes
@method_decorator(csrf_exempt, name='dispatch')
class GetStudentsView(View):
    def post(self, request, *args, **kwargs):
        subject_id = request.POST.get("subject")
        session_year = request.POST.get("session_year")

        subject_model = Subjects.objects.get(id=subject_id)
        session_model = SessionYearModel.objects.get(id=session_year)

        students = Students.objects.filter(
            course_id=subject_model.course_id,
            session_year_id=session_model
        )

        list_data = [{
            "id": student.admin.id,
            "name": f"{student.admin.first_name} {student.admin.last_name}"
        } for student in students]

        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class SaveAttendanceDataView(View):
    def post(self, request, *args, **kwargs):
        student_ids = request.POST.get("student_ids")
        subject_id = request.POST.get("subject_id")
        attendance_date = request.POST.get("attendance_date")
        session_year_id = request.POST.get("session_year_id")

        try:
            subject_model = Subjects.objects.get(id=subject_id)
            session_year_model = SessionYearModel.objects.get(id=session_year_id)
            json_student = json.loads(student_ids)
            
            attendance = Attendance(
                subject_id=subject_model,
                attendance_date=attendance_date,
                session_year_id=session_year_model
            )
            attendance.save()

            for stud in json_student:
                student = Students.objects.get(admin=stud['id'])
                AttendanceReport(
                    student_id=student,
                    attendance_id=attendance,
                    status=stud['status']
                ).save()
            return HttpResponse("OK")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")


@method_decorator(csrf_exempt, name='dispatch')
class GetAttendanceDatesView(View):
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
class GetAttendanceStudentView(View):
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


@method_decorator(csrf_exempt, name='dispatch')
class UpdateAttendanceDataView(View):
    def post(self, request, *args, **kwargs):
        student_ids = request.POST.get("student_ids")
        attendance_date = request.POST.get("attendance_date")

        try:
            attendance = Attendance.objects.get(id=attendance_date)
            json_student = json.loads(student_ids)

            for stud in json_student:
                student = Students.objects.get(admin=stud['id'])
                attendance_report = AttendanceReport.objects.get(
                    student_id=student,
                    attendance_id=attendance
                )
                attendance_report.status = stud['status']
                attendance_report.save()
            return HttpResponse("OK")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")