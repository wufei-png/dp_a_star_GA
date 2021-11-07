import os
from queue import PriorityQueue
import time
with open('MSA_database.txt') as f:
    database = f.read().splitlines()
with open('MSA_query.txt') as f:
    query = f.read().splitlines()

def theta(a, b):
    if a == '-' or b == '-':   # gap or mismatch
        if a == '-' and b == '-': 
            return 0
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

def theta_3d(a, b,c):
    return theta(a, b)+theta(a, c)+theta(b, c)
# score_mat，用来记录每个格子的分值；
# trace_mat，用来记录相应格子里的theta值是由哪个方向计算而来
# gap是2分，mismatch是3分，相等是0分
def make_score_matrix_3d(seq1, seq2,seq3):
    """
    return score matrix and map(each score from which direction)
    0: diagnosis
    1: up
    2: left
    """

    score_mat_12, trace_mat_12=make_score_matrix(seq1, seq2)
    score_mat_13, trace_mat_13=make_score_matrix(seq1, seq3)
    score_mat_23, trace_mat_23=make_score_matrix(seq2, seq3)
    seq1 = '-' + seq1
    seq2 = '-' + seq2
    seq3 = '-' + seq3
    score_mat = {}
    trace_mat = {}
    for i,p in enumerate(seq1):
        score_mat[i] = {}
        trace_mat[i] = {}
        for j,q in enumerate(seq2):
            score_mat[i][j] = {}
            trace_mat[i][j] = {}
            for k,r in enumerate(seq3):
                if i == 0:                    # first row, gap in seq1
                    score_mat[i][j][k] = score_mat_23[j][k]+2*(j+k)
                    if  trace_mat_23[j][k]==1:
                        trace_mat[i][j][k] = 1
                    elif trace_mat_23[j][k]==2:
                         trace_mat[i][j][k] = 5
                    else:
                        trace_mat[i][j][k] = 6
                    continue

                if j == 0:                    # first column, gap in seq2
                    score_mat[i][j][k] = score_mat_13[i][k]+2*(i+k)
                    if  trace_mat_13[i][k]==1:
                        trace_mat[i][j][k] = 1
                    elif trace_mat_13[i][k]==2:
                         trace_mat[i][j][k] = 3
                    else:
                        trace_mat[i][j][k] = 2
                    continue

                if k == 0:                    # first column, gap in seq2
                    score_mat[i][j][k] = score_mat_12[i][j]+2*(i+j)
                    if  trace_mat_12[i][j]==1:
                        trace_mat[i][j][k] = 5
                    elif trace_mat_12[i][j]==2:
                         trace_mat[i][j][k] = 3
                    else:
                        trace_mat[i][j][k] = 4
                    continue
                d1 = score_mat[i][j][k-1] + theta_3d('-','-', r)     # from up-left, mark 0
                d2 = score_mat[i-1][j][k-1] + theta_3d('-',p, r)  # from left, mark 1, gap in seq1
                d3 = score_mat[i-1][j][k] +  theta_3d('-','-', p)    # from up, mark 2, gap in seq2
                d4 = score_mat[i-1][j-1][k] +  theta_3d('-',p, q)
                d5 = score_mat[i][j-1][k] +  theta_3d('-','-', q)
                d6 = score_mat[i][j-1][k-1] +  theta_3d('-',q, r)
                d7 = score_mat[i-1][j-1][k-1] +  theta_3d(p,q, r)
                picked = min([d1,d2,d3,d4,d5,d6,d7])
                score_mat[i][j][k] = picked
                trace_mat[i][j][k] = [d1,d2,d3,d4,d5,d6,d7].index(picked)+1   # record which direction
    return score_mat, trace_mat


def H_cost(seq1, seq2,seq3,direction):
    """
    return score matrix and map(each score from which direction)
    0: diagnosis
    1: up
    2: left
    """
    if direction==1:
        seq3=seq3[1:]

    if direction==2:
        seq1=seq1[1:]
        seq3=seq3[1:]

    if direction==3:
        seq1=seq1[1:]

    if direction==4:
        seq1=seq1[1:]
        seq2=seq2[1:]

    if direction==5:
        seq2=seq2[1:]

    if direction==6:
        seq2=seq2[1:]
        seq3=seq3[1:]

    if direction==7:
        seq1=seq1[1:]
        seq2=seq2[1:]
        seq3=seq3[1:]
    # score_mat, trace_mat= make_score_matrix(seq1,seq2,seq3)
    # return score_mat[len(seq1)][len(seq2)][len(seq3)]
    score_mat12, trace_mat12 = make_score_matrix(seq1, seq2)
    score_mat13, trace_mat13 = make_score_matrix(seq1, seq3)
    score_mat23, trace_mat23 = make_score_matrix(seq2, seq3)
    return score_mat12[len(seq1)][len(seq2)]+score_mat13[len(seq1)][len(seq3)]+score_mat23[len(seq2)][len(seq3)]



