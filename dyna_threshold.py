import math
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize

import os
import argparse
import logging

import cv2
import numpy

from blur_detection import estimate_blur
from blur_detection import fix_image_size
from blur_detection import pretty_blur_map
from noise_calc import estimate_noise


class cameras(object):

    def __init__(self, cid, overlapping):
        self.cid = cid
        self.threshold = [0, 0, 0]  # array for threshold values
        self.overlapping = overlapping
        self.crowd_array = [0, 0, 0]
        self.noises = [0, 0, 0]
        self.blurriness = [0,0,0]

    def crowd_density(self, cr_de):
        self.crowd_array[cr_de[0]] = cr_de[1]

    def noise(self, noise_value):
        self.noises[noise_value[0]] = noise_value[1]

    def blur(self,blur_value):
        self.blurriness[blur_value[0]] = blur_value[1]

    def threshold_calc(self):
        weightage = [0.5, 0.3, 1, 0.1]
        count = 0
        for i in self.overlapping:
                #print(i)
            self.threshold[count] = weightage[0] * (1/i)
            count += 1
        count = 0
        for i in self.blurriness:
            self.threshold[count] += weightage[1] * i
            count += 1
        count = 0
        for i in self.crowd_array:
            self.threshold[count] += weightage[2] * (1/i)
            count += 1
        count = 0
        for i in self.noises:
            self.threshold[count] += weightage[3] * i
            count += 1

        [self.threshold] = normalize([self.threshold],norm='l2')
        return self.threshold


print("Enter the input images name for the three cameras")
s1,s2,s3=raw_input().split()

input_image1 = cv2.imread(s1)
input_image2 = cv2.imread(s2)
input_image3 = cv2.imread(s3)


input_image_1 = fix_image_size(input_image1)
blur_map_1, score_1, blurry_1 = estimate_blur(input_image_1)

input_image_2 = fix_image_size(input_image2)
blur_map_2, score_2, blurry_2 = estimate_blur(input_image_2)

input_image_3 = fix_image_size(input_image3)
blur_map_3, score_3, blurry_3 = estimate_blur(input_image_3)

print("Quality_score1: {0}, blurry1: {1}".format(score_1, blurry_1))
print("Quality_score2: {0}, blurry2: {1}".format(score_2, blurry_2))
print("Quality_score3: {0}, blurry3: {1}".format(score_3, blurry_3))


"""    if args.display:
        cv2.imshow("input", input_image1)
        cv2.imshow("result", pretty_blur_map(blur_map))
        cv2.waitKey(0)"""

img_gray = cv2.cvtColor(input_image1, cv2.COLOR_BGR2GRAY)
noise_value_img_1 = estimate_noise(img_gray)

img_gray = cv2.cvtColor(input_image2, cv2.COLOR_BGR2GRAY)
noise_value_img_2 = estimate_noise(img_gray)

img_gray = cv2.cvtColor(input_image3, cv2.COLOR_BGR2GRAY)
noise_value_img_3 = estimate_noise(img_gray)

print("Noise of camera 1 is ", noise_value_img_1)
print("Noise of camera 2 is ", noise_value_img_2)
print("Noise of camera 3 is ", noise_value_img_3)




c1 = cameras(0, [1, 0.3, 0.4])
c2 = cameras(1, [0.3, 1, 0.2])
c3 = cameras(2, [0.4, 0.2, 1])

# crowd density will be calculated from a separate code.These are dummy values

#scalar = StandardScaler(with_mean=False)
#crowd_density_array = [[10], [5], [7]]
crowd_density_array = [[10,5,7]]
#scalar.fit(crowd_density_array)
#crowd_density_array = scalar.transform(crowd_density_array)
#[crowd_density_array] = np.array(crowd_density_array).reshape((1, 3))
[crowd_density_array] = normalize(crowd_density_array,norm='l2')


c1.crowd_density([c1.cid, crowd_density_array[c1.cid]])
c1.crowd_density([c2.cid, crowd_density_array[c2.cid]])
c1.crowd_density([c3.cid, crowd_density_array[c3.cid]])

c2.crowd_density([c2.cid, crowd_density_array[c2.cid]])
c2.crowd_density([c1.cid, crowd_density_array[c1.cid]])
c2.crowd_density([c3.cid, crowd_density_array[c3.cid]])

c3.crowd_density([c3.cid, crowd_density_array[c3.cid]])
c3.crowd_density([c1.cid, crowd_density_array[c1.cid]])
c3.crowd_density([c2.cid, crowd_density_array[c2.cid]])



#scalar = StandardScaler(with_mean=False)
#noise_array = [[noise_value_img_1], [noise_value_img_2], [noise_value_img_3]]
noise_array = [[noise_value_img_1, noise_value_img_2, noise_value_img_3]]
#scalar.fit(noise_array)
#noise_array = scalar.transform(noise_array)
#[noise_array] = np.array(noise_array).reshape((1, 3))
[noise_array] = normalize(noise_array,norm='l2')


c1.noise([c1.cid, noise_array[c1.cid]])
c1.noise([c2.cid, noise_array[c2.cid]])
c1.noise([c3.cid, noise_array[c3.cid]])

c2.noise([c1.cid, noise_array[c1.cid]])
c2.noise([c2.cid, noise_array[c2.cid]])
c2.noise([c3.cid, noise_array[c3.cid]])

c3.noise([c1.cid, noise_array[c1.cid]])
c3.noise([c2.cid, noise_array[c2.cid]])
c3.noise([c3.cid, noise_array[c3.cid]])



#scalar = StandardScaler(with_mean=False)
#blur_array = [[score_1], [score_2], [score_3]]
blur_array = [[score_1, score_2, score_3]]
#scalar.fit(blur_array)
#blur_array = scalar.transform(blur_array)
#[blur_array] = np.array(blur_array).reshape((1, 3))
[blur_array] = normalize(blur_array,norm='l2')


c1.blur([c1.cid, blur_array[c1.cid]])
c1.blur([c2.cid, blur_array[c2.cid]])
c1.blur([c3.cid, blur_array[c3.cid]])

c2.blur([c2.cid, blur_array[c2.cid]])
c2.blur([c1.cid, blur_array[c1.cid]])
c2.blur([c3.cid, blur_array[c3.cid]])

c3.blur([c3.cid, blur_array[c3.cid]])
c3.blur([c1.cid, blur_array[c1.cid]])
c3.blur([c2.cid, blur_array[c2.cid]])

thresh_c1 = c1.threshold_calc()
thresh_c2 = c2.threshold_calc()
thresh_c3 = c3.threshold_calc()

print("Threshold of cameras w.r.t to Camera1 is ", thresh_c1)
print("Threshold of cameras w.r.t to Camera2 is ", thresh_c2)
print("Threshold of cameras w.r.t to Camera3 is ", thresh_c3)