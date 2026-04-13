from rest_framework import serializers
from song_models.models import Song, SongUser
from django.contrib.auth.models import User


class SongSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Song (solo lectura)"""

    class Meta:
        model = Song
        fields = [
            "id",
            "title",
            "artist",
            "language",
            "category",
            "audio_file",
            "lrc_file",
            "background_image",
            "created_at",
            "number_times_played",
        ]
        read_only_fields = ["id", "created_at", "number_times_played"]


class SongUserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo SongUser (CRUD completo)"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SongUser
        fields = ["id", "song", "user", "played_at", "correct_guesses", "wrong_guesses"]
        read_only_fields = ["id", "played_at"]
