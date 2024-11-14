import os
import re
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import yt_dlp

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def download_video(request):
    if request.method == 'POST':
        url = request.POST.get('url', None)
        if url:
            try:
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': '/tmp/%(title)s.%(ext)s',
                    'noprogress': True,  # To reduce verbosity
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    video_title = info_dict.get('title', None)
                    video_ext = info_dict.get('ext', None)
                    filename = ydl.prepare_filename(info_dict).replace('.webm', f'.{video_ext}')  # Adjust if needed

                print(f"Downloaded file: {filename}")

                # Ensure the file is properly closed before accessing it
                with open(filename, 'rb') as file:
                    file_data = file.read()

                if os.path.exists(filename):
                    response = HttpResponse(file_data, content_type='application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename={os.path.basename(filename)}'
                    os.remove(filename)
                    return response
                else:
                    raise FileNotFoundError(f"No such file: '{filename}'")
            except Exception as e:
                print(f"An error occurred: {e}")
                return JsonResponse({"message": f"An error occurred: {e}"}, status=500)
        return JsonResponse({"message": "Invalid URL"}, status=400)
    return JsonResponse({"message": "Invalid request method"}, status=400)
