import scan
import utils as ut

class DecisionTree:
    node_label = None  # takes the values 0, 1, None. If has the values 0 or 1, then this is a leaf
    left = None
    right = None
    word = None

    def go(self, review):
        if self.node_label == 1 or self.node_label == 0:
            return self.node_label
        else:
            if self.word[0] in review:
                return self.left.go(review)
            else:
                return self.right.go(review)

# http://en.wikipedia.org/wiki/ID3_algorithm
def train(data, wordList):
    #raise 'not implemented'
    if not wordList: return
    #find maximal information gain
    maxWord = None
    maxGain = None
    for word in wordList:
        tmpGain = ut.information_gain(data, word)
        if tmpGain > maxGain: 
            maxGain = tmpGain
            maxWord = word
   
    #iterate to get leftData and rightData
    leftData = []
    rightData = []
    for item in data:
        if maxWord not in item[0]:
            leftData.append(item)
        else:
            rightData.append(item)
    #build root node
    root = DecisionTree()
    if len(wordList) == 1:
        root.word = wordList[0]
        #root.node_label = -1
        #see if node_label should be one or 1
        #count 0 and 1
        countOne = 0
        for row in data:
            if row[1] == 1:
                countOne += 1
        if countOne >= len(data)/2:
            root.node_label = 1
        else:
            root.node_label = 0
        
    else:
        root.node_label = -1
        #delete maxWord in wordList, recursion
        wordList.remove(maxWord)
        root.left = train(leftData, wordList)
        root.right = train(rightData, wordList)
        root.word = maxWord
    
    return root

def test(item, root):
    tmpRev = item[0]
    return root.go(tmpRev)

