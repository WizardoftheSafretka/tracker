from rest_framework import serializers

from tracker.models import Habit
from tracker.validators import validate_habit_data


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)
        validators = [validate_habit_data]