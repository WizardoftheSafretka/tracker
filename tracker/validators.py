from rest_framework.exceptions import ValidationError


def validate_habit_data(data):
    is_pleasant = data.get('is_pleasant')
    related_habit = data.get('related_habit')
    reward = data.get('reward')
    execution_time = data.get('execution_time')
    periodicity = data.get('periodicity')

    if is_pleasant:
        if related_habit:
            raise ValidationError(
                {"related_habit": "Приятная привычка не может иметь связанную привычку."}
            )
        if reward:
            raise ValidationError(
                {"reward": "Приятная привычка не может иметь вознаграждение."}
            )
    else:
        if related_habit and reward:
            raise ValidationError(
                {"related_habit": "Нельзя указывать и связанную привычку, и вознаграждение одновременно."}
            )
        if related_habit and not related_habit.is_pleasant:
            raise ValidationError(
                {"related_habit": "Связанная привычка должна быть приятной."}
            )

    if execution_time and execution_time.total_seconds() > 120:
        raise ValidationError(
            {"execution_time": "Время выполнения не должно превышать 120 секунд."}
        )

    if periodicity and not (1 <= periodicity <= 7):
        raise ValidationError(
            {"periodicity": "Периодичность должна быть от 1 до 7 дней."}
        )

