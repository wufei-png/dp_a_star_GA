import os
from queue import PriorityQueue
import time
with open('MSA_database.txt') as f:
    database = f.read().splitlines()
with open('MSA_query.txt') as f:
    query = f.read().splitlines()

def theta(a, b):
    if a == '-' or b == '-':   # gap or mismatch
        return 2
    elif a == b:                         # match
        return 0
    else:
        return 3
			

def make_score_matrix(seq1, seq2):
    """
    return score matrix and map(each score from which direction)
    0: diagnosis
    1: up
    2: left
    """
    seq1 = '-' + seq1
    seq2 = '-' + seq2
    score_mat = {}
    trace_mat = {}

    for i,p in enumerate(seq1):
        score_mat[i] = {}
        trace_mat[i] = {}
        for j,q in enumerate(seq2):
            if i == 0:                    # first row, gap in seq1
                score_mat[i][j] = 2*j
                trace_mat[i][j] = 1
                continue
            if j == 0:                    # first column, gap in seq2
                score_mat[i][j] = 2*i
                trace_mat[i][j] = 2
                continue
            ul = score_mat[i-1][j-1] + theta(p, q)     # from up-left, mark 0
            l  = score_mat[i][j-1]   + theta('-', q)   # from left, mark 1, gap in seq1
            u  = score_mat[i-1][j]   + theta(p, '-')   # from up, mark 2, gap in seq2
            picked = min([ul,l,u])
            score_mat[i][j] = picked
            trace_mat[i][j] = [ul, l, u].index(picked)   # record which direction
    #print(trace_mat )
    return score_mat, trace_mat


def H_cost(seq1, seq2,direction):
    """
    return score matrix and map(each score from which direction)
    0: diagnosis
    1: up
    2: left
    """
    if direction==0:
        seq1=seq1[1:]
        seq2=seq2[1:]
    if direction==1:
        seq2=seq2[1:]
    if direction==2:
        seq1=seq1[1:]
    score_mat, trace_mat = make_score_matrix(seq1, seq2)
    return score_mat[len(seq1)][len(seq2)]

# def A_cost(score_mat,seq1,seq2,i,j):
#     A1=score_mat[i][j+1]+H_cost(seq1[i:], seq2[j+1:])
#     A2=score_mat[i+1][j]+H_cost(seq1[i+1:], seq2[j:])
#     A0=score_mat[i+1][j+1]+H_cost(seq1[i+1:], seq2[j+1:])
#     picked = min([A0,A1,A2])
#     # return [A0,A1,A2].index(picked)
#     return picked

def fromwhere(i1,j1,i,j):
    if i1==i and j1+1==j:
        return 1
    elif i1+1==i and j1+1==j:
        return 0
    elif i1+1==i and j1==j:
        return 2

def cost_point_to_point(seq1,seq2,current,direction):
  
  if direction==0:
    if seq1[current[0]]==seq2[current[1]]:
      return 0
    else :
      return 3
  else :
    return 2

def astar_2d(seq1, seq2):
    frontier = PriorityQueue()
    start=(0,0)
    frontier.put((0,start))
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0
    goal=(len(seq1),len(seq2))
    path_code=''
    while not frontier.empty():
        current = frontier.get()
        #print(current)
        
        if current[1] == goal:
            break
        i=current[1][0]
        j=current[1][1]
        #print(333)
        #print("i,j:",i,j)
        if i+1<=len(seq1) and j+1<=len(seq2):
            newnodes=[(i+1,j),(i,j+1),(i+1,j+1)]
        elif i+1>len(seq1) and j+1<=len(seq2):
            newnodes=[(i,j+1)]
        elif i+1<=len(seq1) and j+1> len(seq2):
            newnodes=[(i+1,j)]
        for next in newnodes:
            direction=fromwhere(i,j,next[0],next[1])
            new_cost =  cost_so_far[current[1]]+ cost_point_to_point(seq1,seq2,current[1],direction)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost+H_cost(seq1[i:],seq2[j:],direction)
                frontier.put((priority,next))
                came_from[next] = current
    cost=cost_so_far[goal]
    buff=came_from[goal]
    path_code=str(fromwhere(buff[1][0], buff[1][1], goal[0], goal[1]))+path_code
    while buff[1]!=start:
        buff_up=came_from[buff[1]]
        path_code=str(fromwhere(buff_up[1][0], buff_up[1][1],buff[1][0], buff[1][1]))+path_code
        buff=buff_up
    return path_code,cost

# def star_2d(seq1, seq2, score_mat):
#     '''
#     find one optimal traceback path from trace matrix, return path code
#     -!- CAUTIOUS: if multiple equally possible path exits, only return one of them -!-
#     '''
    
