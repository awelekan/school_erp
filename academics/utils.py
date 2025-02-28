import pandas as pd
from io import StringIO
from .models import Student, ClassLevel, AcademicSession, AcademicTerm, Enrollment

def process_csv(file):
    df = pd.read_csv(file)
    enrollments = []

    for _, row in df.iterrows():
        student = Student.objects.get(username=row["username"])
        session = AcademicSession.objects.get(year=row["session"])
        term = AcademicTerm.objects.get(session=session, name=row["term"])

        enrollment = Enrollment(
            student=student,
            session=session,
            term=term,
        )
        enrollments.append(enrollment)

    Enrollment.objects.bulk_create(enrollments)
    return f"{len(enrollments)} students enrolled successfully!"
