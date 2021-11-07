#!/usr/bin/env python
# coding: utf-8

# In[1]:

import time
import random
import numpy as np
# 初始化，找出最长的sequence。
# 随机再开头和结尾加‘-’生成相同长度的sequence。注意本例作为基础的遗传算法，未对最长的sequence加‘-’
# population:生成的size个族群, seq_lengths:初始n个sequence的长度
def initialize(sequences,size): #size是重复生成多个族群
    longest = 0
    seq_lengths = [] # 保存所有sequence的长度
    for seq in sequences:
        if len(seq) > longest:
            longest = len(seq)
        seq_lengths.append(len(seq))
    individual = []
    population = []
    for i in range(size):
        j= 0;
        for seq in sequences: 
            gaps = longest - seq_lengths[j] 
            front_gaps = random.randint(0,gaps)
            end_gaps = gaps - front_gaps
            seq = ('-'*front_gaps) + seq + ('-' * end_gaps)
            j+=1
            individual.append(seq)
        population.append(individual)
        individual= []
    return population,seq_lengths

# 计算族群匹配的得分
# score_array和族群数量size的长度一致，返回每个族群的得分列表
def calc_scores(population,gap_penalty=2,mismatch_penalty=3,match_penalty=0):
    score_array = []
    sequenceLength = len(population[0][0])
    for sequences in population:
        tmp_score = 0
        a, b = sequences[0],sequences[1]
        for index in range(sequenceLength):
            if '-' not in [str(a[index]),str(b[index])]:
                if a[index] == b[index]:
                    tmp_score += 0
                else:
                    tmp_score += mismatch_penalty

            else:
                tmpList = list(set([str(a[index]),str(b[index])]))
                tmpList.remove('-')
                if len(tmpList) == 1:
                    tmp_score += gap_penalty
                else:
                    tmp_score += 0
                    
        score_array.append(tmp_score)
        
    return score_array


# 随机选择一个族群
def selection(population):
    # 生成1-sum之间的随机数
    p = random.randint(1,len(population) )

    return (population[p-1])

