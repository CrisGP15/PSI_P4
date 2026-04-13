# api/test_additional.py
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from song_models.models import Song, SongUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import get_urlconf, set_urlconf
from django.test.utils import override_settings


class AdditionalAPITests(APITestCase):

    def setUp(self):
        dummy_audio = SimpleUploadedFile(
            "test.mp3", b"file_content", content_type="audio/mpeg"
        )
        dummy_lrc = SimpleUploadedFile(
            "test.lrc", b"[00:00.00] Lyrics", content_type="text/plain"
        )
        dummy_image = SimpleUploadedFile(
            "test.jpg", b"image_content", content_type="image/jpeg"
        )
        self.user = User.objects.create_user(
            username="testuser", password="pass1234"
        )
        self.song = Song.objects.create(
            title="Test Song",
            artist="Test Artist",
            language="EN",
            audio_file=dummy_audio,
            lrc_file=dummy_lrc,
            background_image=dummy_image,
            category="POP",
            number_times_played=5,
        )

    # --- Cubre views.py línea 50: n <= 0 raise ValueError ---
    def test_top_songs_zero_n(self):
        """n=0 debe devolver 400 (cubre el raise ValueError del if n <= 0)"""
        url = reverse("songs-top") + "?n=0"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_top_songs_negative_n(self):
        """n negativo debe devolver 400"""
        url = reverse("songs-top") + "?n=-5"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Cubre get_queryset: usuario anónimo devuelve queryset vacío ---
    def test_songuser_list_unauthenticated(self):
        """Sin autenticación debe devolver 401"""
        url = reverse("songusers-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_songuser_create_unauthenticated(self):
        """Crear SongUser sin autenticación debe devolver 401"""
        url = reverse("songusers-list")
        data = {"song": self.song.id, "correct_guesses": 1, "wrong_guesses": 0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Cubre get_queryset: usuario solo ve sus propios registros ---
    def test_songuser_list_only_own_records(self):
        """Un usuario solo ve sus propios SongUser"""
        other_user = User.objects.create_user(
            username="otheruser", password="pass1234"
        )
        SongUser.objects.create(
            song=self.song, user=self.user,
            correct_guesses=2, wrong_guesses=1
        )
        SongUser.objects.create(
            song=self.song, user=other_user,
            correct_guesses=1, wrong_guesses=0
        )
        self.client.force_authenticate(user=self.user)
        url = reverse("songusers-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # --- Cubre perform_create: user se asigna del contexto ---
    def test_songuser_create_assigns_user_from_context(self):
        """perform_create asigna el user del request, no del body"""
        self.client.force_authenticate(user=self.user)
        url = reverse("songusers-list")
        data = {"song": self.song.id, "correct_guesses": 3, "wrong_guesses": 0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        song_user = SongUser.objects.get(id=response.data["id"])
        self.assertEqual(song_user.user, self.user)

    
class DebugURLTest(APITestCase):
    @override_settings(DEBUG=True)
    def test_debug_static_urls(self):
        """Cubre el bloque if settings.DEBUG en urls.py"""
        from importlib import reload
        from songproject import urls
        reload(urls)
        self.assertIsNotNone(urls.urlpatterns)