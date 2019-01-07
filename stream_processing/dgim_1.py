filename = 'engg5108_stream_data.txt'
bucket = []
window = 1000
bucket_max_size = 0
bucket_max_time = 0
t = 0

##  check bucket and combine over 2 same-size buckets
def combine_bucket():
    while True:
        l = len(bucket)
        duplicates = 0
        for i in range(l-1 , 1 , -1):
            if bucket[i][0] == bucket[i-1][0] & bucket[i-1][0] == bucket[i-2][0]:
                duplicates = 1
                break
        if duplicates:
            bucket[i-2][0] = bucket[i-2][0] + 1
            del bucket[i-1]
        else:
            break

def cal_last_1000_bits():
    sum = 0
    for i in range(len(bucket)):
        sum = sum + pow(2 , bucket[i][0])
        print pow(2 , bucket[i][0])
    print pow(2 , (bucket_max_size+1))/2
    print('for the last one thousand bits , the estimated number of 1s is : '), sum + pow(2 , (bucket_max_size+1))/2


## read the stream and update the bucket when '1' comes
with open(filename) as f:
    while True:
        input = f.read(1)
        if not input:
            print "End of file"
            break
        t = t + 1
        if t - bucket_max_time > window:
            del bucket[0]
        if input == '1':
            bucket.append([ 0 , t ])
            combine_bucket()
            bucket_max_size = bucket[0][0]
            bucket_max_time = bucket[0][1]
            for i in range(len(bucket)):
                print pow(2,bucket[len(bucket)-1-i][0]),
            print '\n'


        #print '-----------------'
        #    print 'Bucket {0}\t{1:<6}\t{2:<6}'.format(i,pow(2,bucket[len(bucket)-1-i][0]),bucket[len(bucket)-1-i][1])


f.close()

print('the final buckets are : ')
print bucket

##  description  :  print the size and end timestamp of each bucket
print '                size    end timestamp'
for i in range(len(bucket)):
    print 'Bucket {0}\t{1:<6}\t{2:<6}'.format(i,pow(2,bucket[len(bucket)-1-i][0]),bucket[len(bucket)-1-i][1])

##  estimation  :  estimate how much '1' in the last 1000 bits
cal_last_1000_bits()
