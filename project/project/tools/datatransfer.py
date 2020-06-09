# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 22:16:00 2020

@author: biany
"""

import numpy as np


class location_split:
    def __init__(self, locations, orders):
        self.locations = locations
        self.orders = orders
        self.new_locations = []
        self.new_orders = []

    def split(self, split_func):
        # split_func is a function which input location + order,
        # output two lists after split
        new_locations = [self.locations[0]]
        new_orders = [0]
        for i in range(1, len(self.locations)):
            new_locations_tmp, new_orders_tmp = split_func(self.locations[i], self.orders[i])
            new_locations = new_locations + new_locations_tmp
            new_orders = new_orders + new_orders_tmp

        self.new_locations = new_locations
        self.new_orders = new_orders

        return new_locations, new_orders

    def origin_data(self):
        return self.locations, self.orders

    def new_data(self):
        return self.new_locations, self.new_orders


def all_split(location, order):
    tmp1 = []
    tmp2 = []
    for i in range(order):
        tmp1 = tmp1 + [location]
        tmp2 = tmp2 + [1]

    return tmp1, tmp2


def split_per_v_gen(order_num):
    # generate functions which split each location to have order_num orders
    def split_per_v(location, order):
        # location is the location of vertex, order is total amount of orders in the location
        tmp1 = []
        tmp2 = []
        for i in range(order // order_num):
            tmp1.append(location)
            tmp2.append(order_num)

        rem = order % order_num;
        if (rem == 0):
            return tmp1, tmp2
        else:
            tmp1.append(location)
            tmp2.append(rem)
            return tmp1, tmp2

    return split_per_v


def split_many_gen(fst_ord, fst_ratio, snd_ord, snd_ratio, trd_ord):
    # split orders into three amount: fst_ord, snd_ord, trd_ord
    # fst_ratio * orders be converted to locations with fst_ord number of orders
    # snd_ratio * orders be converted to locations with snd_ord number of orders
    def split_many(location, order):
        new_loc = []
        new_ord = []
        fst_amount = int(order * fst_ratio)
        fst_loc_l, fst_ord_l = split_per_v_gen(fst_ord)(location, fst_amount)

        snd_amount = int(order * snd_ratio)
        snd_loc_l, snd_ord_l = split_per_v_gen(snd_ord)(location, snd_amount)

        trd_amount = order - fst_amount - snd_amount
        trd_loc_l, trd_ord_l = split_per_v_gen(trd_ord)(location, trd_amount)

        new_loc = fst_loc_l + snd_loc_l + trd_loc_l
        new_ord = fst_ord_l + snd_ord_l + trd_ord_l

        return new_loc, new_ord

    return split_many


def split_rand_gen(mean_ord):
    # mean number of order, else, random !
    def split_rand(location, order):
        new_loc = []
        new_ord = []

        num_split = order // mean_ord - 1
        rand_array = np.random.rand(num_split)
        rand_array = np.sort(rand_array)
        # print("rand_array:", rand_array)
        previous = 0

        for i, place in enumerate(rand_array):
            if (previous >= order):
                break

            new_loc.append(location)
            tmp = previous
            if (place * order - previous >= 1):
                previous = int(place * order)
            else:
                previous = 1 + previous

            new_ord.append(previous - tmp)

        if (order - previous >= 1):
            new_loc.append(location)
            tmp = order - previous
            new_ord.append(tmp)

        return new_loc, new_ord

    return split_rand


'''
def split_rand2_gen(mean_ord, var):
    # mean number of order and variance, else, random !
    def split_rand(location, order):
        new_loc = []
        new_ord = []

        num_split = order // mean_ord - 1
        rand_array = np.random.randn(3 * num_split)
        rand_array = rand_array + mean_ord
        print("rand_array:", rand_array)
        previous = 0

        for i, place in enumerate(rand_array): 
            new_loc.append(location)
            tmp = previous
            if (place * order - previous >= 1):
                previous = int(place * order)
            else:
                previous = 1 + previous

            new_ord.append(previous - tmp)

        if (order - previous >= 1) :
            new_loc.append(location)
            tmp = order - previous
            new_ord.append(tmp)

        return new_loc, new_ord

    return split_rand
'''

if __name__ == '__main__':
    locations = [(2, 3), (3, 7), (5, 5), (0, 8), (1, 1)]
    orders = [0, 25, 25, 25, 25]
    loc_spl = location_split(locations, orders)

    print(loc_spl.split(all_split))

    # new vertices mainly has ten orders
    split_ten = split_per_v_gen(10)
    print(loc_spl.split(split_ten))

    split_four = split_per_v_gen(4)
    print(loc_spl.split(split_four))

    split_many = split_many_gen(1, 0.2, 2, 0.2, 3)
    print(loc_spl.split(split_many))

    split_rand = split_rand_gen(5)
    print(loc_spl.split(split_rand))