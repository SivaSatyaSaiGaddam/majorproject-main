from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.base import ContentFile
import base64
import cv2 as cv
import io
import face_recognition
import numpy as np
import json


# Create your views here.
def home(request):
    return render(request,"home.html")

def register(request):
    return render(request,"register.html")

def attendance(request):
    return render(request,"attendance.html")

def show(request):
    return render(request,"show.html")

def registerface(request):
    user={'submit':False}
    if request.method=='POST':
        user['submit']=True
        user["name"]=request.POST['name']
        user["rollno"]=request.POST['rollno']
        image_data = request.POST.get("image-data")
        image_data=image_data.split(',')[1]
        decoded_image = base64.b64decode(image_data)
        # convert the raw data to a numpy array
        image = np.frombuffer(decoded_image, np.uint8)
        # convert the numpy array to a cv2 image
        cv_img = cv.imdecode(image, cv.IMREAD_COLOR)
        print(cv_img.shape)
        fr_img=cv.cvtColor(cv_img,cv.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(fr_img,number_of_times_to_upsample=2)
        face_encoding=face_recognition.face_encodings(fr_img,face_locations)
        flipped_cv_img=cv.flip(cv_img,1)
        if face_encoding:
            a=face_encoding[0]
            print(a)
            user['saved']=True
            return render(request,'user_added.html',{'user':user})
        else:
            user['saved']=False
            return render(request,'registerface.html',{'user':user})
            
    else:
        return render(request,'registerface.html',{'user':user})