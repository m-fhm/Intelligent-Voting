from django.http.response import StreamingHttpResponse,HttpResponse
from .camera import MaskDetect, gen


def detect_mask(request):
    return StreamingHttpResponse (
        gen(MaskDetect()), 
        content_type='multipart/x-mixed-replace; boundary=frame'
    )