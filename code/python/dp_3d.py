import os
import time
with open('MSA_database.txt') as f:
    database = f.read().splitlines()
with open('MSA_query.txt') as f:
    query = f.read().splitlines()

# def theta(a, b):
#     if a == '-' or b == '-':   # gap or mismatch
#         if a == '-' and b == '-': 
#             return 0
#         return 2
#     elif a == b:                         # match
#         return 0
#     else:
#         return 3
    
def theta(a, b):
      # gap or mismatch
    if a == '-' and b == '-': 
        return 0

    elif a == '-' or b == '-': 
        return 2

    elif a == b:                         # match
        return 0

    else:
        return 3
    
# def theta_3d(a, b,c):
#     return theta(a, b)+theta(a, c)+theta(b, c)

def theta_3d(a, b,c):
    if a == '-' and b == '-' or a == '-' and c == '-' or c == '-' and b == '-' : 
        return 4

    elif a == '-': 
        if b == c:                         # match
            return 4
        else:
            return 7

    elif b == '-': 
        if a == c:                         # match
            return 4
        else:
            return 7

    elif c == '-': 
        if a == b:                         # match
            return 4
        else:
            return 7
    else:
        if a==b and a==c :
            return 0
        elif a!=b and a!=c and b!=c:
            return 9
        else:
            return 6
    
        
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
    # start1 = time.perf_counter()
    sum1=0
    sum2=0
    score_mat_12, trace_mat_12=make_score_matrix(seq1, seq2)
    score_mat_13, trace_mat_13=make_score_matrix(seq1, seq3)
    score_mat_23, trace_mat_23=make_score_matrix(seq2, seq3)

    

    start2 = time.perf_counter()
    
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

                start2 = time.perf_counter()

                d1 = score_mat[i][j][k-1] + theta_3d('-','-', r)     # from up-left, mark 0
                d2 = score_mat[i-1][j][k-1] + theta_3d('-',p, r)  # from left, mark 1, gap in seq1
                d3 = score_mat[i-1][j][k] +  theta_3d('-','-', p)    # from up, mark 2, gap in seq2
                d4 = score_mat[i-1][j-1][k] +  theta_3d('-',p, q)
                d5 = score_mat[i][j-1][k] +  theta_3d('-','-', q)
                d6 = score_mat[i][j-1][k-1] +  theta_3d('-',q, r)
                d7 = score_mat[i-1][j-1][k-1] +  theta_3d(p,q, r)

                end2 = time.perf_counter()
                sum1+=end2-start2

                # start2 = time.perf_counter()

                picked = min([d1,d2,d3,d4,d5,d6,d7])
                score_mat[i][j][k] = picked
                trace_mat[i][j][k] = [d1,d2,d3,d4,d5,d6,d7].index(picked)+1   # record which direction
               #print(score_mat[i][j][k])
                # end2 = time.perf_counter()

                # sum2+=end2-start2

    print ("d1-d7耗时",str(sum1),"seconds")
    # print ("picked耗时",str(sum2),"seconds")
    return score_mat, trace_mat

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
            
    return score_mat, trace_mat

def traceback(seq1, seq2,seq3, trace_mat):
    '''
    find one optimal traceback path from trace matrix, return path code
    -!- CAUTIOUS: if multiple equally possible path exits, only return one of them -!-
    '''
    seq1, seq2 ,seq3 = '-' + seq1, '-' + seq2,'-' + seq3
    i, j,k = len(seq1) - 1, len(seq2) - 1,len(seq3) - 1
    path_code = ''
    while i > 0 or j > 0 or k > 0:
        direction = trace_mat[i][j][k]
        if direction == 1:                    # from up-left direction
            k=k-1
            path_code = '1' + path_code
        elif direction == 2:                  # from left
            i = i-1
            k = k-1
            path_code = '2' + path_code
        elif direction == 3:                  # from up
            i = i-1
            path_code = '3' + path_code
        elif direction == 4:                  # from up
            i = i-1
            j = j-1
            path_code = '4' + path_code
        elif direction == 5:                  # from up
            j = j-1
            path_code = '5' + path_code
        elif direction == 6:                  # from up
            j = j-1
            k = k-1
            path_code = '6' + path_code
        elif direction == 7:   
            i = i-1               # from up
            j = j-1
            k = k-1
            path_code = '7' + path_code


    return path_code

def print_m(seq1, seq2, m):
    """print score matrix or trace matrix"""
    seq1 = '-' + seq1; seq2 = '-' + seq2
    print()
    print(' '.join(['%3s' % i for i in ' '+seq2]))
    for i, p in enumerate(seq1):
        line = [p] + [m[i][j] for j in range(len(seq2))]
        print(' '.join(['%3s' % i for i in line]))
    print()
    return

