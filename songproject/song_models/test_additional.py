from django.test import TestCase
from django.contrib.auth.models import User
from song_models.models import Song, SongUser
from django.core.files.uploadedfile import SimpleUploadedFile


class AdditionalCoverageTests(TestCase):
    def setUp(self):
        self.audio = SimpleUploadedFile("test.mp3", b"audio")
        self.lrc = SimpleUploadedFile("test.lrc", b"[00:00] lyric")
        self.image = SimpleUploadedFile("cover.jpg", b"image")
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.song = Song.objects.create(
            title="Test",
            artist="Artist",
            language="EN",
            category="POP",
            audio_file=self.audio,
            lrc_file=self.lrc,
            background_image=self.image,
        )

    def test_save_method_deletes_older_entries(self):
        """Verifica que el método save() borra registros anteriores."""
        # Primera creación
        su1 = SongUser.objects.create(song=self.song, user=self.user)
        self.assertEqual(SongUser.objects.count(), 1)
        # Segunda creación (debería borrar la primera)
        su2 = SongUser.objects.create(song=self.song, user=self.user)
        self.assertEqual(SongUser.objects.count(), 1)
        self.assertEqual(SongUser.objects.first().pk, su2.pk)
