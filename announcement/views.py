from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Announcement
from .serializers import AnnouncementSerializer
from django.core.files.base import ContentFile
from django.utils.timezone import now
import base64

# Create your views here.


class AnnouncementsView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        announcements = Announcement.objects.all().order_by('-created_at')
        return Response(AnnouncementSerializer(announcements, many=True).data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        if (not self.request.user.is_superuser):
            return Response('You are not the owner', status=status.HTTP_403_FORBIDDEN)
        
        title = request.data.get('title')
        content = request.data.get('content', '')
        img = request.data.get('img')
        if not title:
            return Response('Title is required', status=status.HTTP_400_BAD_REQUEST)

        announcement = Announcement(title=title, content=content)
        if (img):
            announcement.image.save('image.jpg', ContentFile(base64.b64decode(img)))
        announcement.save()
        return Response('Successfully created announcement', status=status.HTTP_201_CREATED)
    

class AnnouncementView(GenericAPIView):
    permmission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request: Request, pk: int) -> Response:
        title = request.data.get('title', '')
        content = request.data.get('content', '')
        img = request.data.get('img')

        try:
            announcement = Announcement.objects.get(pk=pk)
        except Announcement.DoesNotExist:
            return Response('Announcement not found', status=status.HTTP_404_NOT_FOUND)
        
        if (title):
            announcement.title = title
            announcement.updated_at = now()
        if (content):
            announcement.content = content
            announcement.updated_at = now()
        if (img):
            announcement.image.save('image.jpg', ContentFile(base64.b64decode(img)))
            announcement.updated_at = now()

        announcement.save()
        return Response('Successfully updated announcement', status=status.HTTP_200_OK)

    def delete(self, request: Request, pk: int) -> Response:
        try:
            announcement = Announcement.objects.get(pk=pk)
        except Announcement.DoesNotExist:
            return Response('Announcement not found', status=status.HTTP_404_NOT_FOUND)
        
        announcement.delete()
        return Response('Successfully deleted announcement', status=status.HTTP_204_NO_CONTENT)


class LatestAnnouncementView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        try:
            announcement = Announcement.objects.latest('updated_at')
        except Announcement.DoesNotExist:
            return Response('No announcements found')
        
        return Response(AnnouncementSerializer(announcement).data, status=status.HTTP_200_OK)
