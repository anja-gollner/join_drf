from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=50, default='#2a3647')
    initials = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Task(models.Model):
    PROGRESS_CHOICES = [
        ('todo', 'To Do'),
        ('in progress', 'In Progress'),
        ('await feedback', 'Await Feedback'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('urgent', 'Urgent'),
    ]

    CATEGORY_CHOICES = [
        ('Technical Task', 'Technical Task'),
        ('User Story', 'User Story'),
    ]

    assignedTo = models.ManyToManyField("Contact")
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='Technical Task')
    description = models.TextField(blank=True, null=True)
    dueDate = models.DateField()
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default='medium')
    progress = models.CharField(
        max_length=20, choices=PROGRESS_CHOICES, default='todo')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Subtask(models.Model):
    task = models.ForeignKey(
        "Task", on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
