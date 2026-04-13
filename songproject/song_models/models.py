from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.contrib.auth import get_user_model


class Song(models.Model):
    LANGUAGE_CHOICES = [
        ("EN", "Inglés"),
        ("ES", "Español"),
        ("FR", "Francés"),
        ("DE", "Alemán"),
        ("IT", "Italiano"),
        ("PT", "Portugués"),
        ("JA", "Japanese"),
        ("ZH", "Chinese"),
    ]

    CATEGORY_CHOICES = [
        ("POP", "Pop"),
        ("ROCK", "Rock"),
        ("JAZZ", "Jazz"),
        ("HIPHOP", "Hip-Hop"),
        ("CLASSICAL", "Classical"),
        ("REGGAE", "Reggae"),
        ("LATIN", "Latin"),
        ("KPOP", "K-Pop"),
        ("COUNTRY", "Country"),
        ("BLUES", "Blues"),
        ("FOLK", "Folk"),
        ("ELECTRONIC", "Electronic"),
        ("R&B", "R&B"),
        ("SOUL", "Soul"),
        ("METAL", "Metal"),
        ("PUNK", "Punk"),
        ("ALTERNATIVE", "Alternative"),
        ("INDIE", "Indie"),
        ("GOSPEL", "Gospel"),
        ("WORLD", "World Music"),
    ]

    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    audio_file = models.FileField(
        upload_to="media/",
        verbose_name="Archivo de audio",
        validators=[
            FileExtensionValidator(allowed_extensions=["mp3", "wav", "ogg", "m4a"])
        ],
    )

    lrc_file = models.FileField(
        upload_to="media/",
        verbose_name="Archivo LRC con letra sincronizada",
        validators=[FileExtensionValidator(allowed_extensions=["lrc", "txt"])],
    )

    background_image = models.FileField(
        upload_to="media/",
        verbose_name="Imagen de fondo",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png"])],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
        help_text="Fecha y hora en que se creó el registro",
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    number_times_played = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],  # No puede ser negativo
        verbose_name="Veces reproducida",
    )

    class Meta:
        verbose_name = "Canción"
        verbose_name_plural = "Canciones"
        ordering = ["-created_at"]  # Más recientes primero
        indexes = [
            models.Index(fields=["title", "artist"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.artist} - {self.title}"


class SongUser(models.Model):
    song = models.ForeignKey(
        "Song", on_delete=models.CASCADE, verbose_name="Canción asociada"
    )

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name="Usuario asociado"
    )

    played_at = models.DateTimeField(
        auto_now=True,
    )

    correct_guesses = models.IntegerField(default=0, verbose_name="Número de aciertos")
    wrong_guesses = models.IntegerField(default=0, verbose_name="Número de errores")

    class Meta:
        verbose_name = "Estadística de canción por usuario"
        verbose_name_plural = "Estadísticas de canciones por usuario"
        ordering = ["-played_at"]

    def __str__(self):
        return f"{self.user.username} - {self.song.title}"

    def save(self, *args, **kwargs):
        # Guardar el objeto actual
        super().save(*args, **kwargs)

        # LUego borrar otros registros con el mismo usuario y cancion(exepto este)
        SongUser.objects.filter(user=self.user, song=self.song).exclude(
            pk=self.pk
        ).delete()
