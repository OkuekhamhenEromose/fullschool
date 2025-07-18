from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from .views import HomeView, ContactView, LoginView, RegistrationView, LogoutView
from .HodViews import (
    AdminHomeView, AddStaffView, ManageStaffView, EditStaffView, DeleteStaffView,
    AddCourseView, ManageCourseView, EditCourseView, DeleteCourseView,
    ManageSessionView, AddSessionView, EditSessionView, DeleteSessionView,
    AddStudentView, ManageStudentView, EditStudentView, DeleteStudentView,
    AddSubjectView, ManageSubjectView, EditSubjectView, DeleteSubjectView,
    CheckEmailExistView, CheckUsernameExistView,
    StudentFeedbackMessageView, StudentFeedbackMessageReplyView,
    StaffFeedbackMessageView, StaffFeedbackMessageReplyView,
    StudentLeaveView, StudentLeaveApproveView, StudentLeaveRejectView,
    StaffLeaveView, StaffLeaveApproveView, StaffLeaveRejectView,
    AdminViewAttendanceView, AdminGetAttendanceDatesView, AdminGetAttendanceStudentView,
    AdminProfileView, AdminProfileUpdateView
)
from .StaffViews import (
    StaffHomeView, StaffTakeAttendanceView, StaffApplyLeaveView, StaffApplyLeaveSaveView,
    StaffFeedbackView, StaffFeedbackSaveView, StaffUpdateAttendanceView,
    StaffProfileView, StaffProfileUpdateView, StaffAddResultView, StaffAddResultSaveView,
    GetStudentsView, SaveAttendanceDataView, GetAttendanceDatesView,
    GetAttendanceStudentView, UpdateAttendanceDataView
)
from .StudentViews import (
    StudentHomeView, StudentViewAttendance, StudentViewAttendancePost,
    StudentApplyLeave, StudentApplyLeaveSave, StudentFeedback, StudentFeedbackSave,
    StudentProfile, StudentProfileUpdate, StudentViewResult
)

