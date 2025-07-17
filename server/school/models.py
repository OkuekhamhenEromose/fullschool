from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()

# Overriding the Default Django Auth 
# User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    HOD = '1'
    STAFF = '2'
    STUDENT = '3'
    
    EMAIL_TO_USER_TYPE_MAP = {
        'hod': HOD,
        'staff': STAFF,
        'student': STUDENT
    }

    user_type_data = ((HOD, "HOD"), (STAFF, "Staff"), (STUDENT, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Subjects(models.Model):
    id =models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    
    # need to give default course
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1) 
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(SessionYearModel, null=True,
                                        on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Attendance(models.Model):
  
    # Subject Attendance
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    stafff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE, default=1)
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


#Creating Django Signals
@receiver(post_save, sender=CustomUser)

# Now Creating a Function which will
# automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
      
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance,
                                    course_id=Courses.objects.get(id=1),
                                    session_year_id=SessionYearModel.objects.get(id=1),
                                    address="",
                                    profile_pic="",
                                    gender="")
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()













# from django.db import models

# # Create your models here.

# class Student(models.Model):
#     # Personal Information
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     date_of_birth = models.DateField()
#     gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

#     # Contact Information
#     address = models.TextField()
#     phone_number = models.CharField(max_length=15)
#     email = models.EmailField(max_length=100)

#     # Parent/Guardian Information
#     guardian_name = models.CharField(max_length=100)
#     guardian_phone_number = models.CharField(max_length=15)
#     guardian_email = models.EmailField(max_length=100)

#     # Academic Information
#     roll_number = models.CharField(max_length=15)
#     admission_date = models.DateField()
#     current_class = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} (Class {self.current_class})"
    
    

    
# # Student Admission model:

# class StudentAdmission(models.Model):
#     ADMISSION_CHOICES = (
#         ('Class1', 'Class 1'),
#         ('Class2', 'Class 2'),
#     )
    
#     ADMISSION_GROUP_CHOICES = (
#         ('Science', 'Science'),
#         ('Arts', 'Arts'),
#         ('Commerce', 'Commerce'),
#         ('General', 'General'),
#     )
    
#     GENDER_CHOICES = (
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#         ('Other', 'Other'),
#     )
    
#     RELIGION_CHOICES = (
#         ('Islam', 'Islam'),
#         ('Christianity', 'Christianity'),
#         ('Buddhism', 'Buddhism'),
#         ('Hinduism', 'Hinduism'),
#     )
    
#     NATIONALITY_CHOICES = (
#         ('Bangladeshi', 'Bangladeshi'),
#     )
    
#     admissionFor = models.CharField(max_length=7, choices=ADMISSION_CHOICES, default='Class1')
#     admissionGroup = models.CharField(max_length=9, choices=ADMISSION_GROUP_CHOICES, default='Science')
#     studentFirstName = models.CharField(max_length=100)
#     studentLastName = models.CharField(max_length=100)
#     studentEmail = models.EmailField()
#     studentPhoneNumber = models.CharField(max_length=15)
#     studentImage = models.ImageField(upload_to='student_images/')
#     studentSignature = models.ImageField(upload_to='student_signatures/')
#     studentGender = models.CharField(max_length=10, choices=GENDER_CHOICES,default='Male')
#     studentReligion = models.CharField(max_length=15, choices=RELIGION_CHOICES,default='Islam')
#     studentNationality = models.CharField(max_length=15, choices=NATIONALITY_CHOICES,default='Bangladesh')
#     birthDate = models.DateField()
#     birthCertificateNumber = models.PositiveIntegerField()
#     fatherName = models.CharField(max_length=100)
#     fatherNID = models.PositiveIntegerField()
#     fatherPhoneNumber = models.CharField(max_length=15)
#     fatherOccupation = models.CharField(max_length=100)
#     fatherReligion = models.CharField(max_length=15, choices=RELIGION_CHOICES,default='Islam')
#     fatherMonthlyIncome = models.PositiveIntegerField()
#     fatherNationality = models.CharField(max_length=15, choices=NATIONALITY_CHOICES,default='Bangladesh')
#     motherName = models.CharField(max_length=100)
#     motherNID = models.PositiveIntegerField()
#     motherPhoneNumber = models.CharField(max_length=15)
#     motherOccupation = models.CharField(max_length=100)
#     motherReligion = models.CharField(max_length=15, choices=RELIGION_CHOICES,default='Islam')
#     motherMonthlyIncome = models.PositiveIntegerField()
#     motherNationality = models.CharField(max_length=15, choices=NATIONALITY_CHOICES,default='Bangladesh')
#     presentAddressLine1 = models.CharField(max_length=100)
#     presentAddressLine2 = models.CharField(max_length=100, blank=True, null=True)
#     presentZila = models.CharField(max_length=100)
#     presentThana = models.CharField(max_length=100, blank=True, null=True)
#     presentPostalCode = models.PositiveIntegerField()
#     permanentAddressLine1 = models.CharField(max_length=100)
#     permanentAddressLine2 = models.CharField(max_length=100, blank=True, null=True)
#     permanentZila = models.CharField(max_length=100)
#     permanentThana = models.CharField(max_length=100, blank=True, null=True)
#     permanentPostalCode = models.PositiveIntegerField()
#     previousClass = models.CharField(max_length=100, blank=True, null=True)
#     previousClassGroup = models.CharField(max_length=15, choices=ADMISSION_GROUP_CHOICES, default='Science', blank=True, null=True)
#     previousClassResultTotalMark = models.PositiveIntegerField(blank=True, null=True)
#     previousClassResultGPA = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
#     previousSchoolName = models.CharField(max_length=100, blank=True, null=True)
#     previousSchoolClassRoll = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return f'{self.studentFirstName} {self.studentLastName} - {self.admissionFor}'