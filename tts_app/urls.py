from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import TTSApiView

urlpatterns = [
    path('api/tts/', TTSApiView.as_view(), name='tts_api'),
    # path('api/tts/<int:mp3_id>/', TTSApiView.as_view(), name='tts_api_mp3'),
    path('api/tts/<int:mp3_id>/', TTSApiView.as_view(), name='tts_api_mp3'),

]