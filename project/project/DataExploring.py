import os
import matplotlib.pyplot as plt
import numpy as np
import queue

def BFS(mat, r, c):
    """
    :param mat: np.array, to determine if the point is choosed
    :param x: starting point x
    :param y: starting point y
    :return: nearest point
    """
    mat = mat.copy()
    vst = np.zeros(mat.shape)
    rmax, cmax = mat.shape[0], mat.shape[1]
    def val_index(p, q):
        return (p >= 0) and (q >= 0) and (p < rmax) and (q < cmax)
    assert mat[r][c] == 0
    q = queue.Queue()
    dir = ((1, 0), (-1, 0), (0, 1), (0, -1))
    q.put((r, c))
    while True:
        (x, y) = q.get()
        if mat[x][y] == 1:
            break
        for i in range(4):
            if val_index(x + dir[i][0], y + dir[i][1]):
                if vst[x + dir[i][0]][y + dir[i][1]] == 0:
                    q.put((x + dir[i][0], y + dir[i][1]))
                    vst[x + dir[i][0]][y + dir[i][1]] = 1
    return x, y




def GridExplore(data, grid, num_des, k, city):
    '''
    :param data: DataFrame
    :param grid:
    :param num_des:
    :return: despoint, [(deppoint)], [num]
    '''

    def index_val(i):
        return (i < grid) and (i >= 0)
    n = data.shape[0]

    DepGrid = np.zeros((grid, grid)).astype("int64")
    DesGrid = np.zeros((grid, grid)).astype("int64")

    LatMax_pick = data['LatPick'].max()
    LatMin_pick = data['LatPick'].min()
    LonMax_pick = data['LonPick'].max()
    LonMin_pick = data['LonPick'].min()

    LatMax_drop = data['LatDrop'].max()
    LatMin_drop = data['LatDrop'].min()
    LonMax_drop = data['LonDrop'].max()
    LonMin_drop = data['LonDrop'].min()

    #print(LatMax_pick, LatMax_drop, LatMin_drop)

    #LatMin_pick, LatMax_pick = plant_extract(LatMin_pick, LatMax_pick, 0, 0)
    #LonMin_pick, LonMax_pick = plant_extract(LonMin_pick, LonMax_pick, 0, 0)


    #LatMin_drop, LatMax_drop = plant_extract(LatMin_drop, LatMax_drop, 0, 0)
    #LonMin_drop, LonMax_drop = plant_extract(LonMin_drop, LonMax_drop, 0, 0)


    interval_lat_pick = (LatMax_pick - LatMin_pick) / grid
    interval_lon_pick = (LonMax_pick - LonMin_pick) / grid

    interval_lat_drop = (LatMax_drop - LatMin_drop) / grid
    interval_lon_drop = (LonMax_drop - LonMin_drop) / grid

    print(interval_lat_drop, interval_lon_drop)

    for i in range(n):
        lat_pick, lon_pick, lat_drop, lon_drop = data['LatPick'][i],data['LonPick'][i],\
                                                 data['LatDrop'][i], data['LonDrop'][i]

        x_pick = min(grid - 1, ((lon_pick - LonMin_pick) // interval_lon_pick).astype("int"))
        y_pick = min(grid - 1, ((lat_pick - LatMin_pick) // interval_lat_pick).astype("int"))

        x_drop = min(grid - 1, ((lon_drop - LonMin_drop) // interval_lon_drop).astype("int"))
        y_drop = min(grid - 1, ((lat_drop - LatMin_drop) // interval_lat_drop).astype("int"))

        if index_val(x_drop) and index_val(x_pick) and index_val(y_drop) and index_val(y_pick):
           DepGrid[x_pick][y_pick] += 1
           DesGrid[x_drop][y_drop] += 1


    DepPoint = list(np.unravel_index(np.argmax(DepGrid),DepGrid.shape))
    DepPoint[0] = DepPoint[0] * interval_lon_pick + LonMin_pick
    DepPoint[1] = DepPoint[1] * interval_lat_pick + LatMin_pick

    DesPointsX, DesPointsY = np.unravel_index(np.argsort(DesGrid, axis=None)[::-1], DesGrid.shape)

    DesPointsX, DesPointsY = list(DesPointsX), list(DesPointsY)
    index = [i for i in range(grid ** 2)]
    index_choose = index[0:10:1] + index[10:k*num_des - 10:k] # index selected
    last_index = index_choose[len(index_choose) - 1]
    mask = np.zeros(DesGrid.shape)
    for i in range(last_index+1):
        mask[DesPointsX[i]][DesPointsY[i]] = 1

    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if mask[i][j] == 0:
                x, y = BFS(mask, i, j)
                DesGrid[x][y] += DesGrid[i][j]
                DesGrid[i][j] = 0

    DesPointsX = [DesPointsX[i] for i in index_choose]
    DesPointsY = [DesPointsY[i] for i in index_choose]


    for i in range(num_des):
        print(DesGrid[DesPointsX[i]][DesPointsY[i]])

    DesPoint = [(DesPointsX[i] * interval_lon_drop + LonMin_drop, DesPointsY[i] * interval_lat_drop + LatMin_drop, DesGrid[DesPointsX[i]][DesPointsY[i]]) for i in range(num_des)]


    for i in range(num_des):
        print("{},{}\n".format(DesPoint[i][0], DesPoint[i][1]))

    print("Departure point", DepPoint)

    print("Destination point", DesPoint)

    print(DesGrid)
   
    plt.matshow(DesGrid, cmap="jet")
    plt.savefig("./results/Des_{}_v1.jpg".format(grid))
    plt.show()
    plt.matshow(DepGrid, cmap="hot")
    plt.savefig("./results/Dep_{}_v1.jpg".format(grid))
    plt.show()

    plt.cla()
    plt.scatter(DepPoint[0], DepPoint[1], marker="*", linewidths=5, c = 'r')
    x = [DesPoint[i][0] for i in range(num_des)]
    y = [DesPoint[i][1] for i in range(num_des)]
    plt.scatter(x, y, marker=",", linewidths=2, c='b')

    plt.savefig('./results/Points_{}g_{}des_{}k_{}.jpg'.format(str(grid), str(num_des), k, city))
    return DesPoint, DepPoint

