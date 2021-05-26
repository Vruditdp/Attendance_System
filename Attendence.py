import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

now2 = datetime.now()
dString2 = now2.strftime('%d-%m-%y')
print(dString2,type(dString2),"gooooood")

path ='ImagesAttendence'
images=[]
classNames=[]
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    # curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

# refDate = datetime.now()
# toDate = refDate.date()
#b=int(refDate.strftime('%d%m%y'))

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        datelist=[]
        flist=[]
        names=[]
        extra="Success"
        for line in myDataList[1:]:
            entry2 = line.split(',')
            datelist.append(entry2[2])
            names.append(entry2[0])
        print(datelist,len(datelist))
        print(names,len(names))
        for e in range (len(datelist)):
            if datelist[e] == dString2:
                flist.append(names[e])
                print("if statement run...")

            # print(datelist[e],type(datelist[e]))
            print('////////////////////')
            print(flist,"is it okk")

        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in flist:
        # if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            dString = now.strftime('%d-%m-%y')
            # dString = now.strftime('%d %B %Y')
            f.writelines(f'\n{name},{dtString},{dString},{extra}')


encodeListknown = findEncodings(images)
print(len(encodeListknown))
print('Encoding is Completed...')
i=0
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
# cap = cv2.VideoCapture(2)
# cap = cv2.VideoCapture(1,cv2.CAP_MSMF)
# cap=cv2.VideoCapture(0,)
while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    print(imgS.shape)

    # imgS=cv2.resize(img,(0,0),None,0.25,0.25,None)
    # imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)


    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)


    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListknown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListknown,encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name=classNames[matchIndex].upper()
            i = i + 1
            print(i,name)
            y1,x2,y2,x1=faceLoc
            y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),2)
            markAttendance(name)

    cv2.imshow('Webcam',img)
    cv2.waitKey(1)






# faceLoc = face_recognition.face_locations(imgElon)[0]
# encodeElon = face_recognition.face_encodings(imgElon)[0]
# cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
#
# faceLocTest = face_recognition.face_locations(imgTest)[0]
# encodeTest = face_recognition.face_encodings(imgTest)[0]
# cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)
#
# results = face_recognition.compare_faces([encodeElon],encodeTest)
# faceDis = face_recognition.face_distance([encodeElon],encodeTest)