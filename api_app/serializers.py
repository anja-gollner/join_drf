from rest_framework import serializers
from .models import Contact, Subtask, Task
from rest_framework.exceptions import ValidationError


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)
    assignedTo = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Contact.objects.all())

    class Meta:
        model = Task
        fields = '__all__'
