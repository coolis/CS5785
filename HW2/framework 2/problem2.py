import decision_tree as dt
import scan
import utils as ut
import operator


def main():
    binary_label = True
    exclude_stopwords = False

    data = scan.scan('/Users/WayneLI/Desktop/CS5785/HW2/framework/finefoods.txt', exclude_stopwords, binary_label)
    length = len(data)

    train_data = data[:int(length*.8)]
    test_data = data[int(length*.8):]

    #decision_tree = dt.train(train_data)
    #test_results = dt.test(decision_tree, test_data)

    #print test_results
    #print data[0:5]

    #get most frequent 30 words in all reviews
    freq = ut.get_unigram_freq_all(data, -1)
    sortFreq = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
    print sortFreq[0:29]

    #get most frequent 30 words in all positive reviews
    freqPos = ut.get_unigram_freq_all(data, 1)
    sortFreqPos = sorted(freqPos.items(), key=operator.itemgetter(1), reverse=True)
    print sortFreqPos[0:29]

    #get most frequent 30 words in all negative reviews
    freqNeg = ut.get_unigram_freq_all(data, 0)
    sortFreqNeg = sorted(freqNeg.items(), key=operator.itemgetter(1), reverse=True)
    print sortFreqNeg[0:29]


    #create new word list, build up decision tree
    mergePosNeg = sortFreqNeg + sortFreqPos
    history = {}
    result = []
    for item in mergePosNeg:
        tmpWord = item[0]
        if tmpWord not in history:
            history[tmpWord] = 1
            result.append(item)
    #print result[0:30]
    wordList = result[0:5]
    #after get the world list, construct the review array with label
    #print train_data[0]
    #print train_data[0][0].split()
    for row in train_data:
        rowString = row[0]
        row[0] = rowString.split()
    #print train_data[0]
    root = dt.train(train_data, wordList)
    #dt.train(result)


    #split test list
    for row in test_data:
        rowString = row[0]
        row[0] = rowString.split()
    #test using test_data
    print test_data[0]
    acCount = 0
    for item in test_data:
        result = dt.test(item, root)
        #print result
        #print item[1]
        if result == item[1]:
            acCount += 1


    print acCount
    print len(test_data)
    print float(acCount)/float(len(test_data))


if __name__ == '__main__':
    main()
