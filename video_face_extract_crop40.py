#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import cv2
from mtcnn.mtcnn import MTCNN
detector = MTCNN()
from moviepy.editor import VideoFileClip
import numpy as np

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


def crop_face(imgarray, section, margin=40, size=64):
        img_h, img_w, _ = imgarray.shape
        if section is None:
            section = [0, 0, img_w, img_h]
        (x, y, w, h) = section
        margin = int(min(w,h) * margin / 100)
        x_a = x - margin
        y_a = y - margin
        x_b = x + w + margin
        y_b = y + h + margin
        if x_a < 0:
            x_b = min(x_b - x_a, img_w-1)
            x_a = 0
        if y_a < 0:
            y_b = min(y_b - y_a, img_h-1)
            y_a = 0
        if x_b > img_w:
            x_a = max(x_a - (x_b - img_w), 0)
            x_b = img_w
        if y_b > img_h:
            y_a = max(y_a - (y_b - img_h), 0)
            y_b = img_h
        cropped = imgarray[y_a: y_b, x_a: x_b]
        resized_img = cv2.resize(cropped, (size, size), interpolation=cv2.INTER_AREA)
        resized_img = np.array(resized_img)
        return resized_img


def pipeline(img , frame_num):
    faces = return_bboxes(img)
    print(faces)
    if(len(faces)!=0):
        face_count = 0
        for face in faces:
            sub_img=crop_face(img, face)
            face_count = face_count+1
            cv2.imwrite(str(frame_num) + "_" + str(face_count)+".jpg",sub_img)


def extract_faces(path):
    clip = VideoFileClip(path)
    num_frames = len(list(clip.iter_frames()))
    print(num_frames)
    video_fps = 10.0
    for frame_number in range(num_frames):
        print(frame_number)
        pipeline(clip.get_frame(frame_number / video_fps) , frame_number)


if __name__== "__main__":
    video_path = sys.argv[1]
    print(video_path)
    extract_faces(video_path)
#     draw_bboxes("aa.jpg")
#https://github.com/Zulko/moviepy/issues/702
#https://stackoverflow.com/questions/37622544/get-number-of-frames-in-clip-with-moviepy