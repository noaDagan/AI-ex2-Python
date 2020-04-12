from collections import *
from itertools import *
import random
def get_anagrams(words):
    for w in words:
        z = ''.join(sorted(w))
    normalized = [''.join(sorted(w)) for w in words]

    d = Counter(normalized)

    return [w for w, n in zip(words, normalized) if d[n] > 1]

#print (get_anagrams(["pool", "loco", "cool", "stain", "satin", "pretty", "nice", "loop"]))



def f(h):
    mem = {-2: 0, -1: 0, 0: 1}
    if h in mem:
        return mem[h]
    else:
        mem[h] = f(h-1) + f(h-2) + f(h-3)
        return mem[h]

#print(f(4))


def func():
    input_x = input()
    sum = int(input_x)
    count = 1
    while True:
        input_x = input()
        if input_x == 'q':
            break
        sum += int(input_x)
        count += 1
    print( sum / count)

#func()


def func1(list_of_num,number):
    return_list =[]
    for num in list_of_num:
        if num % number != 0:
            return_list.append(num)
    list_of_num = []
    for counter, value in enumerate(return_list):
        list_of_num.append(value)
    print(list_of_num)
    return return_list


func1([1,2,3,4,5],2)



def func2(str_temp):
    i = 0
    if str_temp == str_temp[::-1]:
        print("nnnnnnnnn")
    j = len(str_temp) - 1
    while str_temp[i] == str_temp[j]:
        j -= 1
        i += 1
        if i == j or j - 1 == i or i - 1 == j:
            print ("True")
            return True
    print("False")
    return False


def func3():
    x1 = input()
    x2 = input()
    x3 = input()
    y1 = random.randint(1, 9)
    y2 = random.randint(1, 9)
    y3 = random.randint(1, 9)
    a=[]
    b=[]
    a.append(x1)
    a.append(x2)
    a.append(x3)
    b.append(y1)
    b.append(y2)
    b.append(y3)
    a.sort()
    b.sort()
    if a==b:
        print("yessssss")
    else:
        print ("nooooooo")


def func4(file_name):
    file = open(file_name,"r+")
    line = file.readline()
    line.split(" ")
    sum = int(line[0]) + int(line[1])
    file.write(sum)



def func5(list_name):
    list_name.sort()
    new_list = []
    counter = 0
    j = list_name[0]
    list_name = list_name[1:]
    for i in list_name:
        if j == i:
            counter += 1
        else:
            new_list.append(counter)
            counter = 0

        j = i


def sumlist(numbers):
    result = [0] * 10
    for n in numbers:
        result[n] += 1
    print (result)
    return result

sumlist([1,2,3,2,2,2,3])