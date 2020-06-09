import numpy as np
import pandas as pd
import random
import os
import argparse
import copy
import heapq
import matplotlib.pyplot as plt
from gaTools import *

parser = argparse.ArgumentParser()
parser.add_argument("--city", default="chengdu", type=str)
parser.add_argument("--population", default="1000", type=int)
parser.add_argument("--alpha", default="0.1", type=float)
parser.add_argument("--cap", default="20", type=int)


args = parser.parse_args()
random.seed()
population_number = args.population
alpha = args.alpha
cap = args.cap
city = args.city

if city == "chengdu":
    csv_path = "./results/pointChoose/chengdu_50 _subset.xlsx"
elif city == 'haikou':
    csv_path = "./results/pointChoose/haikou_100 _subset.xlsx"

dataMat = pd.read_excel(csv_path)
lonArray = list(dataMat['LonDrop'])
latArray = list(dataMat['LatDrop'])

demand= list(dataMat[cap])

if city == "chengdu":
    lonDep = 104.0494
    latDep = 30.6412
elif city == "haikou":
    lonDep = 110.334
    latDep = 20.0241


# val that will be used in function
best_init_cost = 0
total_dem = sum(demand)
num_des = len(lonArray)

# dist_map
dist_map = np.zeros((num_des, num_des))

def maxk(arraylist,k):
    '''
    max k elemnet in the array, return the index in seq
    '''
    maxlist=[]
    maxlist_id=range(0,k)
    m=[maxlist,maxlist_id]
    for i in maxlist_id:
        maxlist.append(arraylist[i])
    for i in range(k,len(arraylist)):
        if arraylist[i]>min(maxlist):
            mm=maxlist.index(min(maxlist))
            del m[0][mm]
            del m[1][mm]
            m[0].append(arraylist[i])
            m[1].append(i)


def dis_earth_(i, j):
    lat1, long1 = latArray[i],lonArray[i]
    lat2, long2 = latArray[j],lonArray[j]
    tmp = np.sin(lat1 / 180 * np.pi) * np.sin(lat2 / 180 * np.pi) + \
          np.cos(lat1 / 180 * np.pi) * np.cos(lat2 / 180 * np.pi) * np.cos((long1 - long2) / 180 * np.pi)
    return 6371 * np.arccos(tmp)

def dis_earth(i, j):
    return dist_map[i][j]


def dis_from_start(j):
    lat1, long1 =  latDep, lonDep
    lat2, long2 =  latArray[j],lonArray[j]
    tmp = np.sin(lat1 / 180 * np.pi) * np.sin(lat2 / 180 * np.pi) + \
          np.cos(lat1 / 180 * np.pi) * np.cos(lat2 / 180 * np.pi) * np.cos((long1 - long2) / 180 * np.pi)
    return 6371 * np.arccos(tmp)


def generate_random_solutions():
    """

    :return: solution: list of route
    """
    unserved = [j for j in range(num_des)]
    solution = []
    crt_point = 0
    while len(unserved) > 0:

        crt_cap = 0
        r = []

        while True:
            #print(unserved)
            if len(unserved) == 0:
                if len(r) > 0:
                    solution.append(r)
                break
            if len(r) == 0:
                i = min([i for i in range(len(unserved))], key=lambda x:dis_from_start(x))
            else:
                rd = random.uniform(0, 1)
                i = min([i for i in range(len(unserved))], \
                        key=lambda x : dis_earth(r[-1], unserved[x]) if rd < 0.7 else dis_from_start(unserved[x]))
            crt_cap += demand[unserved[i]]
            if crt_cap > cap:
                solution.append(r)
                break
            else:
                r.append(unserved[i])
                unserved.remove(unserved[i])
    #print(solution)
    return solution


def LocalSearch(slt):
    """

    :param slt: list
    :return:  new order after LSA using SIA
    """
    saving = 1
    l = len(slt)
    if l < 3:
        return slt
    while saving > 0.01:
        #print(saving)
        saving = 0
        ibest, jbest = 0, 0
        for j in range(l-1):
            for i in range(j):
                if i + 1 == j:
                    continue
                else:
                    t1 = slt[i]
                    t2 = slt[i + 1]
                    t3 = slt[j]
                    t4 = slt[j + 1]
                    #print(t1, t2, t3, t4)
                    diff = dis_earth(t1, t2) + dis_earth(t3, t4) - dis_earth(t1, t3) - dis_earth(t2, t4)
                    if diff > saving:
                        saving = diff
                        ibest = i
                        jbest = j
        if saving > 0:
            #print(saving)
            slt = slt[0:ibest + 1] + slt[ibest + 1:jbest + 1][::-1] + \
                  slt[jbest + 1: len(slt)]

    return slt


