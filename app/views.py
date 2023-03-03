from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.base import ContentFile
import base64
import cv2 as cv
import io
import face_recognition
import numpy as np
import json
from .models import Student,Attendance,Section
from datetime import date,time,datetime
from django.utils import timezone


# Create your views here.
def home(request):
    return render(request,"home.html")

def register(request):
    return render(request,"register.html")

def attendance(request):
    arr=[]
    if request.method=='POST':
        image_data = request.POST.get("image-data")
        image_data=image_data.split(',')[1]
        decoded_image = base64.b64decode(image_data)
        # convert the raw data to a numpy array
        image = np.frombuffer(decoded_image, np.uint8)
        # convert the numpy array to a cv2 image
        cv_img = cv.imdecode(image, cv.IMREAD_COLOR)
        print(cv_img.shape)
        fr_img=cv.cvtColor(cv_img,cv.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(fr_img,number_of_times_to_upsample=1,model="hog")
        print(face_locations)
        face_encoding=face_recognition.face_encodings(fr_img,face_locations,num_jitters=10,model="large")
        print(len(face_encoding))
        
        if face_encoding:
            arr=[]
            
            for encoding in face_encoding:
                
                for face in Student.objects.all():
                    f=np.asarray(list(json.loads(face.encoding)),dtype=np.float64)
                    print(f)
                    np.set_printoptions(precision=20)
                    m=face_recognition.compare_faces(known_face_encodings=[encoding],face_encoding_to_check=f,tolerance=0.4)
                    if m[0]:
                        now=datetime.now()
                        a=Attendance.objects.filter(date=now.strftime("%Y-%m-%d")).get(rollno=face)
                        if a:
                            a.time_out=now.strftime("%H:%M:%S")
                            a.save()
                        else:
                            Attendance.objects.create(rollno=face,time_in=now.strftime("%H:%M:%S"),time_out=now.strftime("%H:%M:%S"),date=now.strftime("%Y-%m-%d"))

                        arr.append(face.name)
                        break
            print(arr)
            return render(request,'attendance.html',{'list':arr,'detected':True,'captured':True})
        
        else:
            return render(request,'attendance.html',{'detected':False,'captured':True})
    return render(request,'attendance.html',{'captured':False,'detected':False,'attendance':arr})
    

def show(request):
    attended=Attendance.objects.filter(date=datetime.now().strftime("%Y-%m-%d"))
    a=set()
    for i in attended:
        a.add(i.rollno.rollno)
    absent_students = Student.objects.exclude(rollno__in=a)
    print(absent_students)
    return render(request,"show.html",{'attendance':attended,"section":Section.objects.all(),"absentees":absent_students})

def registerface(request):
    user={'submit':False}
    if request.method=='POST':
        user['submit']=True
        user["name"]=request.POST['name']
        user["rollno"]=request.POST['rollno']
        if Student.objects.filter(rollno=request.POST['rollno']):
            user['exists']=True
            return render(request,'registerface.html',{'user':user})
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
        face_encoding=face_recognition.face_encodings(fr_img,face_locations,model="large",num_jitters=10)
        flipped_cv_img=cv.flip(cv_img,1)
        if face_encoding:
            a=face_encoding[0]
            print(a)
            user['saved']=True
            Student.objects.create(name=request.POST['name'],rollno=request.POST['rollno'],section=request.POST['section'],email=request.POST['email'],phoneno=str(request.POST['number']),encoding=json.dumps(list(a)))
            rows = Section.objects.filter(section=request.POST['section'])
            if rows.exists():
                row = rows.first()
                row.count=row.count+1
                row.save
            else:
                Section.objects.create(section=request.POST['section'],count=1)
            return render(request,'user_added.html',{'user':user})
        else:
            user['saved']=False
            return render(request,'registerface.html',{'user':user})
            
    else:
        return render(request,'registerface.html',{'user':user})