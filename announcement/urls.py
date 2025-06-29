from django.urls import path
from .views import AnnouncementsView, AnnouncementView, LatestAnnouncementView

urlpatterns = [
    path('announcements', AnnouncementsView.as_view(), name='announcements'),
    path('announcement/<int:pk>', AnnouncementView.as_view(), name='announcement'),
    path('latest', LatestAnnouncementView.as_view(), name='latest-announcement'),
]
