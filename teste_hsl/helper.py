# -*- coding: utf-8 -*-
import numpy as np
import cv2

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)

    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    cv2.fillPoly(mask, vertices, ignore_mask_color)

    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=(0, 255, 0), thickness=5):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_img = np.zeros(img.shape, dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img


def weighted_img(img, initial_img, alpha=0.8, beta=1., phi=0.):
    return cv2.addWeighted(initial_img, alpha, img, beta, phi)


def isolate_white(img):
    hsl = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    # define range of white color in HSV
    # change it according to your need !
    lower_white = np.array([0, 210, 0], dtype=np.uint8)
    upper_white = np.array([255, 235, 255], dtype=np.uint8)

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsl, lower_white, upper_white)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img, img, mask=mask)
    return res


def separate_lines(lines):
    """ Takes an array of hough lines and separates them by +/- slope.
        The y-axis is inverted in matplotlib, so the calculated positive slopes will be right
        lane lines and negative slopes will be left lanes. """
    right = []
    left = []
    for x1, y1, x2, y2 in lines[:, 0]:
        if x2-x1!=0:
            m = (float(y2) - y1) / (x2 - x1)
        if m >= 0:
            right.append([x1, y1, x2, y2, m])
        else:
            left.append([x1, y1, x2, y2, m])

    return right, left


def extend_point(x1, y1, x2, y2, length):
    """ Takes line endpoints and extroplates new endpoint by a specfic length"""
    line_len = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    x = x2 + (x2 - x1) / line_len * length
    y = y2 + (y2 - y1) / line_len * length
    return x, y


def reject_outliers(data, cutoff, thresh=0.08):
    """Reduces jitter by rejecting lines based on a hard cutoff range and outlier slope """
    data = np.array(data)
    print(data)
    data = data[(data[:, 4] >= cutoff[0]) & (data[:, 4] <= cutoff[1])]
    m = np.mean(data[:, 4], axis=0)
    return data[(data[:, 4] <= m + thresh) & (data[:, 4] >= m - thresh)]


def merge_lines(lines):
    """Merges all Hough lines by the mean of each endpoint,
       then extends them off across the image"""

    lines = np.array(lines)[:, :4]  ## Drop last column (slope)

    x1, y1, x2, y2 = np.mean(lines, axis=0)
    x1e, y1e = extend_point(x1, y1, x2, y2, -1000)  # bottom point
    x2e, y2e = extend_point(x1, y1, x2, y2, 1000)  # top point
    line = np.array([[x1e, y1e, x2e, y2e]])

    return np.array([line], dtype=np.int32)

def merge_prev(line, prev):
    """ Extra Challenge: Reduces jitter and missed lines by averaging previous
        frame line with current frame line. """
    if prev != None:
        line = np.concatenate((line[0], prev[0]))
        x1,y1,x2,y2 = np.mean(line, axis=0)
        line = np.array([[[x1,y1,x2,y2]]], dtype=np.int32)
        return line
    else:
        return line


#função para achar as linhas na imagem/frame
def pipeline(image):
    ###roi nissan.mp4
    #bot_left = [-550, 660]
    #bot_right = [2000, 660]
    #apex_right = [925, 260]
    #apex_left = [380, 260]

    #"region of interest" para o vídeo "solidWhiteRight.mp4"
    #aqui estou pegando os pontos dos vértices do polígono
    bot_left = [80, 540]
    bot_right = [980, 540]
    apex_right = [510, 315]
    apex_left = [450, 315]

    #a variável guarda os pontos do vértice do polígono
    v = [np.array([bot_left, bot_right, apex_right, apex_left], dtype=np.int32)]
    #
    roi = region_of_interest(image, v)


    binaryImage = isolate_white(roi)
    edges = cv2.Canny(binaryImage, 100, 200)

    lines = cv2.HoughLinesP(edges, 0.5, np.pi / 180, 10, np.array([]), minLineLength=90, maxLineGap=200)
    if lines is not None:
        draw_lines(image, lines)


    #cv2.imshow('frame', binaryImage)
    #cv2.imshow('edges', edges)

    return image