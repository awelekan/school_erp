from django.db import models
from accounts.models import User  # Importing User model for relationships
import uuid


#Academic Year
class AcademicSession(models.Model):
    year = models.CharField(max_length=9, unique=True)  # Example: 2024/2025
    is_active = models.BooleanField(default=True)  # Track the current session

    def __str__(self):
        return self.year

class AcademicTerm(models.Model):
    TERM_CHOICES = [
        ('First Term', 'First Term'),
        ('Second Term', 'Second Term'),
        ('Third Term', 'Third Term'),
    ]

    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name="terms")
    name = models.CharField(max_length=20, choices=TERM_CHOICES)
    is_active = models.BooleanField(default=True)  # Track the active term

    class Meta:
        unique_together = ('session', 'name')

    def __str__(self):
        return f"{self.name} - {self.session.year}"

class ClassLevel(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., JSS1, JSS2, SS1
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ClassArm(models.Model):
    level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name="class_arms")  
    name = models.CharField(max_length=10)  # e.g., A, B, C
    class_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'teacher'})

    class Meta:
        unique_together = ('level', 'name')

    def __str__(self):
        return f"{self.level.name} {self.name}"  # Example: JSS1 A

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    student_id = models.CharField(max_length=20, unique=True)  # Custom student ID
    class_arm = models.ForeignKey(ClassArm, on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    address = models.TextField(blank=True, null=True)
    parent_name = models.CharField(max_length=100, blank=True, null=True)
    parent_contact = models.CharField(max_length=15, blank=True, null=True)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.student_id}"
    
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'session', 'term')

    def __str__(self):
        return f"{self.student.student_id} - {self.term.name} ({self.session.year})"
    
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Example: Mathematics
    description = models.TextField(blank=True, null=True)
    class_levels = models.ManyToManyField(ClassLevel, related_name="subjects")  # Which classes study this subject
    teachers = models.ManyToManyField(User, related_name="subjects_taught", limit_choices_to={'role': 'teacher'})  # Teachers for this subject

    def __str__(self):
        return self.name
    
class TeacherAssignment(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_arm = models.ForeignKey(ClassArm, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('teacher', 'subject', 'class_arm')  # Prevent duplicate assignments

    def __str__(self):
        return f"{self.teacher.username} - {self.subject.name} - {self.class_arm}"

class ClassSchedule(models.Model):
    class_arm = models.ForeignKey(ClassArm, on_delete=models.CASCADE, related_name="schedule")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ("Monday", "Monday"),
            ("Tuesday", "Tuesday"),
            ("Wednesday", "Wednesday"),
            ("Thursday", "Thursday"),
            ("Friday", "Friday"),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('class_arm', 'subject', 'day_of_week', 'start_time')

    def __str__(self):
        return f"{self.class_arm} - {self.subject} ({self.day_of_week} {self.start_time}-{self.end_time})"
    

class MidTermTest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='midterm_tests')
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)
    class_arm = models.ForeignKey("ClassArm", on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='midterm_tests_taught')
    test_1 = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # 15 marks
    test_2 = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # 15 marks

    class Meta:
        unique_together = ('student', 'subject', 'class_arm')

    @property
    def total_midterm(self):
        return self.test_1 + self.test_2  # Mid-term total = 30 marks

    def __str__(self):
        return f"{self.student.username} - {self.subject.name} Mid-Term ({self.total_midterm}/30)"

class FinalExam(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='final_exams')
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)
    class_arm = models.ForeignKey("ClassArm", on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='final_exams_taught')
    exam_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # 70 marks

    class Meta:
        unique_together = ('student', 'subject', 'class_arm')

    def __str__(self):
        return f"{self.student.username} - {self.subject.name} Exam ({self.exam_score}/70)"

class FinalGrade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='final_grades')
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)
    class_arm = models.ForeignKey("ClassArm", on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='final_grades_given')
    midterm = models.OneToOneField(MidTermTest, on_delete=models.CASCADE)
    final_exam = models.OneToOneField(FinalExam, on_delete=models.CASCADE)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    grade = models.CharField(max_length=2, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'subject', 'class_arm')

    def save(self, *args, **kwargs):
        self.total_score = self.midterm.total_midterm + self.final_exam.exam_score  # Total Score = 30 + 70 = 100

        # Assign Grades
        if self.total_score >= 90:
            self.grade = "A+"
        elif self.total_score >= 80:
            self.grade = "A"
        elif self.total_score >= 70:
            self.grade = "B"
        elif self.total_score >= 60:
            self.grade = "C"
        elif self.total_score >= 50:
            self.grade = "D"
        else:
            self.grade = "F"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.subject.name} ({self.total_score}/100 - {self.grade})"

class ReportCard(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    class_arm = models.ForeignKey("ClassArm", on_delete=models.CASCADE)
    term = models.CharField(max_length=20, choices=[("First Term", "First Term"), ("Second Term", "Second Term"), ("Third Term", "Third Term")])
    session = models.CharField(max_length=10)  # E.g., 2024/2025
    attendance = models.PositiveIntegerField(default=0)  # Number of days present
    total_days = models.PositiveIntegerField(default=0)  # Total school days
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'class_arm', 'term', 'session')

    def __str__(self):
        return f"{self.student.username} - {self.term} Report Card ({self.session})"

    @property
    def attendance_percentage(self):
        if self.total_days == 0:
            return 0
        return round((self.attendance / self.total_days) * 100, 2)

    def generate_performance_summary(self):
        grades = FinalGrade.objects.filter(student=self.student, class_arm=self.class_arm)
        total_score = sum(grade.total_score for grade in grades)
        subjects_count = grades.count()

        if subjects_count > 0:
            avg_score = total_score / subjects_count
        else:
            avg_score = 0

        return {
            "total_score": total_score,
            "average_score": round(avg_score, 2),
            "attendance_percentage": self.attendance_percentage,
            "remarks": self.remarks or "No remarks provided."
        }
