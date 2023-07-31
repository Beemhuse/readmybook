# from django.http import JsonResponse
# from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser
import base64

from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse
# from pydub.pyaudioop import reverse

from .tts_app import read_text_from_file, read_pdf_content, text_to_speech
#
# class TTSApiView(APIView):
#     parser_classes = [MultiPartParser]
#
#     def post(self, request, format=None):
#         if 'file' not in request.data:
#             return JsonResponse({'error': 'No file part in the request.'}, status=400)
#
#         uploaded_file = request.data['file']
#         file_content = uploaded_file.read()
#
#         if uploaded_file.name.endswith('.txt'):
#             text_content = file_content.decode('utf-8')
#         elif uploaded_file.name.endswith('.pdf'):
#             text_content = read_pdf_content(file_content)
#         else:
#             return JsonResponse({'error': 'Unsupported file format.'}, status=400)
#
#         if text_content:
#             voice_id = 1  # Change this to the index of the desired voice
#             output_file = "output.mp3"  # Change the output file name if needed
#             text_to_speech(text_content, output_file)
#
#             mp3_url = request.build_absolute_uri(output_file)
#
#             return JsonResponse({'mp3_url': mp3_url})
#
#         return JsonResponse({'error': 'No content in the file or an error occurred while reading.'}, status=400)



# tts_app/views.py

import io
import pyttsx3
# import fitz
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models  import MP3File
# from tts_app.models import MP3File

# from tts_project.tts_app.tts_app import text_to_speech, read_pdf_content


class TTSApiView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        if 'file' not in request.data:
            return Response({'error': 'No file part in the request.'}, status=400)

        uploaded_file = request.data['file']
        file_content = uploaded_file.read()

        if uploaded_file.name.endswith('.txt'):
            text_content = file_content.decode('utf-8')
        elif uploaded_file.name.endswith('.pdf'):
            text_content = read_pdf_content(file_content)
            if text_content is None:
                return Response({'error': 'Error: Unable to extract text from the PDF.'}, status=400)
        else:
            return Response({'error': 'Unsupported file format.'}, status=400)

        if text_content:
            mp3_data = text_to_speech(text_content)
            if mp3_data:
                # Encode the MP3 data as base64
                encoded_mp3_data = base64.b64encode(mp3_data).decode('utf-8')

                return JsonResponse({'mp3_data': encoded_mp3_data}, status=201)
                # return JsonResponse({'mp3_url': request.build_absolute_uri(reverse('tts_api_mp3', args=[mp3_file.pk]))},
                #                     status=201)
            # if mp3_data:
            #     mp3_file = MP3File.objects.create(content=mp3_data)
            #     return JsonResponse({'mp3_url': request.build_absolute_uri(reverse('tts_api_mp3', args=[mp3_file.pk]))},
            #                         status=201)
                # return Response({'mp3_id': mp3_file.pk}, status=201)
            else:
                return Response({'error': 'Error occurred during text-to-speech.'}, status=500)
        else:
            return Response({'error': 'No content in the file or an error occurred while reading.'}, status=400)

    def get(self, request, mp3_id, format=None):
        try:
            mp3_file = MP3File.objects.get(pk=mp3_id)
            return HttpResponse(mp3_file.content, content_type='audio/mpeg')
        except MP3File.DoesNotExist:
            return Response({'error': 'MP3 file not found.'}, status=404)