#     i, j = 0, 0
#     path_code = ''
#     came_from={}
#     openlist=[]
#     closelist=[]
#     came_from[start] = None
#     openlist.append(0,[0,0])
    
#     while  len(openlist):
#             i=q.get()[1][0]
#             j=q.get()[1][1]

#             if i==len(seq1) and j==len(seq2):#end
#                 while i > 0 or j > 0:
#                     i1,j1=comefrom[(i,j)]
#                     direction=fromwhere(i1,j1,i,j)
#                     path_code =  path_code+ direction
#                     i,j=i1,j1
#                 return path_code
#             newnodes=[(i+1,j),(i,j+1),(i+1,j+1)]
#             for node in newnodes:


    # while i <len(seq1) or j <len(seq2):
    #     direction = A_cost(score_mat,seq1,seq2,i,j)
    #     if direction == 0:                    # from up-left direction
    #         i=i+1
    #         j=j+1
    #         path_code =  path_code+'0'
    #     elif direction == 1:                  # from left
    #         j=j+1
    #         path_code = path_code+'1' 
    #     elif direction == 2:                  # from up
    #         i=i+1
    #         path_code = path_code+'2'
    #     if i ==len(seq1):
    #       while j <len(seq2):
    #         j=j+1
    #         path_code = path_code+'1' 
    #       return path_code
    #     if j ==len(seq2):
    #       while i <len(seq1):
    #         i=i+1
    #         path_code = path_code+'2'
    #       return path_code
    # return path_code

def pretty_print_align(seq1, seq2, path_code):
    '''
    return pair alignment result string from
    path code: 0 for match, 1 for gap in seq1, 2 for gap in seq2
    '''
    align1 = ''
    middle = ''
    align2 = ''
    for p in path_code:
        if p == '0':
            align1 = align1 + seq1[0]
            align2 = align2 + seq2[0]
            if seq1[0] == seq2[0]:
                middle = middle + '|'
            else:
                middle = middle + ' '
            seq1 = seq1[1:]
            seq2 = seq2[1:]
        elif p == '1':
            align1 = align1 + '-'
            align2 = align2 + seq2[0]
            middle = middle + ' '
            seq2 = seq2[1:]
        elif p == '2':
            align1 = align1 + seq1[0]
            align2 = align2 + '-'
            middle = middle + ' '
            seq1 = seq1[1:]

    print('Alignment:\n\n   ' + align1 + '\n   ' + middle + '\n   ' + align2)
    
    return align1,align2

def calc_penalty(align1,align2):
    score = 0
    for i in range(len(align1)):
        if align1[i] == '-' or align2[i] == '-':
            score += 2
        elif align1[i] == align2[i]:
            score += 0
        else:
            score += 3
    print(f"The final penalty cost is {score}")
    return score

def visual_match(match_sequence):
    for key, value in match_sequence.items():
        print("序列" ,key,"最匹配的序列是：",value)

def main():
    match_sequence = {}
    scores = {}
    start = time.perf_counter()
    for seq1 in query[1:6]:
        for seq2 in database[0:10]:
            path_code,cost=astar_2d(seq1, seq2)
            # path_code = traceback(seq1, seq2, trace_mat)
            # align1,align2 = pretty_print_align(seq1, seq2, path_code)
            scores[seq2] = cost
        match_sequence[seq1] = sorted(scores.items(),key=lambda x:x[1],reverse=False)[0][0]
        #print(type(match_sequence))
        visual_match(match_sequence)
        end = time.perf_counter()
        print ("耗时",str(end-start),"seconds")   

def main_test():
    seq1 = 'KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJKPXKJXXJAJKHXKJXX'
    seq2 ='IWTJBGTJGJTWGBJTPKHAXHAGJJSJJPPJAPJHJHJHJHJHJHJHJHJPKSTJJUWXHGPHGALKLPJTPJPGVXPLBJHHJPKWPPDJSG'
    # seq2 ='IWTJBGTJGJTWGBJTPKHAXHAGJJSJJPPJAPJHJHJHJHJHJHJHJHJPKSTJJUWXHGPHGALKLPJTPJPGVXPLBJHHJPKWPPDJSG'
    # seq1 = 'AA'
    # seq2 = 'BC'
    start = time.perf_counter()
    path_code,cost=astar_2d(seq1, seq2)
    print("path_code:",path_code,"cost:",cost)
    # path_code = star_2d(seq1, seq2, score_mat)
    # print(path_code)
    align1,align2 = pretty_print_align(seq1, seq2, path_code)
    # calc_penalty(align1,align2)
    end = time.perf_counter()
    print ("耗时",str(end-start),"seconds")  
if __name__ == '__main__':
    main_test()