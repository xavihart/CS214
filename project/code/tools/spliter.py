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
    # all split into one order per location, the same as split_per_v_gen(1)
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
    # control mean number of order, all others are random
    def split_rand(location, order):
        new_loc = []
        new_ord = []

        num_split = max(order // mean_ord - 1, 0)
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


def split_rand2_gen(mean_ord, var):
    # mean number of order and variance, else, random !
    # compared to the previous function, you can control the variance now !
    # The usage is the same
    def split_rand(location, order):
        new_loc = []
        new_ord = []

        num_split = max(order // mean_ord, 1)
        rand_array = np.random.randn(3 * num_split)
        rand_array = rand_array * np.sqrt(var)
        rand_array = rand_array + mean_ord
        # print("rand_array:", rand_array)
        previous = 0

        for i, ord_n in enumerate(rand_array):
            rem = order - previous
            if (rem == 0):
                break

            if (ord_n >= 1):
                previous += min(int(ord_n), rem)
                new_loc.append(location)
                new_ord.append(min(int(ord_n), rem))
            else:
                previous += 1
                new_loc.append(location)
                new_ord.append(1)

        return new_loc, new_ord

    return split_rand


if __name__ == '__main__':
    '''
    locations = [(2,3),(3,7),(5,5),(0,8),(1,1)]
    orders = [0,25,25,25,25]

    # initialize the class
    loc_spl = location_split(locations, orders)

    print(loc_spl.split(all_split))

    # new vertices mainly has ten orders
    split_ten = split_per_v_gen(10)
    print(loc_spl.split(split_ten))

    #  new vertices mainly has 4 orders
    split_four = split_per_v_gen(4)
    print(loc_spl.split(split_four))

    # The orders are split into 20% 1-order, 30% 2-order, the rest are 3-order
    split_many = split_many_gen(1, 0.2, 2, 0.3, 3)
    print(loc_spl.split(split_many))

    # The mean of orders per location is 5, the concrete value is random
    split_rand = split_rand_gen(5)
    print(loc_spl.split(split_rand))

    # mean is 5, variance is 1
    split_rand = split_rand2_gen(5, 1)
    print(loc_spl.split(split_rand))
    '''
    locations = [(0, 0), (110.327905, 20.01876), (110.30977, 20.01876), (110.34604, 20.01876),
                 (110.327905, 19.9889589999999), (110.34604, 19.9889589999999), (110.327905, 19.959158),
                 (110.30977, 19.9889589999999), (110.364175, 19.9889589999999), (110.291635, 19.9889589999999),
                 (110.2735, 19.9889589999999), (110.327905, 20.048561), (110.364175, 20.01876), (110.45485, 19.929357),
                 (110.30977, 20.048561), (110.2735, 19.959158), (110.2735, 20.01876), (110.509255, 19.959158),
                 (110.30977, 19.959158), (110.472985, 19.959158), (110.41858, 19.959158), (110.364175, 20.048561),
                 (110.436715, 19.959158), (110.23723, 20.01876), (110.400445, 19.9889589999999),
                 (110.472985, 19.929357), (110.45485, 19.959158), (110.20096, 20.048561), (110.49112, 19.929357),
                 (110.327905, 19.899556), (110.38231, 20.01876)]
    orders = [0, 100, 98, 86, 83, 79, 74, 53, 50, 49, 44, 30, 20, 20, 10, 7, 6, 6, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4,
              4]
    loc_spl = location_split(locations, orders)
    split_rand = split_rand_gen(10)
    print(loc_spl.split(split_rand))