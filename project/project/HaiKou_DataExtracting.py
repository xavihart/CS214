import os
import pandas

file_list = []
for i in range(1, 9):
    file_list.append('./data_haikou/dwv_order_make_haikou_{}.txt'.format(i))

data = []
date_list = ['2017-10-07', '2017-10-08', '2017-10-09', '2017-10-10']
for f in file_list:
    f0 = open(f, "rb")
    i = 0
    print("read_file:[{}]".format(f))
    for lines in f0:
        lines = str(lines)
        l = lines.split("\\t")
        date = l[11]
        if date[:10] not in date_list:
            continue
        l = l[-7:-3]  # only need four coloumns of data
        l = [float(i) for i in l]
        data.append(l)
print(len(data))

Data = pandas.DataFrame(data)
Data.rename(columns={0: "LonDrop", 1: "LatDrop", 2: "LonPick", 3: "LatPick"}, inplace=True)
Data.to_csv('./data_haikou/order.csv', header=1)


