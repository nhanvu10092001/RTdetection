from django.shortcuts import render
from django.http import HttpResponse
#from django.view.decorator import gzip
from django.http import StreamingHttpResponse

import cv2
import threading
from ultralytics import YOLO    


def index(request):
    
    return render(request, 'home.html')
def contact(request):
    return render(request, 'contact.html')

# def streamvideo(request):
#     try:
#         return StreamingHttpResponse(gen(videocapture()), content_type="multipart/x-mixed-replace;boundary=frame")
#     except Exception as err:
#          # This is bad! replace it with proper handling
#         print(err)
#     return render(request, 'home.html')
# class videocapture(object):
#     def __init__(self) -> None:
#         self.cap = cv2.VideoCapture(0)
#         while self.cap.isOpened():
#             self.success, self.frame = self.cap.read()
#             threading.Thread(target=self.update, args=()).start()
#     def __del__(self):
#         self.cap.release()
#     def get_frame(self):
#         image = self.frame
#         ret, im = cv2.imencode(".jpg", image)
#         return im
#     def update(self):
#         while True:
#             (self.success, self.frame) = self.cap.read()
# def gen(camera):
#     model = YOLO("C:/Users/asus/project/best.pt")
#     while True:
#         frame = camera.get_frame()
#         results = model(frame)
#         annotated_frame = results[0].plot()
#         ret, im = cv2.imencode('.jpg', annotated_frame)
#         im = im.tobytes()
#         yield(b'--frame\r\n'
#               b'Content-Type: image/jpeg\r\n\r\n' + im + b'\r\n\r\n')

model = YOLO("C:/Users/asus/project/best.pt")
def Home(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'app1.html')

#to capture video class
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        
        results = model(image)
        annotated_frame = results[0].plot()
        _, jpeg = cv2.imencode('.jpg', annotated_frame)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# Create your views here.
