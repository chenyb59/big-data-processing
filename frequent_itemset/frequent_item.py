import numpy as np


threshold = 100
threshold_2 = 20
basket = []
frequent_100 = []
candidate = []
item_count = np.zeros(10001)


##  produce each basket
for j in range(1,10001):
    itemlist = []
    for item in range(1,j+1):
        if j % item ==0:
            itemlist.append(item)
            item_count[item]=item_count[item]+1
    basket.append(itemlist)



## find the frequent item whose support is 100
for item in range(10000):
    if item_count[item] >= threshold:
        frequent_100.append(item)
print 'The frequent items whose support is 100 are : '
print frequent_100


print('---------------------------')


##  check whether input is frequent itemset
def if_check_support(s):
    support_num = 0
    for ii in basket:
        if s.issubset(ii):
            support_num = support_num + 1
        if support_num >= threshold_2:
            return True
    return False

## check whether all the subset of k-size input is in the (k-1)-size frequent itemset
def check_subset(set1 , canlist):
    re = True
    for ss in set1:
        s3 = set()
        s3.add(ss)
        s2 = set1 - s3
        if s2 not in canlist:
            re = False
            break
    return re


## find the frequent item whose support is 20
for item in range(10000):
    s1 = set()
    if item_count[item] >= threshold_2:
        s1.add(item)
        candidate.append(s1)

## find the maximum-size frequent itemset whose support is 20
for size in range(2,100):
    candidate_2 = set()
    support_list = [0]*len(basket)
    if len(candidate) == 1:
        break
    else:
        checked_set=[]
        for i in range(len(candidate)):
            for j in range(i+1 , len(candidate)):
                setl = candidate[i] | candidate[j]
                if (setl not in checked_set) & (len(setl)==size):
                    if check_subset(setl , candidate) == True:
                        if if_check_support(setl):
                            candidate_2.add(frozenset(setl))
                    checked_set.append(setl)
    if len(candidate_2) != 0:
        candidate = list(candidate_2)
    else:
        break


## print out the result
v = []
for fs in candidate:
    u = list(fs)
    u.sort()
    v.append(u)
v.sort()
print 'The maximal frequent itemset whose support is 20 are : '
print v
