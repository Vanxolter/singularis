from django.test import Client
import pytest
from django.contrib.auth.models import User

from main.models import Places


class TestJoinStatus:
    def test_join(self):
        client = Client()

        response = client.get("/login/")
        assert response.status_code == 200

        response = client.get("/register/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestCreateUser:
    def test_createuser(self):
        client = Client()

        # Тест по созданию юзера
        user = User.objects.create(username="test", email="test@test.com", password="test")
        client.force_login(user)

        # Тест на создание места
        coordinates = Places.objects.create(author=user, name="Test", places_long=0, places_lat=0)

        # Тест на главную страницу
        response = client.get("")
        assert response.status_code == 200

        # Тест страницу с маршрутом
        response = client.get("/53.87844040332883,27.369689941406254,53.934270043817094,27.675951429212574")
        assert response.status_code == 200