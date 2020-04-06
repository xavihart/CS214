import numpy as np

def BookShelf_Solution(data_path):
    # init data
    t = [0]
    w = [0]
    f = open(data_path)
    
    for i, lines in enumerate(f):
        if i == 0:
            n = int(lines)
        else:
            ite = lines.split(' ')
            t.append(int(ite[0]))
            w.append(int(ite[1]))
   
    # init dp-matri: dp[i][j] = inf means the 1-ith books can not be aranged in length j
    dp =  np.ones((n+5, 3*n))
    dp *= 3*n

    # can be aranged
    dp[0][0] = 0
    
    # dp tranverse
    current_thickness = 0
    for i in range(1, n+1):
        current_thickness += t[i]
        for j in range(1, current_thickness + 1):
            if j - t[i] >= 0:
                dp[i][j] = min(dp[i - 1][j] + w[i], dp[i - 1][j - t[i]])
            else:
                dp[i][j] = dp[i - 1][j] + w[i]
    
    for i in range(current_thickness):
        if(dp[n][i] <= i):
            print(i)
            break

if __name__ == "__main__":
    BookShelf_Solution("./Data-P1.txt")
    


