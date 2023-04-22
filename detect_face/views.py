from django.http.response import StreamingHttpResponse, HttpResponse
# from .camera import VideoCamera, gen


def detect_face(request):
    return HttpResponse("test abc")
    # return StreamingHttpResponse (
    #     gen(VideoCamera()), 
    #     content_type='multipart/x-mixed-replace; boundary=frame'
    # )

