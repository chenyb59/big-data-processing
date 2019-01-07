#!/usr/bin/python
import sys

similarity = 0

##  calculate the similarity between two users according to their same and different preference
def main():
    k = ''
    lastk = ''
    samenum = 0
    diffnum = 0
    for line in sys.stdin:
        line = line.strip()
        info = line.split('\t')
        k = info[0]
        if lastk =='':
            lastk = k
        if lastk != k:
            u = lastk.split('_')
            similarity = (samenum)/float(samenum + diffnum)
            sys.stdout.write('{0}\t{1:.4f}\n'.format(' & '.join([u[0] , u[1]]) , similarity))
            lastk = k
            samenum = 0
            diffnum = 0
        if info[1] == 's':
            samenum = samenum +1
        else:
            diffnum = diffnum +1
    u = lastk.split('_')
    similarity = (samenum)/float(samenum + diffnum)
    sys.stdout.write('{0}\t{1:.4f}\n'.format(' & '.join([u[0] , u[1]]) , similarity))



if __name__ == '__main__':
    main()
