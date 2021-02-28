import random
import re
import math
import seaborn as sns
import matplotlib.pyplot as plt


def file_data(file_num):
    x = 100
    y = 100
    fw = open("k-means_data.txt", "w", encoding="utf-8")
    for i in range(0, file_num):
        data = [str(random.randint(0, x)), " ", str(random.randint(0, y)), " ", str(0), "\n"]
        fw.writelines(data)

    fw.close()


    fr = open("k-means_data.txt", "r", encoding="utf-8")
    entire_data = []
    for data in fr:
        data = data.split(" ")
        data[0] = int(data[0])
        data[1] = int(data[1])
        data[2] = re.sub("\n", "", data[2])
        data[2] = int(data[2])
        entire_data.append(data)

    fr.close()
    return entire_data


def clustering(n):
    file_num = 200
    entire_data = file_data(file_num)
    G = []

    #初期設定(重心の位置をランダムで決定する)
    for i in range(1, n+1):
        index = random.randint(0, file_num-1)
        entire_data[index][2] = i
        G.append(entire_data[index])

    
    while True:
        #各データのラベルを振り分ける
        for i in range(0, file_num):
            min_dis = 10000
            for j in range(0, n):
                dis = math.sqrt((entire_data[i][0] - G[j][0])**2 + (entire_data[i][1] - G[j][1])**2)
                if min_dis > dis:
                    min_dis = dis
                    entire_data[i][2] = G[j][2]


        #重心を更新する
        """各ラベルごとに分けて考える(前処理)"""
        entire_label = []
        for i in range(1, n+1):
            each_label = [data for data in entire_data if data[2] == i]
            entire_label.append(each_label)

        """各ラベルごとに重心を更新する"""
        i = 0  #重心が同じであった回数
        j = 0  #配列Gのインデックス
        l = 0
        for each_label, g in zip(entire_label, G):
            x_sum = 0.0
            y_sum = 0.0
            for data in each_label:
                x_sum += data[0]
                y_sum += data[1]
        
            if len(each_label) == 0:
                l = 1
                break

            x_ave = x_sum / len(each_label)
            y_ave = y_sum / len(each_label)

            """重心が更新されない(i==3)場合は終了"""
            if g[0] == x_ave and g[1] == y_ave:
                i += 1
                if i == 3:
                    break
                else:
                    continue
            else:
                j += 1
                G[j-1] = [x_ave, y_ave, j]
                
        
        """重心が更新されない場合"""
        if i == 3:
            break
        if l == 1:
            break

    
    if l == 1:
        return
    

    #プロットする
    Entire_label = []
    for i in range(1, n+1):
        each_label = [data for data in entire_data if data[2] == i]
        Entire_label.append(each_label)
    
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    x3 = []
    y3 = []

    #k = 4
    """
    x4 = []
    y4 = []
    """
    
    for each_label in Entire_label:
        for data in each_label:

            
            #k = 3
            if data[2] == 1:
                x1.append(data[0])
                y1.append(data[1])
            elif data[2] == 2:
                x2.append(data[0])
                y2.append(data[1])
            else:
                x3.append(data[0])
                y3.append(data[1])
            
            
            """
            #k = 4
            if data[2] == 1:
                x1.append(data[0])
                y1.append(data[1])
            elif data[2] == 2:
                x2.append(data[0])
                y2.append(data[1])
            elif data[2] == 3:
                x3.append(data[0])
                y3.append(data[1])
            else:
                x4.append(data[0])
                y4.append(data[1])
            """

    
    plt.scatter(x1, y1, c="red")
    plt.scatter(x2, y2, c="green")
    plt.scatter(x3, y3, c="blue")
    """
    plt.scatter(x4, y4, c="orange")
    """
    
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Scatter Plot of clustering")
    plt.show()


    #結果をファイルに格納
    fw = open("k-means_data_result.txt", "w", encoding="utf-8")
    for data in entire_data:
        data[0] = str(data[0]) + " "
        data[1] = str(data[1]) + " "
        data[2] = str(data[2]) + "\n"
        fw.writelines(data)

    fw.close()


    
clustering(3)


    
            







