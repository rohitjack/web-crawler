import pandas as pd
import re
# Iterative longest contiguous sequence. No one character matchings
def lcs(s1,s2):
    longest = ""
    i = 0
    #print(type(s1))
    try:
        for x in s1:
            if re.search(x, s2):
              s= x
              while re.search(s, s2):
                if len(s)>len(longest):
                    longest = s
                if i+len(s) == len(s1):
                    break
                s = s1[i:i+len(s)+1]
            i += 1
        return longest
    except:
        print(s1)
        return longest

def iterLCS(pdf):
    try:
        posCounter = 1
        sw1Orig = pdf['Root Word']
        sw2Orig = pdf['Full Word']
        sw1 = pdf['Root Word']
        sw2 = pdf['Full Word']
        longDict = dict()
        prevSInd = 0
        prevTInd = 0
        rejLength =0

        while True:
            tempVal = lcs(sw1Orig,sw2Orig)
            if len(tempVal)  <= 1:
                break

            tempSInd =  pdf['Root Word'].find(tempVal) + 1
            tempTInd =  pdf['Full Word'].find(tempVal) + 1
            if (tempSInd - prevSInd)*(tempTInd - prevTInd) < 0:
                print('here',tempVal,pdf['Root Word'],pdf['Full Word'])
                sw1Orig = sw1Orig.replace(tempVal,'~~',1)
                sw2Orig = sw2Orig.replace(tempVal,'^^',1)
                rejLength += len(tempVal)
            else:
                longDict[tempSInd] = tempVal+'#'+str(posCounter)
                sw1 = sw1.replace(tempVal,'#'+str(posCounter)+'#',1)
                sw2 = sw2.replace(tempVal,'!'+str(posCounter)+'!',1)
                sw1Orig = sw1Orig.replace(tempVal,'~'+str(posCounter)+'~',1)
                sw2Orig = sw2Orig.replace(tempVal,'^'+str(posCounter)+'^',1)
                prevSInd = tempSInd + 1
                prevTInd = tempTInd + 1
                posCounter += 1

        #return [longList,[item for item in sw1.split('#') if len(item) > 0],[item for item in sw2.split('!') if len(item) > 0]]
        pdf['common'] = longDict
        pdf['deleted'] = [item for item in sw1.split('#') if len(item) > 0 and item.isdigit()!=True ]
        pdf['sourceSkeleton'] = sw1
        pdf['targetSkeleton'] = sw2


        jointWord = ''
        sw1Split = sw1.split('#')
        sw2Split = sw2.split('!')

        sw3 = [nummi for nummi in sw1Split if nummi.isdigit() == True]
        sw4 = [nummi for nummi in sw2Split if nummi.isdigit() == True]

        if sw3!=sw4:
                print('ordermatchilla',sw3,sw4)


        for key in sorted(longDict.keys()):
            nowN = longDict[key].split('#')[1]
            try:

                while sw1Split[0] != nowN:

                    tingi = sw1Split.pop(0)
                    if len(tingi) > 0:

                        jointWord += 'DEL('
                        for cahra in tingi:
                            jointWord += cahra
                        jointWord += ')'
            except IndexError:
                print("SW1",pdf['Root Word'])

            try:
                while sw2Split[0] != nowN:
                    tingi = sw2Split.pop(0)
                    if len(tingi) > 0:
                        jointWord += 'INS('
                        for cahra in tingi:
                            jointWord += cahra
                        jointWord += ')'
            except IndexError:
                print("SW2",pdf['Root Word'])


            try:    
                if  sw1Split[0] == nowN and  sw2Split[0] == nowN:
                    jointWord = jointWord + longDict[key].split('#')[0]
                    sw1Split.pop(0)
                    sw2Split.pop(0)
                else:
                    print('pani pali not expected')
            except IndexError:
                print("common",pdf['Root Word'])

        while len(sw1Split) > 0:
            tingi = sw1Split.pop(0)
            if len(tingi) > 0:
                jointWord += 'DEL('
                for cahra in tingi:
                    jointWord += cahra
                jointWord += ')'

        while len(sw2Split) > 0:

            tingi = sw2Split.pop(0)
            if len(tingi) > 0:
                jointWord += 'INS('
                for cahra in tingi:
                    jointWord += cahra
                jointWord += ')'


        if len(pdf['deleted']) == 0:
            pdf['deleted'] = ['ϵ']


        pdf['added'] = [item for item in sw2.split('!') if len(item) > 0 and item.isdigit()!=True]

        if len(pdf['added']) == 0:
            pdf['added'] = ['ϵ']

        pdf['aligned'] = jointWord

        return pdf
    except:
        print("error")
        return
df=pd.read_csv('prefix_final.csv')
df.drop([2242])
ddf = df.apply(iterLCS, axis=1)
ddf.to_csv('prefix_pattern.csv')