def SIA(S):
    #print(cal_des_num(S))
    for j in range(len(S)):
        S[j] = LocalSearch(S[j])
    assert (cal_des_num(S) == 30)

def cost(S):
    tot_dist = 0
    #print(S)
    for route in S:
        tot_dist += dis_from_start(route[0])
        tot_dist += dis_from_start(route[len(route) - 1])
        #print("00", tot_dist)
        for i in range(len(route) - 1):
            tot_dist += dis_earth(route[i], route[i + 1])
        #print(tot_dist)
    return tot_dist


def penalty(S, iter):
    pen = 0
    for route in S:
        dem = 0
        for i in route:
            dem += demand[i]
        if dem > cap:
            pen += (dem - cap) ** 2
    return pen


def fitness(S, iter):
    return cost(S) + alpha * best_init_cost * iter \
           * penalty(S, iter) / (cap * (total_dem // cap))**2


def random_subroute_choose(S):
    """

    :param S: a solution
    :return: subroute list for S
    """

    while True:
        #print(S)
        n = random.randrange(0, len(S))
        if len(S[n]) >= 2:
            break
    while True:
        i = random.randrange(0, len(S[n]))
        j = random.randrange(0, len(S[n]))
        if j - i >= 1:
            break
    return n, S[n][i:j+1]

def CrossOver(Si_, Sj):
    n, subr = random_subroute_choose(Sj)
    Si = copy.deepcopy(Si_)
    #print(Si)
    for i in subr:
        for j in range(len(Si)):
            if i in Si[j]:
                Si[j].remove(i)
    #print(Si)
    l = len(Si)

    while [] in Si:
        Si.remove([])

    # insert subr into Si
    rx_min, rx_max = min([lonArray[i] for i in subr]), max(lonArray[i] for i in subr)
    ry_min, ry_max = min([latArray[i] for i in subr]), max(latArray[i] for i in subr)
    bbarea = []
    for routes in Si:
        if len(routes) == 1:
            bbarea.append(-1)
            continue
        x_min, x_max = min([lonArray[i] for i in routes]), max(lonArray[i] for i in routes)
        y_min, y_max = min([latArray[i] for i in routes]), max(latArray[i] for i in routes)
        bbax = max(0, min(x_max, rx_max) - max(x_min, rx_min))
        bbay = max(0, min(y_max, ry_max) - max(y_min, ry_min))
        bba = bbax * bbay
        bbarea.append(bba)
    #print(bbarea)
    id = list(map(bbarea.index, heapq.nlargest(3, bbarea)))
    #print(id)
    id_min_demand = id[0]
    if bbarea[id_min_demand] < 0:
        print("fall")
        return Si_
    min_dmd = 1e9
    for i in id:
        if bbarea[i] < 0:
           continue
        dmd = 0
        for j in Si[i]:
            dmd += demand[j]
        if dmd < min_dmd:
            min_dmd = dmd
            id_min_demand = i
    #print(Si[id_min_demand])
    Si_route_choose = id_min_demand

    insert_index = min([i for i in range(len(Si[Si_route_choose])-1)], key = lambda x : \
        dis_earth(Si[Si_route_choose][x], subr[0]) + dis_earth(Si[Si_route_choose] [x + 1], subr[-1]))

    dist_min = dis_earth(Si[Si_route_choose][insert_index], subr[0]) + dis_earth(Si[Si_route_choose][insert_index + 1], subr[-1])
    insert_head_dist = dis_from_start(subr[0]) + dis_earth(subr[-1], Si[Si_route_choose][0])
    insert_tail_dist = dis_from_start(subr[-1]) + dis_earth(subr[0], Si[Si_route_choose][-1])

    if insert_head_dist < dist_min and insert_head_dist < insert_tail_dist:
        Si[Si_route_choose] = subr + Si[Si_route_choose]
        #print("1st")
    elif insert_tail_dist < dist_min and insert_tail_dist < insert_head_dist:
        #print(Si[Si_route_choose], subr)
        Si[Si_route_choose] = Si[Si_route_choose] + subr
        #print(Si[Si_route_choose])
        #print("len2-------", cal_des_num(Si))
    else:
        #print("len3a-------", cal_des_num(Si), subr, Si[Si_route_choose])
        Si[Si_route_choose] = Si[Si_route_choose][0:insert_index + 1] + subr + Si[Si_route_choose][
                                                                   insert_index + 1:len(Si[Si_route_choose])]
        #print(Si[Si_route_choose])
        #print(insert_index)
        #print("len3b-------", cal_des_num(Si))
    assert(cal_des_num(Si) == 30)
    return Si

def Muten(S):
    """
    
    :param S: a solution
    :return: randomly choose a customer and insert it into best position in other routes
    """
    while True:
        #print("hi")
        n = random.randrange(0, len(S))
        if len(S[n]) > 1:
            break
    k = random.randrange(0, len(S[n]))
    k = S[n][k]

    S[n].remove(k)
    r = random.uniform(0, 1)
    if r <= 0.2:
        if len(S[n]) <= 1:
            S[n] = S[n] + [k]
            #print("s1")
            return S
        ins = min([i for i in range(len(S[n]) - 1)], key = lambda x: dis_earth(k, S[n][x]) + dis_earth(k, S[n][x+1]))
        S[n] = S[n][0:ins+1] + [k] + S[n][ins+1:len(S[n])]
        return S
    else:
        besti, bestj = 0, 0
        MinDist = 1e9
        for i in range(len(S)):
            if i == n:
                continue
            for j in range(len(S[i]) - 1):
                dis = dis_earth(S[i][j], k) + dis_earth(S[i][j + 1], k)
                if dis < MinDist:
                    MinDist = dis
                    besti, bestj = i, j

        S[besti] = S[besti][0:bestj+1] + [k] + S[besti][bestj + 1: len(S[besti])]

    assert(cal_des_num(S) == 30)
    return S

def valid_solution(S):
    for r in S:
        dmd = 0
        for i in range(len(r)):
            dmd += demand[r[i]]
        if dmd > cap:
            return 0
    return 1

def route_dmd(route):
    return sum([demand[i] for i in route])


def repairing(routes):
    r_max_i = max((i for i in range(len(routes))), key=lambda i: route_dmd(routes[i]))
    r_min_i = min((i for i in range(len(routes))), key=lambda i: route_dmd(routes[i]))
    if route_dmd(routes[r_max_i]) > cap:
        rint = random.randrange(0, len(routes[r_max_i]) - 1)
        routes[r_min_i]+=[routes[r_max_i][rint]]
        routes[r_max_i].remove(routes[r_max_i][rint])
        assert (cal_des_num(routes) == 30)
        return True
    return False


def cal_des_num(S):
    t = 0
    for i in S:
        t += len(i)
    return t



def main():
    # to do
    for i in range(num_des):
        for j in range(num_des):
            dist_map[i][j] = dis_earth_(i,j)
    #print(cost([[0], [1], [2], [3], [4, 11], [5], [13], [7, 9, 23, 8], [10, 29, 17, 19, 12, 14, 15], [16, 6, 25, 18, 21, 27, 24, 26, 28, 22, 20]]))
    iteration = 300
    population = [generate_random_solutions() for _ in range(population_number)]

    muta_prop = 0.3
    cross_prop = 0.9
    min_list = []
    #for i in range(len(population)):
    #   SIA(population[i])

    sorted(population, key=lambda x:cost(x))
    global best_init_cost
    best_init_cost = cost(population[0])
    print("best init cost", best_init_cost, population[0])

    for iter in range(1, iteration+1):
        k = 1
        #print(population[0], "b")
        for i in range(0, len(population) // 8):
            j = i + len(population) // 8
            if random.uniform(0, 1) < 0.2:
                j = random.randrange(0, len(population))
            if i == j:
                continue
            r = random.uniform(0, 1)
            if r < cross_prop:

                c = CrossOver(population[j], population[i])
                rmuta = random.uniform(0, 1)
                if rmuta < muta_prop:
                   c = Muten(c)
                   #print("mt")
                assert (cal_des_num(c) == 30)
                SIA(c)
                f = repairing(c)
                population[-k] = c
                #print(cost(c))
                k += 1
        min_cost = 1e9
        min_indiv = population[0]
        for k in population:
            if valid_solution(k):
                cost_i = cost(k)
                if cost_i < min_cost:
                    min_cost = cost_i
                    min_indiv = k
        population = sorted(population, key=lambda x:fitness(x, iter))
        #print(population[0], "a")
        min_list.append(min_cost)
        print("fitness", [fitness(x,iter) for x in population])
        print("iteration[{}], best cost[{}], solultion[{}]".format(iter, min_cost, min_indiv))
    plt.plot(min_list)
    plt.savefig("./results/GA/{}/costCurve_cap{}[alpha{}population{}].jpg".format(city, cap, alpha, population_number))
    f=open("./results/GA/{}/min_list_cap{}[alpha{}population{}].txt".format(city, cap, alpha, population_number), "w")
    for i in min_list:
        f.write(str(i)+" ")
    f.write("\nroute:\n")
    for i in min_indiv:
        for j in i:
            f.write(str(j)+" ")
        f.write("\n")
    f.close()
    return

if __name__ == '__main__':
    main()



