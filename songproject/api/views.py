from rest_framework import viewsets
from .serializers import SongSerializer, SongUserSerializer

from song_models.models import Song, SongUser

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

import random
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class SongPagination(PageNumberPagination):
    page_size = 10


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    pagination_class = SongPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"], url_path="random")
    def random(self, request):
        """Obtener cancion aleatori"""
        count = Song.objects.count()

        if count == 0:
            return Response(
                {"detail": "No songs available"}, status=status.HTTP_404_NOT_FOUND
            )

        random_index = random.randint(0, count - 1)
        random_song = Song.objects.all()[random_index]

        serializer = self.get_serializer(random_song)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="top")
    def top(self, request):
        """Obtener las top canciones (number_times_played más alta)"""
        n = request.query_params.get("n", "3")  # El 3 es el valor por defecto

        try:
            n = int(n)

            if n <= 0:
                raise ValueError
        except ValueError:
            return Response(
                {"error": "Invalid n paramenter"}, status=status.HTTP_400_BAD_REQUEST
            )

        top_songs = Song.objects.order_by("-number_times_played")[:n]
        serializer = self.get_serializer(top_songs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        """Obtener la cancion mediante búsqueda"""
        query = request.query_params.get("title", "")

        if not query:
            return Response(
                {"error": "Missing title parameter"}, status=status.HTTP_400_BAD_REQUEST
            )

        songs = Song.objects.filter(title__icontains=query)

        if not songs.exists():
            return Response({"title": "Nonexistent"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(songs, many=True)

        return Response(serializer.data)


class SongUserViewSet(viewsets.ModelViewSet):
    serializer_class = SongUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # desactivar paginación para songusers

    def get_queryset(self):
        #if not self.request.user.is_authenticated:
            #return SongUser.objects.none()
        return SongUser.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
