import os
import numpy
import pandas as pd


def read_file(file_path, read_method, city, splitby=",", max_lines=1e9, list=False):
    """
    :param file_path:
    :param read_method: advice "rb"
    :param splitby: "," [default]
    :param max_lines: to control the max size
    :return: a DataFrame
    """
    if city == "haikou":
        splitby = " "
    f = open(file_path, read_method)
    s = []
    for i, lines in enumerate(f):
        if i > max_lines:
            break
        lines = str(lines)
        flag = 1
        l = lines.split(splitby)
        l[-1] = l[-1][:-3]
        if city == "haikou":
            l = l[-4:]
        for i in range(len(l)):
            if city == "chengdu" and i == 0:
                continue
            if "." not in l[i]:
                l[i] = int(l[i])
                if(l[i] == 0):
                    flag = 0
            else:
                l[i] = float(l[i])
                if (l[i] == 0.0):
                    flag = 0
        if flag == 1:
            s.append(l)
    f.close()

    if list == True:
        return s

    data = pd.DataFrame(s)
    assert data.shape[1] == 8 or 4
    if city == "chengdu":
        data.rename(columns={0: "OrderID", 1: "Stime", 2: "Etime", 3: "LonPick", 4: "LatPick",
                             5:"LonDrop", 6:"LatDrop", 7:"Rwd"}, inplace=True)
    elif city == "haikou":
        data.rename(columns={0: "LonDrop", 1: "LatDrop", 2:"LonPick", 3:"LatPick"}, inplace=True)
    print("read successfully!")
    return data


def dis_earth(lat1, long1, lat2, long2):
    tmp = np.sin(lat1 / 180 * np.pi) * np.sin(lat2 / 180 * np.pi) + \
          np.cos(lat1 / 180 * np.pi) * np.cos(lat2 / 180 * np.pi) * np.cos((long1 - long2) / 180 * np.pi)
    return 6371 * np.arccos(tmp)

def plant_extract(l, r, t1, t2):
    ep1 = (r - l) * t1
    ep2 = (r - l) * t2
    l = l + ep1
    r = r - ep2
    return l, r