urlpatterns = [
    # Main Views
    path('', HomeView.as_view(), name="home"),
    path('contact', ContactView.as_view(), name="contact"),
    path('login', LoginView.as_view(), name="login"),
    path('logout_user', LogoutView.as_view(), name="logout_user"),
    path('registration', RegistrationView.as_view(), name="registration"),
    
    # URLS for Student
    path('student_home/', StudentHomeView.as_view(), name="student_home"),
    path('student_view_attendance/', StudentViewAttendance.as_view(), name="student_view_attendance"),
    path('student_view_attendance_post/', StudentViewAttendancePost.as_view(), name="student_view_attendance_post"),
    path('student_apply_leave/', StudentApplyLeave.as_view(), name="student_apply_leave"),
    path('student_apply_leave_save/', StudentApplyLeaveSave.as_view(), name="student_apply_leave_save"),
    path('student_feedback/', StudentFeedback.as_view(), name="student_feedback"),
    path('student_feedback_save/', StudentFeedbackSave.as_view(), name="student_feedback_save"),
    path('student_profile/', StudentProfile.as_view(), name="student_profile"),
    path('student_profile_update/', StudentProfileUpdate.as_view(), name="student_profile_update"),
    path('student_view_result/', StudentViewResult.as_view(), name="student_view_result"),

    # URLS for Staff
    path('staff_home/', StaffHomeView.as_view(), name="staff_home"),
    path('staff_take_attendance/', StaffTakeAttendanceView.as_view(), name="staff_take_attendance"),
    path('get_students/', GetStudentsView.as_view(), name="get_students"),
    path('save_attendance_data/', SaveAttendanceDataView.as_view(), name="save_attendance_data"),
    path('staff_update_attendance/', StaffUpdateAttendanceView.as_view(), name="staff_update_attendance"),
    path('get_attendance_dates/', GetAttendanceDatesView.as_view(), name="get_attendance_dates"),
    path('get_attendance_student/', GetAttendanceStudentView.as_view(), name="get_attendance_student"),
    path('update_attendance_data/', UpdateAttendanceDataView.as_view(), name="update_attendance_data"),
    path('staff_apply_leave/', StaffApplyLeaveView.as_view(), name="staff_apply_leave"),
    path('staff_apply_leave_save/', StaffApplyLeaveSaveView.as_view(), name="staff_apply_leave_save"),
    path('staff_feedback/', StaffFeedbackView.as_view(), name="staff_feedback"),
    path('staff_feedback_save/', StaffFeedbackSaveView.as_view(), name="staff_feedback_save"),
    path('staff_profile/', StaffProfileView.as_view(), name="staff_profile"),
    path('staff_profile_update/', StaffProfileUpdateView.as_view(), name="staff_profile_update"),
    path('staff_add_result/', StaffAddResultView.as_view(), name="staff_add_result"),
    path('staff_add_result_save/', StaffAddResultSaveView.as_view(), name="staff_add_result_save"),
    
    # URLS for Admin (HOD)
    path('admin_home/', AdminHomeView.as_view(), name="admin_home"),
    path('add_staff/', AddStaffView.as_view(), name="add_staff"),
    path('add_staff_save/', AddStaffView.as_view(), name="add_staff_save"),  # Same view handles both GET and POST
    path('manage_staff/', ManageStaffView.as_view(), name="manage_staff"),
    path('edit_staff/<staff_id>/', EditStaffView.as_view(), name="edit_staff"),
    path('edit_staff_save/', EditStaffView.as_view(), name="edit_staff_save"),  # Same view handles both GET and POST
    path('delete_staff/<staff_id>/', DeleteStaffView.as_view(), name="delete_staff"),
    
    path('add_course/', AddCourseView.as_view(), name="add_course"),
    path('add_course_save/', AddCourseView.as_view(), name="add_course_save"),  # Same view handles both GET and POST
    path('manage_course/', ManageCourseView.as_view(), name="manage_course"),
    path('edit_course/<course_id>/', EditCourseView.as_view(), name="edit_course"),
    path('edit_course_save/', EditCourseView.as_view(), name="edit_course_save"),  # Same view handles both GET and POST
    path('delete_course/<course_id>/', DeleteCourseView.as_view(), name="delete_course"),
    
    path('manage_session/', ManageSessionView.as_view(), name="manage_session"),
    path('add_session/', AddSessionView.as_view(), name="add_session"),
    path('add_session_save/', AddSessionView.as_view(), name="add_session_save"),  # Same view handles both GET and POST
    path('edit_session/<session_id>/', EditSessionView.as_view(), name="edit_session"),
    path('edit_session_save/', EditSessionView.as_view(), name="edit_session_save"),  # Same view handles both GET and POST
    path('delete_session/<session_id>/', DeleteSessionView.as_view(), name="delete_session"),
    
    path('add_student/', AddStudentView.as_view(), name="add_student"),
    path('add_student_save/', AddStudentView.as_view(), name="add_student_save"),  # Same view handles both GET and POST
    path('edit_student/<student_id>/', EditStudentView.as_view(), name="edit_student"),
    path('edit_student_save/', EditStudentView.as_view(), name="edit_student_save"),  # Same view handles both GET and POST
    path('manage_student/', ManageStudentView.as_view(), name="manage_student"),
    path('delete_student/<student_id>/', DeleteStudentView.as_view(), name="delete_student"),
    
    path('add_subject/', AddSubjectView.as_view(), name="add_subject"),
    path('add_subject_save/', AddSubjectView.as_view(), name="add_subject_save"),  # Same view handles both GET and POST
    path('manage_subject/', ManageSubjectView.as_view(), name="manage_subject"),
    path('edit_subject/<subject_id>/', EditSubjectView.as_view(), name="edit_subject"),
    path('edit_subject_save/', EditSubjectView.as_view(), name="edit_subject_save"),  # Same view handles both GET and POST
    path('delete_subject/<subject_id>/', DeleteSubjectView.as_view(), name="delete_subject"),
    
    path('check_email_exist/', CheckEmailExistView.as_view(), name="check_email_exist"),
    path('check_username_exist/', CheckUsernameExistView.as_view(), name="check_username_exist"),
    
    path('student_feedback_message/', StudentFeedbackMessageView.as_view(), name="student_feedback_message"),
    path('student_feedback_message_reply/', StudentFeedbackMessageReplyView.as_view(), name="student_feedback_message_reply"),
    path('staff_feedback_message/', StaffFeedbackMessageView.as_view(), name="staff_feedback_message"),
    path('staff_feedback_message_reply/', StaffFeedbackMessageReplyView.as_view(), name="staff_feedback_message_reply"),
    
    path('student_leave_view/', StudentLeaveView.as_view(), name="student_leave_view"),
    path('student_leave_approve/<leave_id>/', StudentLeaveApproveView.as_view(), name="student_leave_approve"),
    path('student_leave_reject/<leave_id>/', StudentLeaveRejectView.as_view(), name="student_leave_reject"),
    path('staff_leave_view/', StaffLeaveView.as_view(), name="staff_leave_view"),
    path('staff_leave_approve/<leave_id>/', StaffLeaveApproveView.as_view(), name="staff_leave_approve"),
    path('staff_leave_reject/<leave_id>/', StaffLeaveRejectView.as_view(), name="staff_leave_reject"),
    
    path('admin_view_attendance/', AdminViewAttendanceView.as_view(), name="admin_view_attendance"),
    path('admin_get_attendance_dates/', AdminGetAttendanceDatesView.as_view(), name="admin_get_attendance_dates"),
    path('admin_get_attendance_student/', AdminGetAttendanceStudentView.as_view(), name="admin_get_attendance_student"),
    
    path('admin_profile/', AdminProfileView.as_view(), name="admin_profile"),
    path('admin_profile_update/', AdminProfileUpdateView.as_view(), name="admin_profile_update"),
]