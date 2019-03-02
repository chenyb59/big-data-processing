#!/usr/bin/env python
import re, sys
from pyspark import SparkContext
from operator import add



def split_follow(follows):
    info = re.split(r'\s+', follows)
    # info = follows.split(' ')
    return info[0], info[1]


def compute_out_rank(follows, rank):
    num_follows = len(follows)
    for usr in follows:
        yield (usr, rank / num_follows)


def main():
    if len(sys.argv) < 2:
        print >> sys.stderr, "InputFormat: pagerank <master> <file> "
        exit(-1)

    # Initialize the spark context.
    sc = SparkContext(sys.argv[1], "TwitterPagerank")

    # Loads in input file. It should be in format of:
    #     user1         follow userID
    #     user2         follow userID
    #     user3         follow userID
    #     ...
    lines = sc.textFile(sys.argv[2], 1)

    # Loads all followed users from input file and aggregate into one table groupby key:
    #     user1         user2 , user3 , user4...
    #     user2         user1 , user3 , ...
    #     ...
    follow_table = lines.map(lambda follows: split_follow(follows)).distinct().groupByKey().cache()

    # initialize ranks of all users 1/N (N denotes the total number of users)
    r1 = lines.flatMap(lambda follows: split_follow(follows)).distinct()
    num = r1.count()
    ranks = r1.map(lambda usr : (usr, 1.0/num))



    # Calculates and updates user ranks continuously using PageRank algorithm.
    # the updating process would not terminate until the change of ranks smaller than threshold.
    # set alpha = 0.85 , to deal with dead end nodes and spider traps. The leaked ranks are re-insert to all the nodes in avarage.
    alpha = 0.85
    not_finished = True
    threshold = 0.01
    round = 0
    # write the output into a local file
    f = open('log_pg2.txt','w')

    while not_finished:
        round  = round + 1
        # Calculates ranks of out-degree nodes.
        out_ranks = follow_table.join(ranks).flatMap(lambda (usr, (follows, rank)) : compute_out_rank(follows, rank))
        # Combine the result by key and sum them up.
        # multiply with alpha
        r2 = out_ranks.reduceByKey(add).mapValues(lambda rank: rank * alpha)

        # compute the leaked rank and add them back to make sure the total rank is 1.
        leak = 1 - r2.values().sum()
        if leak > 0 :
            # r3 = r1.map(lambda usr : (usr , float(leak / num))).union(r2).reduceByKey(add)
            r3 = r1.mapValues(lambda rank : rank + float(leak / num))
        else:
            r3 = r2

        # compute the difference ranks between this round and last round , decide whether to end the loop.
        diff = r3.join(ranks).mapValues(lambda (a , b) : abs(a - b)).values().sum()
        print 'round',round
        print 'diff',diff
        f.write(str(round)+'\t'+str(diff)+'\n')
        if diff < threshold:
            not_finished = False
        ranks = r3

    f.write('output'+'\n')

    # Sort the result by rank values , and save the first 10000 users and ranks.
    top1w = ranks.takeOrdered(10000, key = lambda x: -x[1])
    print 'Top 10000 rank : '
    for (usr, rank) in top1w:
        print "%s has rank: %s." % (usr, rank)
        f.write(str(usr)+' : '+str(rank)+'\n')

    f.close()



if __name__ == "__main__":
    main()
