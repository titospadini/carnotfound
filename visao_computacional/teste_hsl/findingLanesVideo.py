# -*- coding: utf-8 -*-
# =============================================================
#
#                       -- ROBOCAR --
#
# TIME: CarNotFound
# CARRO: 404
#
# =============================================================

import numpy as np
import cv2
import helper

#carrega o vídeo na varíavel
video = cv2.VideoCapture("solidWhiteRight.mp4")

while True:

    ret, frame = video.read()

    #chama a função que encapsula todo o processo
    #necessário para gerar as linhas nas bordas
    final_frame = helper.pipeline(frame)

    cv2.imshow('frame',final_frame)


    if not ret:
        video = cv2.VideoCapture("nissan.mp4")
        continue


    key = cv2.waitKey(25)
    if key == 27:
        break



video.release()
cv2.destroyAllWindows()