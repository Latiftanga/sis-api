from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Person(models.Model):
    """Person abstract model"""
    GENDER_CHOICES = (
        ('m', 'Male'), ('f', 'Female')
    )
    first_name = models.CharField(max_length=32)
    other_names = models.CharField(max_length=32, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    mobile_phone = models.CharField(
        max_length=32, blank=True, default=''
    )
    religion = models.CharField(
        max_length=32, blank=True, default=''
    )
    nationality = models.CharField(max_length=128)
    national_id = models.CharField(
        max_length=32, blank=True, default=''
    )
    social_security_no = models.CharField(
        max_length=32, blank=True, default=''
    )
    
    def __str__(self):
        return f"{self.first_name} {self.other_names}"

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """"Manage for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_adminuser(self, email, password):
        """Create and return a new admin user"""
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_teacheruser(self, email, password):
        """Create and return a new teacher user"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user

    def create_studentuser(self, email, password):
        """Create and return a new student user"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user

    def create_guardianuser(self, email, password):
        """Create and return a new guardian user"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=32, unique=True)
    is_active = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_guardian = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class SignupPin(models.Model):
    pin = models.CharField(max_length=10, unique=True)
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE,
        null=True, blank=True
    )  # Can be linked to a user later
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pin


class Teacher(Person):
    school = models.ForeignKey(
        School, related_name='teachers', on_delete=models.CASCADE
    )
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE,
        related_name='teacher', blank=True, null=True
    )


class Student(Person):
    school = models.ForeignKey(
        School, related_name='students', on_delete=models.CASCADE
    )
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE,
        related_name='student', blank=True, null=True
    )
    grade_level = models.CharField(max_length=10)  # Example: '1st Grade', '2nd Grade'


class Subject(models.Model):
    """Subjects in the system"""
    name = models.CharField(
        max_length=255, unique=True
    )
    subject_type = models.CharField(max_length=64)
    subect_code = models.CharField(
        max_length=64, unique=True, blank=True, default=''
    )

    def __str__(self) -> str:
        return f'{self.name}'


class Lesson(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE,
        related_name='lessons'
    )
    description = models.CharField(max_length=50)  # e.g., algebra
    semester = models.CharField(max_length=20)  # e.g., "Fall", "Spring"
    year = models.IntegerField()

    def __str__(self):
        return f"{self.subject.name} - ({self.semester} {self.year})"


class AssignmentType(models.Model):
    lesson = models.ForeignKey(
        Lesson, related_name='assignment_types',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)  # e.g., "Tests", "Quizzes"
    percentage = models.FloatField()  # Must sum to 100% across categories in a course

    def __str__(self):
        return f"{self.name} - {self.percentage}%"


class Assignment(models.Model):
    assignment_type = models.ForeignKey(
        AssignmentType, related_name='assignments',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    max_points = models.IntegerField()  # The maximum possible points for this assignment

    def __str__(self):
        return f"{self.name} ({self.assignment_type.name})"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, related_name='enrollments', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='enrollments', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student} enrolled in {self.lesson.name}"


class Score(models.Model):
    student = models.ForeignKey(Student, related_name='scores', on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, related_name='scores', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('student', 'assignment')

    def __str__(self):
        return f"{self.student} - {self.assignment.name}: {self.points}/{self.assignment.max_points}"
