import argparse
import time

import cv2
import dlib
import imutils
import numpy as np
from imutils import face_utils
from imutils.video import FileVideoStream, VideoStream
from scipy.spatial import distance as dist


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])  # vertical distance
    C = dist.euclidean(eye[0], eye[3])  # horizental distance
    ear = (A + B) / (2.0 * C)
    return ear


def blink_count(video_name):
    """
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-p", "--shape-predictor", required=True, help="path to facial landmark predictor"
    )
    ap.add_argument("-v", "--video", type=str, default="", help="path to input video file")
    args = vars(ap.parse_args())
    """
    PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
    VIDEO_PATH=""
    IMAGE_FRAME_PATH=""
    EYE_AR_THRESH = 0.28
    EYE_AR_CONSEC_FRAMES = 3

    COUNTER = 0
    TOTAL = 0

    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    print("[INFO] starting video stream thread...")
    vs = FileVideoStream(video_name).start()
    fileStream = True
    # vs = VideoStream(src=0).start()
    # fileStream = False
    time.sleep(1.0)

    while True:

        if fileStream and not vs.more():
            break

        frame = vs.read()
        if True:
            cv2.imwrite(video_name+".jpg", frame)  # save frame as JPEG file
        frame = imutils.resize(frame, width=800)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 0)

        for rect in rects:
            shape = predictor(gray, rect)

            #  print("[INFO] counbting face...")
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            ear = (leftEAR + rightEAR) / 2.0

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            if ear < EYE_AR_THRESH:
                COUNTER += 1

            else:

                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1

                COUNTER = 0

            cv2.putText(
                frame,
                "Blinks: {}".format(TOTAL),
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )
            cv2.putText(
                frame,
                "EAR: {:.2f}".format(ear),
                (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )

        # cv2.imshow("Frame", frame)
        # key = cv2.waitKey(1) & 0xFF

        # if key == ord("q"):
        # break
        print("[INFO] Total Blink Count...", TOTAL)
        cv2.destroyAllWindows()
        vs.stop()
    return TOTAL


#total = blink_count()
#print("[INFO] Total Blink Count...>>", total)
