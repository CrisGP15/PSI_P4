from django.db.models.signals import post_save
from django.dispatch import receiver  # decorador receiver
from .models import SongUser, Song


@receiver(
    post_save, sender=SongUser
)  # Escuchamos: cuando se guarde un SongUser, hacemos:
def update_song_times_played(sender, instance, created, **kwargs):
    """
    Señal que se activa cuando se crea o se actualiza un SongUser
    Actualiza el contador number_times_played de la canción
    Esta función se ejecutará automáticamente después de guardar un SongUser.
    - instance: el objeto SongUser que se acaba de guardar.
    - created: booleano. True si es un registro NUEVO, False si solo se actualizó.
    """

    # song = instance.song
    # if created:
    #     # Si es nuevo, incrementamos
    #     song.number_times_played += 1
    #     song.save()
    # else:
    #     # Si es actualización, NO incrementamos
    #     # Por ahora, no hacemos nada en actualizaciones
    #     pass

    song = instance.song
    song.number_times_played += 1  # Incrementa siempre
    song.save()
