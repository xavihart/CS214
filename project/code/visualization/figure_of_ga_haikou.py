import matplotlib as mlp
import matplotlib.pyplot as plt

numbers1 = []
numbers2 = []
numbers3 = []

with open('results/haikou/20/BIG2min_list_cap20[alpha1.0population200]split4.txt') as fp:
    #Iterate through each line
    for line in fp:
        if(line == 'route:\n'):
            break
        numbers1.extend([float(item) for item in line.split() ])

with open('results/haikou/30/BIGmin_list_cap30[alpha0.1population600]split4.txt') as fp:
    #Iterate through each line
    for line in fp:
        if(line == 'route:\n'):
            break
        numbers2.extend([float(item) for item in line.split() ])

fig, ax2 = plt.subplots(figsize = (4, 3)) 
ax2.set_xlabel('Iteration number')  # Add an x-label to the axes.
ax2.set_ylabel('Shortest distance')  # Add a y-label to the axes.
ax2.set_title("Comparision between different population\n Haikou, Cap=20, alpha=1.0, Popu=200") 

ax2.plot(numbers1)
#ax2.plot(numbers2, label='population=600')

#ax2.legend()  # Add a legend.
plt.savefig("results/haikou/haikou_20_best.png", dpi=200,  bbox_inches = 'tight')
plt.show()
