# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 11:56:58 2020

@author: biany
"""
import numpy as np

def haversin(theta):
    return np.sin(theta/2) * np.sin(theta/2)


def sphere_dis(long1, lat1, long2, lat2):
    long1_rad = long1 / 180 * np.pi
    lat1_rad = lat1 / 180 * np.pi
    long2_rad = long2 / 180 * np.pi
    lat2_rad = lat2 / 180 * np.pi
    
    tmp = haversin(lat1_rad - lat2_rad) +\
        np.cos(lat1_rad) * np.cos(lat2_rad) * haversin(long1_rad - long2_rad)
    
    return 2 * 6371 * np.arcsin(np.sqrt(tmp))


def dis_earth(long1, lat1, long2, lat2):
    tmp = np.sin(lat1 / 180 * np.pi) * np.sin(lat2 / 180 * np.pi) + \
          np.cos(lat1 / 180 * np.pi) * np.cos(lat2 / 180 * np.pi) * np.cos((long1 - long2) / 180 * np.pi)
    if tmp > 1:
        tmp = 1
    return 6371 * np.arccos(tmp)


if __name__ == '__main__':
    locations = [(105, 88), (101, 64), (105.1, 88.2), (105.2, 88.3), (105.2, 88.3), (105.21, 88.31)]
    for i in range(len(locations) - 1):
        print(sphere_dis(locations[i][0], locations[i][1], locations[i+1][0], locations[i+1][1]))
        print(dis_earth(locations[i][0], locations[i][1], locations[i+1][0], locations[i+1][1]))
    
    