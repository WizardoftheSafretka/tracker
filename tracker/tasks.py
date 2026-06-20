@shared_task
def send_notification():
    current_time = timezone.now().time()
    habits_list = Habit.objects.filter(time=current_time)
    for habit in habits_list:
        user = habit.user
        if user.tg_chat_id:
            message = f"{user.email} выполните {habit.action} в {habit.place} в {habit.time}!"
            send_telegram_message(user.tg_chat_id, message)