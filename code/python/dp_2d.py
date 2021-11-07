import os
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
    

# score_mat，用来记录每个格子的分值；
# trace_mat，用来记录相应格子里的theta值是由哪个方向计算而来
# gap是2分，mismatch是3分，相等是0分
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


def traceback(seq1, seq2, trace_mat):
    '''
    find one optimal traceback path from trace matrix, return path code
    -!- CAUTIOUS: if multiple equally possible path exits, only return one of them -!-
    '''
    seq1, seq2 = '-' + seq1, '-' + seq2
    i, j = len(seq1) - 1, len(seq2) - 1
    path_code = ''
    while i > 0 or j > 0:
        #print("trace_mat:",trace_mat[i][j],i,j)
        direction = trace_mat[i][j]
        if direction == 0:                    # from up-left direction
            i = i-1
            j = j-1
            path_code = '0' + path_code
        elif direction == 1:                  # from left
            j = j-1
            path_code = '1' + path_code
        elif direction == 2:                  # from up
            i = i-1
            path_code = '2' + path_code
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
    seq1 = 'KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJKPXKJXXJAJKHXKJXX'
    seq2 ='IWTJBGTJGJTWGBJTPKHAXHAGJJSJJPPJAPJHJHJHJHJHJHJHJHJPKSTJJUWXHGPHGALKLPJTPJPGVXPLBJHHJPKWPPDJSG'
    # seq2 = 'IPJTUMAOULBGAIJHUGBSOWBWLKKBGKPGTGWCIOBGXAJLGTWCBTGLWTKKKYGWPOJL'
    # seq1 = 'IPZJJLMLTKJULOSTKTJOGLKJOBLTXGKTPLUWWKOMOYJBGALJUKLGLOSVHWBPGWSLUKOBSOPLOOKUKSARPPJ'
    # seq2 = 'IPOKJOLKHPZUOZJOGGUSPXLOHLTUTOGKJOTOXPGGZPGPVPHOSOJMOJOSIOMGCWWOWUPPPOGULWHVLJGKPLMMMMMMMMDDDDDDDDDDDDDDDDDDDDDDDDDD'
    # print(len(seq1),len(seq2))
    start = time.perf_counter()
    score_mat, trace_mat = make_score_matrix(seq1, seq2)
    print(score_mat[len(seq1)][len(seq2)])
    # score_mat, trace_mat = make_score_matrix_2d(seq1, seq2)
    end = time.perf_counter()
    path_code = traceback(seq1, seq2, trace_mat)
    #print("pathcode:",path_code)
    align1,align2 = pretty_print_align(seq1, seq2, path_code)
    #calc_penalty(align1,align2)
    
    print ("耗时",str(end-start),"seconds")   

def visual_match(match_sequence):
    for key, value in match_sequence.items():
        print("序列" ,key,"最匹配的序列是：",value[0],"cost是",value[1])
        
def main():
    match_sequence = {}
    scores = {}
    start = time.perf_counter()
    for seq1 in query[1:6]:
        for seq2 in database:
            score_mat, trace_mat = make_score_matrix(seq1, seq2)
            # path_code = traceback(seq1, seq2, trace_mat)
            # align1,align2 = pretty_print_align(seq1, seq2, path_code)
            scores[seq2] = score_mat[len(seq1)][len(seq2)]
        match_sequence[seq1] = sorted(scores.items(),key=lambda x:x[1],reverse=False)[0]
        #print(type(match_sequence))

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