def pretty_print_align(seq1, seq2,seq3, path_code):
    '''
    return pair alignment result string from
    path code: 0 for match, 1 for gap in seq1, 2 for gap in seq2
    '''
    align1 = ''
    middle1 = ''
    align2 = ''
    middle2 = ''
    align3 = ''
    for p in path_code:
        if p == '1':
            align1 = align1 + '-'
            align2 = align2 + '-'
            align3 = align3 + seq3[0]
            middle1 = middle1 + ' '
            middle2 = middle2 + ' '
            seq3 = seq3[1:]
            
        elif p == '2':
            align1 = align1 + seq1[0]
            align2 = align2 + '-'
            align3 = align3 + seq3[0]
            seq1 = seq1[1:]
            seq3 = seq3[1:]
            middle1 = middle1 + ' '
            middle2 = middle2 + ' '

        elif p == '3':
            align1 = align1 + seq1[0]
            align2 = align2 + '-'
            align3 = align3 + '-'
            middle1 = middle1 + ' '
            middle2 = middle2 + ' '
            seq1 = seq1[1:]

        elif p == '4':
            align1 = align1 + seq1[0]
            align2 = align2 + seq2[0]
            align3 = align3 + '-'
            if seq1[0]==seq2[0]:
                middle1 = middle1 + '|'
            else:
                middle1 = middle1 + ' '
            middle2 = middle2 + ' '
            seq1 = seq1[1:]
            seq2 = seq2[1:]

        elif p == '5':
            align1 = align1 + '-'
            align2 = align2 + seq2[0]
            align3 = align3 + '-'
            middle1 = middle1 + ' '
            middle2 = middle2 + ' '
            seq2 = seq2[1:]

        elif p == '6':
            align1 = align1 + '-'
            align2 = align2 + seq2[0]
            align3 = align3 + seq3[0]
            if seq2[0]==seq3[0]:
                middle2 = middle2 + '|'
            else:
                middle2 = middle2 + ' '
            middle1 = middle1 + ' '
            seq2 = seq2[1:]
            seq3 = seq3[1:]

        elif p == '7':
            align1 = align1 + seq1[0]
            align2 = align2 + seq2[0]
            align3 = align3 + seq3[0]
            if seq1[0]==seq2[0]:
                middle1 = middle1 + '|'
            else:
                middle1 = middle1 + ' '
            if seq2[0]==seq3[0]:
                middle2 = middle2 + '|'
            else:
                middle2 = middle2 + ' '
            
            seq1 = seq1[1:]
            seq2 = seq2[1:]
            seq3 = seq3[1:]

    print('Alignment:\n\n   ' + align1 + '\n   ' + middle1 + '\n   ' +   align2 + '\n   '+ middle2 + '\n   '+ align3)
    
    return align1,align2,align3


def calc_penalty(align1,align2):
    score = 0
    for i in range(len(align1)):
        if align1[i] == '-' or align2[i] == '-':
            score += 2
        elif align1[i] == align2[i]:
            score += 0
        else:
            score += 3
    #print(f"The final penalty cost is {score}")
    return score

def calc_penalty_3d(align1,align2,align3):
    score = 0
    for i in range(len(align1)):
        score+=theta_3d(align1[i],align2[i], align3[i])
    print(f"The final penalty cost is {score}")
    return score

def main_test():
    seq1 = 'IPZJJLMLTKJULOSTKTJOGLKJOBLTXGKTPLUWWKOMOYJBGALJUKLGLOSVHWBPGWSLUKOBSOPLOOKUKSARPPJ'
    seq2 = 'IPJTUMAOULBGAIJHUGBSOWBWLKKBGKPGTGWCIOBGXAJLGTWCBTGLWTKKKYGWPOJL'
    # seq3 ='IHOKPHYKOOOOZJJGGJMHOLZJLKOOHGBOOPZXTGWZPGMVTVPZOJJJJLSIOOGCUWOWUPLPOPULBHVTJGKZLGJGLLWXKSOJIGPSGPKOSAJKBPMGKUMPOXZGXPPP'
    # seq1 = 'KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJK'
    # seq2 = 'IPJTUMAOULBGAIJHUGBSOWBWLKKBGKPGTGWCIOBGXAJLGTWCBTGLWTKKKYGWPOJL'
    # seq3 ='WTJBGTJGJTWGBJTPKHAXHAGJJSJJPPJAPJHJHJHJHJHJHJHJHJPKSTJJUWXHGPHG'
    # seq1 = "abcd";
    # seq2 = "abdasdfasf";
    # seq3 ="acdeeee";
    # seq1 = 'ABCD'
    # seq2 = 'ACD'
    seq3 = 'BNIPMBSKHSASLLXKPIPLPUVHKHCSJCYAPLUKJGSGPGSLKUBDXGOPKLTLUCWKAUSL'
    start = time.perf_counter()
    score_mat, trace_mat = make_score_matrix_3d(seq1, seq2, seq3)
    end = time.perf_counter()
    path_code = traceback(seq1, seq2,seq3, trace_mat)
    # start = time.perf_counter()
    # end = time.perf_counter()
    print ("耗时",str(end-start),"seconds")
    align1,align2,align3 = pretty_print_align(seq1, seq2, seq3,path_code)
    calc_penalty_3d(align1, align2, align3)
    #print(score_mat[len(seq1)][len(seq2)][len(seq3)])

def visual_match(match_sequence):
    for key, value in match_sequence.items():
        print("序列" ,key,"最匹配的两条序列组合是：",value[0],"和",value[1])

def main():
    match_sequence = {}
    scores = {}
    start = time.perf_counter()
    for seq1 in query[7:9]:#7 9
        for seq2 in database:
            for seq3 in database[database.index(seq2)+1:]:
                score_mat, trace_mat = make_score_matrix_3d(seq1, seq2, seq3)
                path_code = traceback(seq1, seq2,seq3, trace_mat)
                # align1,align2 = pretty_print_align(seq1, seq2, path_code)
                scores[(seq2,seq3)] = score_mat[len(seq1)][len(seq2)][len(seq3)]
            match_sequence[seq1] = sorted(scores.items(),key=lambda x:x[1],reverse=False)[0][0]
        
        visual_match(match_sequence)
        end = time.perf_counter()
        print ("耗时",str(end-start),"seconds")
if __name__ == '__main__':
    main_test()




# n = 1
# for seq1,seq2 in match_sequence.items():
#     print(f'\n-----Query{n} best match-----')
#     score_mat, trace_mat = make_score_matrix(seq1, seq2)
#     path_code = traceback(seq1, seq2, trace_mat)
#     align1,align2 = pretty_print_align(seq1, seq2, path_code)
#     calc_penalty(align1,align2)
#     n += 1

# 单独测试用，选取query中的第一条和database里面的第一条
