import scan as sc
import math

# decision tree stuff
def entropy(data):
    elist = []
    freqList = []
    freqList.append(0)
    freqList.append(0)
    #compute the sum
    sumFreq = len(data)
    if sumFreq == 0:
        return 0
    #compute the freqList
    for item in data:
        if item[1] == 1:
            freqList[1] += 1
        if item[1] == 0:
            freqList[0] += 1
            
    for f in freqList:
        c = f / sumFreq
        if c == 0:
            continue
        print c
        elist.append(-c * math.log(c ,2))
    return sum(elist)

def information_gain(data, word):
    if len(data) == 0:
        return 0
    subset_entropy = 0.0

    inData = []
    notInData = []
    for item in data:
        wordList = item[0]
        if word in wordList:
            inData.append(item)
        else:
            notInData.append(item)
    dataAll = [inData, notInData]
    for tmpData in dataAll:
        val_prob        = len(tmpData) / len(data)
        subset_entropy += val_prob * entropy(tmpData)

    return (entropy(data) - subset_entropy)

# natural language processing stuff
def freq(lst):
    freq = {}
    length = len(lst)
    for ele in lst:
        if ele not in freq:
            freq[ele] = 0
        freq[ele] += 1
    return (freq, length)

def get_unigram(review):
    return freq(review.split())

def get_unigram_list(review):
    return get_unigram(review)[0].keys()
    
def get_unigram_freq_all(data, target):
    freqTotal = {}
    #reviewData = [item[0] for item in data]
    #print reviewData    
    for reviewRow in data:
        tmpFreq = get_unigram(reviewRow[0])[0]
        #print tmpFreq
        tmpScore = reviewRow[1]
        #print tmpScore
        #print target
        #tmpTar = sc.score_to_binary(tmpScore)
        if(tmpScore == target or target == -1):
            for ele in tmpFreq:
                if ele not in freqTotal:
                    freqTotal[ele] = 0
                freqTotal[ele] += tmpFreq[ele]
    return freqTotal
