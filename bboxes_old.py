#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
from mtcnn.mtcnn import MTCNN
detector = MTCNN()
from moviepy.editor import VideoFileClip

def draw_bboxes(img_path):
    image = cv2.imread(img_path)
    result = detector.detect_faces(image)
    for face in range(len(result)):
        bounding_box = result[face]
        cv2.rectangle(image,(bounding_box[0]-10, bounding_box[1]-10),
              (bounding_box[0]+bounding_box[2]+10, bounding_box[1] + bounding_box[3]+10),(0,155,255),2)
        cv2.imwrite("drawn"+img_path, image)
    print(result)
    
def return_bboxes_(img_path):
    image = cv2.imread(img_path)
    result = detector.detect_faces(image)
    return result

def return_bboxes(img):
    result = detector.detect_faces(image)
    return result

def pipeline(img):
    print(1)
    faces = return_bboxes(img)
    print(faces)
    for x,y,w,h in faces:
        sub_img=image[y-10:y+h+10,x-10:x+w+10]
        i = i+1
        cv2.imwrite(str(i)+".jpg",sub_img)

def extract_faces(path):
    global i
    i = 0
    clip = VideoFileClip(path)
    clip.fl_image(pipeline)

if __name__== "__main__":
    extract_faces("./video5.mp4")
#     draw_bboxes("aa.jpg")