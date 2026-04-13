import os
import django
import shutil


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "songproject.settings")
django.setup()

from song_models.models import Song, SongUser
from django.contrib.auth.models import User

from datetime import datetime, timedelta
import random


from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populate the database with sample data"

    def handle(self, *args, **kwargs):
        SongUser.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS("=== INICIANDO POBLACIÓN DE BASE DE DATOS ===\n")
        )
        self.clean()
        usuarios = self.crear_usuarios()
        self.crear_superusuario()
        songs = self.crear_canciones()

        if usuarios and songs:
            self.crear_relaciones_songuser(usuarios, songs)
        else:
            self.stdout.write(self.style.WARNING("No se pudo crear relaciones"))

        self.ver_resumen()

        self.stdout.write(self.style.SUCCESS("=====POBLACION CON EXITO!! =====\n"))

    def ver_resumen(self):
        print("\n=== RESUMEN FINAL ===")
        print(f"Usuarios normales: {User.objects.filter(is_superuser=False).count()}")
        print(f"Superusuarios: {User.objects.filter(is_superuser=True).count()}")
        print(f"Canciones: {Song.objects.count()}")
        print(f"Relaciones SongUser: {SongUser.objects.count()}")
        print(
            f"Total reproducciones: {sum(s.number_times_played for s in Song.objects.all())}"
        )

    def clean(self):
        self.stdout.write("Clean bbdd")
        Song.objects.all().delete()
        SongUser.objects.all().delete()
        User.objects.all().delete()

        self.clean_media_folder()
        self.stdout.write(self.style.SUCCESS("BBDD limpiada\n"))

    def crear_usuarios(self):
        self.stdout.write("Creando 2 usuarios")

        user1 = User.objects.create_user(
            username="ana_maria",
            password="ana1234",
            email="ana@email.com",
            first_name="Ana",
            last_name="Maria",
        )
        user2 = User.objects.create_user(
            username="juan_perez",
            password="juan1234",
            email="juan@email.com",
            first_name="Juan",
            last_name="Pérez",
        )

        return user1, user2

    def crear_superusuario(self):
        self.stdout.write("Creando superusuario")
        if not User.objects.filter(username="alumnodb").exists():
            superuser = User.objects.create_superuser(
                username="alumnodb", password="alumnodb", email="alumnodb@email.com"
            )
            self.stdout.write("Superusuario creado")
        else:
            self.stdout.write("Superusuario ya existe")

    def crear_canciones(self):
        self.stdout.write("Insertando canciones")

        # Obtener la ruta al archivo actual
        current_file = os.path.abspath(__file__)

        # self.stdout.write(f"Archivo actual: {current_file}")

        # Necesitamos subir hasta la raíz del proyecto (donde está manage.py y Media/)
        # Partimos de: .../songproject/song_models/management/commands/populate.py
        management_dir = os.path.dirname(current_file)  # .../management
        song_models_dir = os.path.dirname(management_dir)  # .../song_models
        songproject_dir = os.path.dirname(song_models_dir)  # .../songproject
        project_root = os.path.dirname(songproject_dir)  # .../ (raíz del proyecto)

        media_dir = os.path.join(project_root, "Media")

        # self.stdout.write(f"Buscando archivos en: {media_dir}")

        songs_data = [
            {
                "title": "Super Trouper",
                "artist": "ABBA",
                "language": "EN",
                "category": "POP",
                "audio": "ABBA - Super Trouper.mp3",
                "lrc": "ABBA - Super Trouper.lrc",
                "image": "ABBA - Super Trouper.jpg",
            },
            {
                "title": "Here In The Real World",
                "artist": "Alan Jackson",
                "language": "ES",
                "category": "ROCK",
                "audio": "Alan Jackson - Here In The Real World.mp3",
                "lrc": "Alan Jackson - Here In The Real World.lrc",
                "image": "Alan Jackson - Here In The Real World.jpg",
            },
            {
                "title": "Don't Forget to Remember",
                "artist": "Beegees",
                "language": "FR",
                "category": "JAZZ",
                "audio": "Beegees - Don't Forget to Remember.mp3",
                "lrc": "Beegees - Don't Forget to Remember.lrc",
                "image": "Beegees - Don't Forget to Remember.jpg",
            },
        ]

        create_songs = []

        for s in songs_data:
            audio_path = os.path.join(media_dir, s["audio"])
            lrc_path = os.path.join(media_dir, s["lrc"])
            image_path = os.path.join(media_dir, s["image"])

            if not all(os.path.exists(p) for p in [audio_path, lrc_path, image_path]):
                self.stdout.write(f"Falta archivos para {s['title']}")
                continue

            song = Song.objects.create(
                title=s["title"],
                artist=s["artist"],
                language=s["language"],
                category=s["category"],
                # Nota: Los FileField requieren abrir los archivos de una manera especial
            )

            # asignar los archivos
            with open(audio_path, "rb") as f:
                song.audio_file.save(s["audio"], f, save=False)

            with open(lrc_path, "rb") as f:
                song.lrc_file.save(s["lrc"], f, save=False)

            with open(image_path, "rb") as f:
                song.background_image.save(s["image"], f, save=False)

            song.save()
            create_songs.append(song)

        self.stdout.write(f"Total canciones creada : {len(create_songs)}\n")
        return create_songs

    def crear_relaciones_songuser(self, users, songs):
        self.stdout.write("Creando relaciones SOngUser")
        user1, user2 = users
        relation_created = 0

        # para cada usuario, crear algunas relaciones
        for u in [user1, user2]:
            # cada usuario escuchará algunas canciones, pero no todas
            num_songs_to = random.randint(2, len(songs))
            selected_songs = random.sample(songs, num_songs_to)

            for song in selected_songs:
                # Generar datos aleatorios
                correct = random.randint(5, 20)
                wrong = random.randint(0, 10)

                # Fecha aleatoria en los últimos 30 días
                dias_pasado = random.randint(0, 30)
                played_at = datetime.now() - timedelta(days=dias_pasado)

                # Crear o actualizar la relacion
                song_user, created = SongUser.objects.update_or_create(
                    user=u,
                    song=song,
                    defaults={
                        "correct_guesses": correct,
                        "wrong_guesses": wrong,
                        "played_at": played_at,
                    },
                )

                # IMPORTANTE: La señal post_save actualizará number_times_played automáticamente

                relation_created += 1
                action = "creada" if created else "actualizada"

                self.stdout.write(f"Relacion {action}: {u.username} - {song.title}")

        self.stdout.write(f"Total relaciones creadas/actualizadas: {relation_created}")
        return relation_created

    def clean_media_folder(self):
        """Elimina la carpeta media/ si existe para evitar archivos duplicados"""
        # Obtener la ruta de la carpeta media (mismo cálculo que en crear_canciones)
        current_file = os.path.abspath(__file__)
        management_dir = os.path.dirname(current_file)
        song_models_dir = os.path.dirname(management_dir)
        songproject_dir = os.path.dirname(song_models_dir)
        project_root = os.path.dirname(songproject_dir)
        media_path = os.path.join(project_root, "media")

        if os.path.exists(media_path):
            self.stdout.write(f"Eliminando carpeta media existente: {media_path}")
            shutil.rmtree(media_path)
            self.stdout.write(self.style.SUCCESS("✓ Carpeta media eliminada"))
        else:
            self.stdout.write("No existía carpeta media para eliminar")
