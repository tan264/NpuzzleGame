from heapq import heapify, heappush, heappop

#Tạo chuỗi dạng ma trận 2 chiều cho ma trận matrix được truyền vào
def toString(matrix):
    s = "\n"
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            s += str(matrix[i][j]) + " "
        s += "\n"

    return s

#Tính khoảng cách manhattan của ma trận matrix được truyền vào
def manhattan(matrix):
    n = len(matrix)
    counter = 0
    expectedCoord = [0, 0]
    for i in range (n):
        for j in range (n):
            value = matrix[i][j]
            if (value == 0):
                continue
            expectedCoord[0] = (value - 1) // n
            expectedCoord[1] = (value - 1) % n
            counter += abs(expectedCoord[0] - i) + abs(expectedCoord[1] - j)
    return counter

#Kiểm tra ma trận matrix được truyền vào đã là ma trận đích chưa
def isGoal(matrix):
    temp = 0
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if (i == n - 1 and j == n - 1 and matrix[i][j] == 0):
                break
            temp += 1
            if (matrix[i][j] != temp):
                return False
          
    return True

#Lấy các ma trận hàng xóm của ma trận current được truyền vào
def  neighbors(current):
    n = len(current[-1])
    neighbors = []
    blank = None# chứa toạ độ của điểm blank

    #Lấy toạ độ điểm blank của ma trận trong biến current
    for i in range(n):
        try:
            blank = current[i].index (0)
        except Exception as e:
            continue
        blank = (i, blank)
        break

    if (blank[1] < (n - 1)):# Nếu có thể di chuyển blank sang phải
        a = [ i.copy() for i in current ]
        number = a[blank[0]][blank[1] + 1]
        a[blank[0]][blank[1]], a[blank[0]][blank[1] + 1] = a[blank[0]][blank[1] + 1], a[blank[0]][blank[1]]
        neighbors.append(('Click ' + str(number) + " or press the LEFT arrow key" + toString(a), a, (blank[0], blank[1] + 1)))

    if (blank[1] > 0):# Nếu có thể di chuyển blank sang trái
        b = [ i.copy () for i in current ]
        number = b[blank[0]][blank[1] - 1]
        b[blank[0]][blank[1]], b[blank[0]][blank[1] - 1] = b[blank[0]][blank[1] - 1], b[blank[0]][blank[1]]
        neighbors.append(('Click ' + str(number) + " or press the RIGHT arrow key"+ toString(b), b, (blank[0], blank[1] - 1)))

    if (blank[0] > 0):# Nếu có thể di chuyển blank đi lên
        c = [ i.copy () for i in current ]
        number = c[blank[0] - 1][blank[1]]
        c[blank[0]][blank[1]], c[blank[0] - 1][blank[1]] = c[blank[0] - 1][blank[1]], c[blank[0]][blank[1]]
        neighbors.append(('Click ' + str(number) + " or press the DOWN arrow key"+toString(c), c, (blank[0] - 1, blank[1])))

    if (blank[0] < (n - 1)):# Nếu có thể di chuyển blank đi xuống
        d = [ i.copy () for i in current ]
        number = d[blank[0] + 1][blank[1]]
        d[blank[0]][blank[1]], d[blank[0] + 1][blank[1]] = d[blank[0] + 1][blank[1]], d[blank[0]][blank[1]]
        neighbors.append(('Click ' + str(number) + " or press the UP arrow key"+ toString(d), d, (blank[0] + 1, blank[1])))

    return neighbors

import time
def solve(grid):# sử dụng thuật toán A* để giải
    # biến currentNode có cấu trúc như sau:
    # currentNode[0] độ ưu tiên
    # currentNode[1] số bước đã dịch chuyển để tới ma trận này(ma trận lưu trong currentNode[3])
    # currentNode[2] chứa các cách thức di chuyển
    # currentNode[3] chứa ma trận hiện tại
    currentNode = (manhattan(grid), 0, [], grid) # node đầu tiên
    stateTree = [currentNode] # cây với 1 node đầu tiên
    visited_matrix = [] # chứa danh sách các ma trận đã đi qua
    inner_matrix = [currentNode[-1]] # chứa danh sách các ma trận đang ở trong stateTree

    heapify(stateTree) # khởi tạo priority queue
    start_time = time.time() # thời gian bắt đầu giải
    while (not  isGoal(currentNode[-1])):
        currentNode = heappop(stateTree) # lấy từ priority queue node có currentNode[0] nhỏ nhất
        inner_matrix.remove(currentNode[-1]) # ma trận currentNode[-1] ko ở trong stateTree nữa nên xoá đi
        visited_matrix.append(currentNode[-1]) # thêm vào những ma trận đã đi qua
        # print(currentNode)

        for state in  neighbors(currentNode[-1]): # lấy các ma trận hàng xóm
            if (state[1] not in visited_matrix and state[1] not in inner_matrix): # Nếu ma trận state[1] đã đi qua hoặc ở trong pq rồi thì không thêm vào nữa
                heappush(stateTree, 
                    (
                        manhattan(state[1]) + currentNode[1] + 1,
                        currentNode[1] + 1, 
                        currentNode[2] + [state[0]], 
                        state[1]
                    )
                )
                inner_matrix.append(state[1])

    # Trả về số bước dịch chuyển, dãy các cách thức di chuyển, thời gian thực thi
    return (currentNode[1], currentNode[2], round(time.time() - start_time, 2))

from tkinter import *
from tkinter import scrolledtext
def guide(matrix):# cài đặt giao diện hiển thị kết quả
    ws = Tk()
    ws.title('Guide')
    ws.geometry('400x640')
    ws.configure(bg='#04bf87')
    font_tuple = ("Helvetica", 12)
    label = Label(ws, text = "Processing ...", font = font_tuple )
    label.pack(expand=True)
    ws.update()

    report = ""
    seqCount, sequence, time_excute = solve(matrix)
    label.destroy()
    report +=  str(time_excute) + " seconds\n"
    report += str(seqCount) + " steps\n\n"
    report += "Initial board:"
    report += toString(matrix) + "\n"
    report += '\n'.join (sequence)  

    text_box = scrolledtext.ScrolledText(
        ws,
        height=140,
        width=100,
        wrap='word',
        bg='#04bf87',
        font=font_tuple
    )
    text_box.insert('end', report)
    text_box.pack(side=LEFT,expand=True)
    text_box.config(state='disabled')

    ws.mainloop()
    

if (__name__ == '__main__'):
    # 1.2 - 1.5s
    # grid = [[1,4,0], [2,5,3], [7,6,8]]

    # 7.2 - 8.5s
    grid = [[6,5,4], [7,0,8], [1,2,3]]

    # 0 - 0.01s
    # grid = [[0,1,3], [4,2,5], [7,8,6]]
    guide(grid)