# 淘汰掉表现不好的种群
def halves_of_populations(population,score_array):
    scored_population = []
    new_population = []
    index = 0
    for indiv in population:
        scored_population.append([indiv, score_array[index]])
        index += 1
    scored_population = sorted(scored_population, key=lambda a_entry: a_entry[1])
    half_of_population = scored_population[:len(scored_population) // 2]
    other_half = scored_population[len(scored_population) // 2:]

    # sum = 0
    # pr = []
    # # pr负分记为1，正分记本身
    # for i in other_half:
    #     if(i[1] < 0):
    #         space = 1
    #     else:
    #         space = i[1]
    #     sum += space + 1
    #     pr.append(sum);
    return half_of_population,other_half

def check_region(individual):
    default_start = len(individual[0])//4
    default_end = len(individual[0])//2
    return default_start,default_end

# 生成下一代
# start_index,end_index，控制中间的不变区域
def reproduce(individual1,probability):
    # start_index,end_index = check_region(individual1)
    child = []
    # temp = []

    # for seq in individual1:
        # region = seq[start_index:end_index]
        # temp.append(region)

    index = 0
    # head = ''
    # tail = ''

    for seq in individual1:
        # head = seq[:start_index]
        # tail = seq[end_index:]
        # head = swap_gaps(head)
        # tail =swap_gaps(tail)
        seq = swap_gaps(seq,probability)
        child.append(seq)
        index += 1;
    return child

# def cross (individual1,individual2):
#     # start_index,end_index = check_region(individual1)
#     child1 = []
#     child2 = []
#     child1.append(individual1[0])
#     child2.append(individual1[1])
#     # temp = []

#     # for seq in individual1:
#         # region = seq[start_index:end_index]
#         # temp.append(region)

#     # index = 0
#     # head = ''
#     # tail = ''

    
#     return child1,child2

# 交换gap的位置
def swap_gaps(seq, probability):
    new_seq = ''
    seq = list(seq)
    index =0
    while index < len(seq):
        
        if seq[index] == '-' :
            decision=random.random()
            #print(probability)
            if decision<probability:
                swap_direction = random.randint(0, 1)
                if swap_direction == 1 and index < len(seq)-1:
                    temp = seq[index+1]
                    seq[index+1] = seq[index]
                    seq[index] = temp
                elif  swap_direction == 1 and index >0:
                    temp = seq[index - 1]
                    seq[index- 1] = seq[index]
                    seq[index] = temp
        index+=1

    for letter in seq:
        new_seq+= letter
    return new_seq


# 选出最好的一个族群
def best_individual(half_of_population):
    if len(half_of_population):
        indiv = half_of_population[0]
        return indiv
    else :
        return -1

# 打印出最好的族群和分数
def print_indiv(indiv):
    score  = indiv[1]
    indiv = indiv[0]
    for seq in indiv:
        print(seq)
    print('The final penalty cost is: ', score)

# 找出所有代中匹配最好的一个
def best_among_best(indivs):
    best = indivs[0]
    score = best[1]
    for indiv in indivs:
        if indiv[1] <score:
            best = indiv
            score = indiv[1]
    return best


def genetic_algorithm(population):
    found = False
    iterarion = 0
    size = 20
    best_individuals = []

    #繁殖次数, 需要调整， 原则上是越高越好，这里为了快速得到结果设置为3次
    while (iterarion <100):
        iterarion += 1
#         if iterarion % 100 == 0:
#             print("Generation Count : " + str(iterarion))

        new_population = []

        score_array = calc_scores(population)
        #print("score_array",type(score_array))
        # if iterarion==1:
        #     print(score_array)
        # score_array1=np.array(score_array)
        # #print(score_array1)
        # #print("score_array",type(score_array1))
        # score1=score_array1/40-4
        # print(score1)
        # score2= 1/(1+np.exp(-score1))
        #print(score2.shape)
        #print(score2)
        half_of_population, other_half = halves_of_populations(population,score_array)
        best_indiv = best_individual(half_of_population)
        if best_indiv!=-1:
            best_individuals.append(best_indiv)
        else :
            print("没有人口了")
        # 在好的族群里面生成下一代孩子
        for i,x in enumerate(half_of_population):
            child = reproduce(x[0],i/len(half_of_population))
            child1 = reproduce(x[0],i/len(half_of_population))
            new_population.append(child)
            new_population.append(child1)
        # 在坏的种群里随机生成下一代孩子
        # for i in range(size//2):
        #     x = selection(other_half)
        #     child = reproduce(x[0],score2[i+len(half_of_population)])

        #     if child not in new_population:
        #         new_population.append(child)
        #     else:
        #         pass
#                 print('Child already exist')

        population = new_population
#         if iterarion % 100 == 0:
#             print(len(population))

    found = best_among_best(best_individuals)
#     print('\n\n-------------RESUTLS----------------')
#     print("The best alignment")
#     print_indiv(found)
#     print(found)
    
    return found[0],found[1]
#     print('-------------RESUTLS----------------')

from itertools import combinations
with open('MSA_database.txt') as f:
    database = f.read().splitlines()
with open('MSA_query.txt') as f:
    query = f.read().splitlines()

score_final = {}
for q in query[1:6]:
    for db in database[:10]:
        score_each = {}
        sequences = [q,db]
        size = 200  #种群数量, 可以调整， 但是在此例子中20即可
        population, seq_lengths = initialize(sequences, size)
        sequence, score = genetic_algorithm(population)
        score_each[score] = sequence
    d = sorted(score_each.items(), key=lambda d:d[0],reverse = False)
    score_final[q] = {'Sequence':d[0][1],'Score':d[0][0]}

# 在最终结果score_final中，生成的字典的值为query中的数据，共有5条
# sequence中的第二个数据为找到的匹配数据库中最相近的序列
# Score中的数字为两个sequence的惩罚分数，越小越相近
print(score_final)

## 注意繁殖次数(iterarion)，需要调整，原则上越大越好，这里设置的是50
## 种群数量size, 可以调整， 但是在此例子中20即可
## 本例为基础遗传算法，对种群的淘汰和后代的基因突变方法均可优化，这里未做深入研究。


# In[ ]:




