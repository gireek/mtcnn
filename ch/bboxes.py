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
    result = detector.detect_faces(img)
    return result

def pipeline(img , frame_num):
    faces = return_bboxes(img)
    print(faces)
#     if(len(faces)==0):
#         return 0
    if(len(faces)!=0):
        face_count = 0
        for x,y,w,h in faces:
            sub_img=img[y-10:y+h+10,x-10:x+w+10]
            face_count = face_count+1
            cv2.imwrite(str(frame_num) + "_" + str(face_count)+".jpg",sub_img)
#         return 1

def extract_faces(path):
    clip = VideoFileClip(path)
#     clip.fl_image(pipeline)
    num_frames = len(list(clip.iter_frames()))
    print(num_frames)
    video_fps = 10.0
    for frame_number in range(num_frames):
        print(frame_number)
        pipeline(clip.get_frame(frame_number / video_fps) , frame_number)

if __name__== "__main__":
    extract_faces("./video5.mp4")
#     draw_bboxes("aa.jpg")
#https://github.com/Zulko/moviepy/issues/702
#https://stackoverflow.com/questions/37622544/get-number-of-frames-in-clip-with-moviepy
