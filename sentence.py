import MeCab
import random

#形態素解析
def MorphologicalAnalysis(text):
    mecab = MeCab.Tagger("-Ochasen")
    mecab.parse('')#文字列がGCされるのを防ぐ
    node = mecab.parseToNode(text)
    sentence = []
    sentence_pos = []

    while node:
        #単語を取得
        word = node.surface
        #品詞を取得
        pos = node.feature.split(",")[0]
        sentence.append(word)
        sentence_pos.append(pos)
        #次の単語に進める
        node = node.next

    sentence.pop(0)
    sentence.pop(-1)
    sentence_pos.pop(0)
    sentence_pos.pop(-1)
    return sentence, sentence_pos


def PhraseMorphologicalAnalysis(phrase):
    mecab = MeCab.Tagger("-Ochasen")
    mecab.parse('')#文字列がGCされるのを防ぐ
    node = mecab.parseToNode(phrase)
    sentence_pos = []

    while node:
        #単語を取得
        word = node.surface
        #品詞を取得
        pos = node.feature.split(",")[0]
        sentence_pos.append(pos)
        #次の単語に進める
        node = node.next

    sentence_pos.pop(0)
    sentence_pos.pop(-1)
    return sentence_pos


#ngrams
def Ngrams(n, text):
    sentence, sentence_pos = MorphologicalAnalysis(text)
    ngrams_list = []
    ngrams_pos = []
    for i in range(len(sentence)-n+1):
        ngrams_list.append(sentence[i:i+n])
        ngrams_pos.append(sentence_pos[i:i+n])

    return ngrams_list, ngrams_pos


def MakingDocument(n, text):
    sentence, sentence_pos = Ngrams(n, text)
    i = 0
    index = 0
    next_phrase = ""
    makingSentence = []
    candidate = []
    while i <= 3:

        if len(makingSentence) == 0:
            for sen, sen_pos in zip(sentence, sentence_pos):
                if sen_pos[0] == "名詞":
                    candidate.append(sen)
            
            index = random.randrange(0, len(candidate))
            next_phrase = candidate[index][0]
            makingSentence.append(next_phrase)
            candidate.clear()
            continue

        
        if next_phrase == "の":
            for sen, sen_pos in zip(sentence, sentence_pos):
                if sen_pos[0] != "動詞" or sen_pos[0] != "助詞" or sen_pos[0] != "助動詞" or sen_pos[0] != "記号":
                    candidate.append(sen)
            
            index = random.randrange(0, len(candidate))
            next_phrase = candidate[index][0]
            makingSentence.append(next_phrase)
            candidate.clear()
            continue


        if next_phrase == "．" or next_phrase == "，":
            for sen, sen_pos in zip(sentence, sentence_pos):
                if sen_pos[0] == "名詞":
                    candidate.append(sen)
            
            if next_phrase == "．":
                i += 1
            if i == 3:
                break

            index = random.randrange(0, len(candidate))
            next_phrase = candidate[index][0]
            makingSentence.append(next_phrase)
            candidate.clear()
            continue

        
        if PhraseMorphologicalAnalysis(makingSentence[-1]) == "助動詞":
            makingSentence.append("．")
        

        index = random.randrange(0, len(sentence))
        next_phrase = sentence[index][0]
        while next_phrase == makingSentence[-1][0] or sentence_pos[index][0] == PhraseMorphologicalAnalysis(makingSentence[-1]):
            index = random.randrange(0, len(sentence))
            next_phrase = sentence[index][0]

        makingSentence.append(next_phrase)



    makingSentence = "".join(makingSentence)
    print(makingSentence)



f = open("sentence_data.txt", "r", encoding="utf-8")
dataList = f.readlines()
for i in range(len(dataList)):
    sen = dataList[i].strip()
    dataList[i] = sen
    
text2 = "".join(dataList)
sentences2, sentence_pos2 = Ngrams(3, text2)

MakingDocument(3, text2)
#print(sentences2)
#print(sentence_pos2)

f.close()
