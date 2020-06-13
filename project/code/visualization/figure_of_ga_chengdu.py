import matplotlib as mlp
import matplotlib.pyplot as plt
import math

numbers1 = []
numbers2 = []
numbers3 = []

with open('results/chengdu/20/BIGmin_list_cap20[alpha0.1population350]split4.txt') as fp:
    #Iterate through each line
    for line in fp:
        if(line == 'route:\n'):
            break
        numbers1.extend([float(item) for item in line.split() ])

with open('results/chengdu/25/BIGmin_list_cap25[alpha0.1population550]split4.txt') as fp:
    #Iterate through each line
    for line in fp:
        if(line == 'route:\n'):
            break
        numbers2.extend([float(item) for item in line.split() ])

with open('results/chengdu/30/BIGmin_list_cap30[alpha0.1population500]split4.txt') as fp:
    #Iterate through each line
    for line in fp:
        if(line == 'route:\n'):
            break
        numbers3.extend([float(item) for item in line.split() ])


fig, ax2 = plt.subplots(figsize = (4, 3)) 
ax2.set_xlabel('Iteration number')  # Add an x-label to the axes.
ax2.set_ylabel('Shortest distance')  # Add a y-label to the axes.
ax2.set_title("Comparision between different population\n Chengdu, cap=20, alpha=0.1, best result")  # Add a title to the axes.
#ax2.set_yscale('log')

ax2.plot(numbers1, label='population=350')
#ax2.plot(numbers2, label='population=550')
#ax2.plot(numbers3, label='population=500')

ax2.legend()  # Add a legend.
plt.savefig("results/chengdu/chengdu_best_20.png", dpi=200,  bbox_inches = 'tight')
plt.show()
