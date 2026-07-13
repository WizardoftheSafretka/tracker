# tracker/tests.py
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Habit

User = get_user_model()


class HabitAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="user1@test.com", password="testpass123", tg_chat_id="12345"
        )
        self.user2 = User.objects.create_user(
            email="user2@test.com", password="testpass123", tg_chat_id="67890"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def create_habit(self, user, **kwargs):
        defaults = {
            "place": "Home",
            "time": "10:00:00",
            "action": "Read",
            "is_pleasant": False,
            "periodicity": 1,
            "execution_time": 60,
            "is_public": False,
            "reward": "Chocolate",
        }
        defaults.update(kwargs)
        return Habit.objects.create(user=user, **defaults)

    def test_list_own_habits(self):
        """Тест получения списка своих привычек с пагинацией"""
        for i in range(6):
            self.create_habit(self.user1, action=f"Habit {i}")

        # Используем namespace 'tracker:'
        url = reverse("tracker:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertEqual(response.data["count"], 6)

    def test_list_public_habits(self):
        """Тест получения списка публичных привычек"""
        self.create_habit(self.user1, action="Public 1", is_public=True)
        self.create_habit(self.user1, action="Private", is_public=False)
        self.create_habit(self.user2, action="Public 2", is_public=True)

        # Используем namespace 'tracker:'
        url = reverse("tracker:public-habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        actions = [h["action"] for h in response.data["results"]]
        self.assertIn("Public 1", actions)
        self.assertIn("Public 2", actions)

    def test_create_habit_valid(self):
        """Тест создания корректной привычки"""
        url = reverse("tracker:habit-list")
        data = {
            "place": "Office",
            "time": "14:30:00",
            "action": "Exercise",
            "is_pleasant": False,
            "periodicity": 3,
            "reward": "Coffee",
            "execution_time": 90,
            "is_public": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        habit = Habit.objects.first()
        self.assertEqual(habit.user, self.user1)
        self.assertEqual(habit.action, "Exercise")

    def test_create_habit_invalid_execution_time(self):
        """Тест: время выполнения не должно превышать 120 секунд"""
        url = reverse("tracker:habit-list")
        data = {
            "place": "Office",
            "time": "14:30:00",
            "action": "Exercise",
            "execution_time": 150,
            "periodicity": 1,
            "reward": "Coffee",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("execution_time", response.data)

    def test_create_habit_invalid_periodicity(self):
        """Тест: периодичность должна быть от 1 до 7"""
        url = reverse("tracker:habit-list")
        data = {
            "place": "Office",
            "time": "14:30:00",
            "action": "Exercise",
            "execution_time": 60,
            "periodicity": 8,
            "reward": "Coffee",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("periodicity", response.data)

    def test_create_habit_with_reward_and_related_habit(self):
        """Тест: нельзя одновременно указывать reward и related_habit"""
        pleasant = self.create_habit(self.user1, action="Pleasant", is_pleasant=True)
        url = reverse("tracker:habit-list")
        data = {
            "place": "Office",
            "time": "14:30:00",
            "action": "Exercise",
            "execution_time": 60,
            "periodicity": 2,
            "reward": "Coffee",
            "related_habit": pleasant.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("related_habit", response.data)

    def test_create_pleasant_habit_with_reward(self):
        """Тест: приятная привычка не может иметь reward"""
        url = reverse("tracker:habit-list")
        data = {
            "place": "Office",
            "time": "14:30:00",
            "action": "Relax",
            "is_pleasant": True,
            "execution_time": 60,
            "periodicity": 1,
            "reward": "Chocolate",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("reward", response.data)

    def test_create_pleasant_habit_with_related_habit(self):
        """Тест: приятная привычка не может иметь related_habit"""
        other = self.create_habit(self.user1, action="Other")
        url = reverse("tracker:habit-list")
        data = {
            "place": "Office",
            "time": "14:30:00",
            "action": "Relax",
            "is_pleasant": True,
            "execution_time": 60,
            "periodicity": 1,
            "related_habit": other.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("related_habit", response.data)

    def test_create_habit_with_non_pleasant_related_habit(self):
        """Тест: related_habit должна быть приятной привычкой"""
        non_pleasant = self.create_habit(
            self.user1, action="NonPleasant", is_pleasant=False
        )
        url = reverse("tracker:habit-list")
        data = {
            "place": "Office",
            "time": "14:30:00",
            "action": "Exercise",
            "execution_time": 60,
            "periodicity": 2,
            "related_habit": non_pleasant.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("related_habit", response.data)

    def test_retrieve_own_habit(self):
        """Тест получения своей привычки"""
        habit = self.create_habit(self.user1)
        url = reverse("tracker:habit-detail", args=[habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], habit.id)

    def test_retrieve_public_habit_other_user(self):
        """Тест получения публичной привычки другого пользователя"""
        habit = self.create_habit(self.user2, action="Other Public", is_public=True)
        url = reverse("tracker:habit-detail", args=[habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Other Public")

    def test_retrieve_private_habit_other_user_forbidden(self):
        """Тест: нельзя получить приватную привычку другого пользователя"""
        habit = self.create_habit(self.user2, action="Private Other", is_public=False)
        url = reverse("tracker:habit-detail", args=[habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_habit(self):
        """Тест обновления своей привычки"""
        habit = self.create_habit(self.user1, action="Old Action")
        url = reverse("tracker:habit-detail", args=[habit.id])
        data = {"action": "New Action"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.action, "New Action")

    def test_update_other_habit_forbidden(self):
        """Тест: нельзя обновлять привычку другого пользователя"""
        habit = self.create_habit(self.user2, action="Other")
        url = reverse("tracker:habit-detail", args=[habit.id])
        data = {"action": "Changed"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_habit(self):
        """Тест удаления своей привычки"""
        habit = self.create_habit(self.user1)
        url = reverse("tracker:habit-detail", args=[habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=habit.id).exists())

    def test_delete_other_habit_forbidden(self):
        """Тест: нельзя удалять привычку другого пользователя"""
        habit = self.create_habit(self.user2)
        url = reverse("tracker:habit-detail", args=[habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        """Тест доступа без аутентификации"""
        self.client.logout()
        url = reverse("tracker:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_public_habits_unauthenticated(self):
        """Тест: публичные привычки доступны без аутентификации"""
        self.client.logout()
        url = reverse("tracker:public-habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
