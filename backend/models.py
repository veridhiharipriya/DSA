from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base


# =========================================================
# SECTION
# =========================================================

class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False
    )

    # Faculty assigned to this section
    faculty_name = Column(
        String(100),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # One section → many students
    students = relationship(
        "Student",
        back_populates="section",
        cascade="all, delete-orphan"
    )


# =========================================================
# STUDENT
# =========================================================

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        nullable=True
    )

    department = Column(
        String(150),
        nullable=True
    )

    year = Column(
        String(50),
        nullable=True
    )

    section_id = Column(
        Integer,
        ForeignKey("sections.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Student → Section
    section = relationship(
        "Section",
        back_populates="students"
    )


# =========================================================
# ASSIGNMENT
# =========================================================

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(
        Integer,
        ForeignKey("sections.id"),
        nullable=False,
        index=True
    )
    title = Column(String(200), nullable=False)
    subject = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    faculty_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    section = relationship("Section")


# =========================================================
# SUBMISSION
# =========================================================

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)

    # Link submission to an actual student
    student_record_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=True
    )

    assignment_id = Column(
        Integer,
        ForeignKey("assignments.id"),
        nullable=True,
        index=True
    )

    student_name = Column(
        String(100),
        nullable=False
    )

    assignment_title = Column(
        String(200),
        nullable=False
    )

    subject = Column(
        String(150),
        nullable=False
    )

    filename = Column(
        String(255),
        nullable=False
    )

    file_path = Column(
        String(500),
        nullable=True
    )

    status = Column(
        String(50),
        default="PENDING"
    )

    submitted_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Submission → Student
    student = relationship(
        "Student",
        foreign_keys=[student_record_id]
    )
    assignment = relationship("Assignment")


# =========================================================
# EVALUATION
# =========================================================

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)

    submission_id = Column(
        Integer,
        nullable=False
    )

    marks = Column(
        Float,
        nullable=True
    )

    similarity_percentage = Column(
        Float,
        nullable=True
    )

    fingerprints_1 = Column(
        Integer,
        nullable=True
    )

    fingerprints_2 = Column(
        Integer,
        nullable=True
    )

    winnowed_1 = Column(
        Integer,
        nullable=True
    )

    winnowed_2 = Column(
        Integer,
        nullable=True
    )

    common_fingerprints = Column(
        Integer,
        nullable=True
    )

    common_passages = Column(
        Text,
        nullable=True
    )

    feedback = Column(
        Text,
        nullable=True
    )

    faculty_name = Column(
        String(100),
        nullable=True
    )

    evaluation_status = Column(
        String(50),
        default="PENDING"
    )

    evaluated_at = Column(
        DateTime,
        nullable=True
    )