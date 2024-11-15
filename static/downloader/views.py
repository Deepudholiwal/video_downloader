import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import yt_dlp

def index(request):
    return render(request, 'index.html')  # Render your main page

@csrf_exempt
def download_video(request):
    if request.method == 'POST':
        url = request.POST.get('url', None)
        if not url:
            return JsonResponse({"message": "Please provide a valid URL!"}, status=400)

        try:
            # Set options for yt-dlp
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to downloads folder
                'noplaylist': True,  # Download only single video
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',  # Convert to mp4
                    'preferedformat': 'mp4',
                }],
            }

            # Create downloads directory if it doesn't exist
            if not os.path.exists('downloads'):
                os.makedirs('downloads')

            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Assuming the video is downloaded successfully, return a success response
            return JsonResponse({"message": "Download completed!"}, status=200)

        except yt_dlp.utils.DownloadError as e:
            return JsonResponse({"message": f"Download error: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"message": f"An unexpected error occurred: {str(e)}"}, status=500)

    return JsonResponse({"message": "Invalid request method. Use POST."}, status=405)