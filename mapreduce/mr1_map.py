import sys


## input  = each line comprises all the users who have rated the movie
## output = produce user pairs
def main():
    for line in sys.stdin:
        line = line.strip()
        info = line.split(',')
        if len(info) != 1:
            for i in range(len(info)-1):
                for j in range(i+1 , len(info)):
                    u1 , p1 = info[i].split('_')
                    u2 , p2 = info[j].split('_')
                    if p1 == p2:
                        sys.stdout.write('{0}\t{1}\n'.format('_'.join([u1 , u2]) , 's'))
                    else:
                        sys.stdout.write('{0}\t{1}\n'.format('_'.join([u1 , u2]) , 'd'))



if __name__ == '__main__':
    main()