def fromwhere(i1,j1,k1,i,j,k):
    if i1==i and j1==j and k1+1==k:
        return 1
    if i1+1==i and j1==j and k1+1==k:
        return 2
    if i1+1==i and j1==j and k1==k:
        return 3
    if i1+1==i and j1+1==j and k1==k:
        return 4
    if i1==i and j1+1==j and k1==k:
        return 5
    if i1==i and j1+1==j and k1+1==k:
        return 6
    if i1+1==i and j1+1==j and k1+1==k:
        return 7
        

def cost_point_to_point(seq1,seq2,seq3,current,direction):

    if direction==1 or direction==3 or direction==5:
        return 4

    if direction==2:
        if seq1[current[0]]==seq3[current[2]]:
            return 4
        else :
            return 7
            
    if direction==4:
        if seq1[current[0]]==seq2[current[1]]:
            return 4
        else :
            return 7

    if direction==6:
        if seq2[current[1]]==seq3[current[2]]:
            return 4
        else :
            return 7

    if direction==7:
        return theta_3d(seq1[current[0]],seq2[current[1]], seq3[current[2]])
    


def astar_3d(seq1, seq2,seq3):
    frontier = PriorityQueue()
    start=(0,0,0)
    frontier.put((0,start))
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0
    goal=(len(seq1),len(seq2),len(seq3))
    path_code=''
    while not frontier.empty():
        current = frontier.get()
        #print(current)
        
        if current[1] == goal:
            break
        i=current[1][0]
        j=current[1][1]
        k=current[1][2]
        #print(333)
        #print("i,j:",i,j)
        newnodes=[(i+1,j,k),(i,j+1,k),(i,j,k+1),(i+1,j+1,k),(i+1,j,k+1),(i,j+1,k+1),(i+1,j+1,k+1)]
        if i+1>len(seq1):
            if (i+1,j,k) in newnodes:
                newnodes.remove((i+1,j,k))
            if (i+1,j+1,k) in newnodes:
                newnodes.remove((i+1,j+1,k))
            if (i+1,j,k+1) in newnodes:
                newnodes.remove((i+1,j,k+1))
            if (i+1,j+1,k+1) in newnodes:
                newnodes.remove((i+1,j+1,k+1))

        if j+1>len(seq2):
            if (i,j+1,k) in newnodes:
                newnodes.remove((i,j+1,k))
            if (i+1,j+1,k) in newnodes:
                newnodes.remove((i+1,j+1,k))
            if (i,j+1,k+1) in newnodes:
                newnodes.remove((i,j+1,k+1))
            if (i+1,j+1,k+1) in newnodes:
                newnodes.remove((i+1,j+1,k+1))


        if k+1>len(seq3):
            if (i,j,k+1) in newnodes:
                newnodes.remove((i,j,k+1))
            if (i+1,j,k+1) in newnodes:
                newnodes.remove((i+1,j,k+1))
            if (i,j+1,k+1) in newnodes:
                newnodes.remove((i,j+1,k+1))
            if (i+1,j+1,k+1) in newnodes:
                newnodes.remove((i+1,j+1,k+1))
            
        for next in newnodes:
            direction=fromwhere(i,j,k,next[0],next[1],next[2])
            #print(direction)
            #print(type(cost_so_far[current[1]]))
            #print(direction)
            new_cost =  cost_so_far[current[1]]+ cost_point_to_point(seq1,seq2,seq3,current[1],direction)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                #print(H_cost(seq1[i:],seq2[j:],seq3[k:],direction))
                priority = new_cost+H_cost(seq1[i:],seq2[j:],seq3[k:],direction)
                frontier.put((priority,next))
                came_from[next] = current
    cost=cost_so_far[goal]
    buff=came_from[goal]
    path_code=path_code+str(fromwhere(buff[1][0], buff[1][1], buff[1][2], goal[0], goal[1],goal[2]))
    while buff[1]!=start:
        buff_up=came_from[buff[1]]
        path_code=path_code+str(fromwhere(buff_up[1][0], buff_up[1][1],buff_up[1][2],buff[1][0], buff[1][1],buff[1][2]))
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

def main_test():
    seq1 = "IPZJJLMLTKJULOSTKTJOGLKJOBLTXGKTPLUWWKOMOYJBGALJUKLGLOSVHWBPGWSLUKOBSOPLOOKUKSARPPJ"
    seq2 = "IPJTUMAOULBGAIJHUGBSOWBWLKKBGKPGTGWCIOBGXAJLGTWCBTGLWTKKKYGWPOJL"
    seq3 = "BNIPMBSKHSASLLXKPIPLPUVHKHCSJCYAPLUKJGSGPGSLKUBDXGOPKLTLUCWKAUSL"
    # seq1 = 'AA'
    # seq2 = 'BC'
    # seq1 = 'ABCD'
    # seq2 = 'ACD'
    # seq3 = 'BCDFFFE'
    start = time.perf_counter()
    path_code,cost=astar_3d(seq1, seq2,seq3)
    end =  time.perf_counter()
    print ("耗时",str(end-start),"seconds")
    print("path_code:",path_code,"cost:",cost)
    # path_code = star_2d(seq1, seq2, score_mat)
    # print(path_code)
    # align1,align2 = pretty_print_align(seq1, seq2, path_code)
    # calc_penalty(align1,align2)

if __name__ == '__main__':
    main_test()