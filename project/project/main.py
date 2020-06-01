from DataExploring import *
from tools.utils import *
import pandas as pd
import argparse



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

Despoint, Deppoint = GridExplore(data, grid, num_des, k=2)

print(Deppoint)

print(Despoint)