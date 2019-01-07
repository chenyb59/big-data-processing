import sys

like_score = ['5' , '4.5' , '4' , '3.5' , '3']
unlike_score = ['2.5' , '2' , '1.5' , '1' , '0.5']
movielist = []
userlist=[]


##  preprocess the 'ratings.csv' to a txt file , each line corresponding to one movie
def main():
    num = 0
    f = open('ratings.csv', 'r')
    result = list()
    for line in f.readlines():
        num = num + 1
        line = line.strip()
        line = line.split(',')
        if num == 1:
            continue
        if line[2] in like_score:
            content = '_'.join([line[0],'y'])
        else:
            content = '_'.join([line[0],'n'])
        if line[1] not in movielist:
            movielist.append(line[1])
            userlist.append([content])
        else:
            position = movielist.index(line[1])
            userlist[position].append(content)
    f.close()

    fw = open('ratings_out.txt','w')
    for item in userlist:
        n = 0
        for i in item:
            n = n + 1
            if n != 1:
                fw.write(',')
            fw.write(i)
        fw.write('\n')
    fw.close()



if __name__ == '__main__':
    main()
