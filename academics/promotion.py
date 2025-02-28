from django.utils import timezone
from .models import Student, Enrollment, AcademicSession, ClassLevel

def promote_students():
    current_session = AcademicSession.objects.filter(is_active=True).first()
    if not current_session:
        return "No active session found!"

    students = Enrollment.objects.filter(session=current_session, term__name="Third Term")
    
    for enrollment in students:
        student = enrollment.student
        if student.class_level.next_class:
            student.class_level = student.class_level.next_class
            student.save()

    return "Class Promotion Completed!"
