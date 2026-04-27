from rest_framework import serializers
from song_models.models import Song, SongUser
from django.contrib.auth.models import User


class SongSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Song (solo lectura)"""

    audio_url = serializers.SerializerMethodField()
    lyrics_url = serializers.SerializerMethodField()

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
            "audio_url",
            "lyrics_url",
            "created_at",
            "number_times_played",
        ]
        read_only_fields = ["id", "created_at", "number_times_played"]

    def get_audio_url(self, obj):
        if not obj.audio_file:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.audio_file.url) if request else obj.audio_file.url

    def get_lyrics_url(self, obj):
        if not obj.lrc_file:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.lrc_file.url) if request else obj.lrc_file.url


class SongUserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo SongUser (CRUD completo)"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SongUser
        fields = ["id", "song", "user", "played_at", "correct_guesses", "wrong_guesses"]
        read_only_fields = ["id", "played_at"]
