#!/usr/bin/env python
# coding: utf-8

# In[8]:


import random
import time
def read_sequences(path):
    k = 0
    sequences = []
    with open(path,'r') as reader:
        for text in reader:
            text= text.replace('\n','')
            text = text.upper()
            sequences.append(text)
            k+=1
    return sequences,k

def initialize(sequences,size): 
    longest = 0
    seq_lengths = []
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

# 感觉是计算得分的，最终返回一个得分矩阵
# score_array和族群数量size的长度一致，返回每个三族群的得分列表
def calc_scores(population,gap_penalty=2,mismatch_penalty=3,match_penalty=0):
    score_array = []
    sequenceLength = len(population[0][0])
    for sequences in population:
        tmp_score = 0
        a, b, c = sequences[0],sequences[1],sequences[2]
        for index in range(sequenceLength):
            if '-' not in [str(a[index]),str(b[index]),str(c[index])]:
                if a[index] == b[index] and a[index] == c[index] and b[index] == c[index]:
                    tmp_score += 0
                elif a[index] != b[index] and a[index] != c[index] and b[index] != c[index]:
                    tmp_score += mismatch_penalty*3
                else:
                    tmp_score += mismatch_penalty*2
            else:
                tmpList = list(set([str(a[index]),str(b[index]),str(c[index])]))
                tmpList.remove('-')
                if len(tmpList) == 1:
                    tmp_score += gap_penalty*2
                elif len(tmpList) == 2 and tmpList[0] == tmpList[1]:
                    tmp_score += gap_penalty*2
                elif len(tmpList) == 2 and tmpList[0] != tmpList[1]:
                    tmp_score = tmp_score + gap_penalty*2 + mismatch_penalty
                else:
                    print('!!!!Here is a ERROR!!!')
                    
        score_array.append(tmp_score)
        
    return score_array


def selection(population):
    # 生成1-sum之间的随机数
    p = random.randint(1,len(population) )

    return (population[p-1])

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

def reproduce(individual1):
    start_index,end_index = check_region(individual1)
    child = []
    temp = []

    for seq in individual1:
        region = seq[start_index:end_index]
        temp.append(region)

    index = 0
    head = ''
    tail = ''

    for seq in individual1:
        head = seq[:start_index]
        tail = seq[end_index:]
        head = swap_gaps(head)
        tail =swap_gaps(tail)
        seq = head + temp[index] + tail
        child.append(seq)
        index += 1;
    return child


def swap_gaps(seq):
    new_seq = ''
    seq = list(seq)
    index =0
    while index < len(seq):
        if seq[index] == '-':
            swap_direction = random.randint(0, 1)
            if swap_direction == 1 and index < len(seq)-1:
                temp = seq[index+1]
                seq[index+1] = seq[index]
                seq[index] = temp
            elif index >0:
                temp = seq[index - 1]
                seq[index- 1] = seq[index]
                seq[index] = temp
        index+=1

    for letter in seq:
        new_seq+= letter
    return new_seq


def best_individual(half_of_population):
    indiv = half_of_population[0]
    return indiv

def print_indiv(indiv):
    score  = indiv[1]
    indiv = indiv[0]
    for seq in indiv:
        print(seq)
    print('The final penalty cost is: ', score)

def best_among_best(indivs):
    score = 0
    best = indivs[0]

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
    while (iterarion < 500):
        iterarion += 1
#         if iterarion % 100 == 0:
#             print("Generation Count : " + str(iterarion))

        new_population = []
        score_array = calc_scores(population)
        half_of_population, other_half = halves_of_populations(population,score_array)
        best_indiv = best_individual(half_of_population)
        best_individuals.append(best_indiv)

        for x in half_of_population:
            child = reproduce(x[0])
            new_population.append(child)
        for i in range(size//2):
            x = selection(other_half)
            child = reproduce(x[0])

            if child not in new_population:
                new_population.append(child)
            else:
                pass
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
for q in query[7:10]:
    for db in list(combinations(database[:10],2)):
        score_each = {}
        sequences = []
        for i in [q,db[0],db[1]]:
            sequences.append(i)
        size =20  
        population, seq_lengths = initialize(sequences, size)
        sequence, score = genetic_algorithm(population)
        score_each[score] = sequence
    d = sorted(score_each.items(), key=lambda d:d[0],reverse = False)
    score_final[q] = {'Sequence':d[0][1],'Score':d[0][0]}
    
print(score_final)


# In[ ]:




