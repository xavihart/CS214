from DataExploring import *
from tools.utils import *
import pandas as pd
import argparse


print(os.getcwd())
parser = argparse.ArgumentParser()
parser.add_argument("--city", default="chengdu", type=str)
parser.add_argument("--grid", default=20, type=int)
parser.add_argument("--desnum", default=30, type=int)
args = parser.parse_args()

city = args.city
grid = args.grid
num_des = args.desnum


if city == "chengdu":
    data =read_file("./data_chengdu/total_ride_request/order_20161106", "rb", "chengdu")
elif city == "haikou":
    data = pd.read_csv("./data_haikou/order.csv")


Despoint, Deppoint = GridExplore(data, grid, num_des, k=2, city=city)

print(Deppoint)
print(Despoint)

DesCSV = pd.DataFrame(Despoint)
DesCSV.rename(columns={0: "LonDrop", 1: "LatDrop", 2:"NumOrder"}, inplace=True)
DesCSV.to_csv("./results/pointChoose/{}_{}.csv".format(city, grid))

f = open("./results/pointChoose/points_{}.txt".format(city), "w")
f.write(str(Deppoint) + "\n")
f.write(str(Despoint))
f.close()




