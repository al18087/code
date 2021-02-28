from urllib.request import urlopen
from bs4 import BeautifulSoup
from gensim.models import word2vec
import re
import MeCab


def wikipedia_sentence(url):
    html = urlopen("https://ja.wikipedia.org{}".format(url))
    soup = BeautifulSoup(html, "html.parser")
    sentences = ""
    for sentence in soup.findAll("p"):
        sentences += sentence.get_text()

    return sentences


#形態素解析
def MorphologicalAnalysis(sentences):
    mecab = MeCab.Tagger("-Ochasen")
    mecab.parse('')#文字列がGCされるのを防ぐ
    node = mecab.parseToNode(sentences)
    sentence = []

    while node:
        #単語を取得
        word = node.surface
        #品詞を取得
        pos = node.feature.split(",")
        if pos[1] == "固有名詞" or (pos[0] == "動詞" and pos[1] == "一般"):
            sentence.append(word)
        #次の単語に進める
        node = node.next

    sentence.pop(0)
    sentence.pop(-1)
    return sentence


#wikipedia_urls = ["/wiki/%E4%B9%83%E6%9C%A8%E5%9D%8246", "/wiki/Python", "/wiki/%E5%91%AA%E8%A1%93%E5%BB%BB%E6%88%A6"]
wikipedia_urls = ["/wiki/%E4%B9%83%E6%9C%A8%E5%9D%8246", "/wiki/%E6%AB%BB%E5%9D%8246", "/wiki/%E6%97%A5%E5%90%91%E5%9D%8246"]
for url in wikipedia_urls:
    sentences = wikipedia_sentence(url)
    noun_verb = MorphologicalAnalysis(sentences)
    
    meishidoushi = [noun_verb]
    model = word2vec.Word2Vec(meishidoushi, size=100, min_count=1)
    words = []
    for word in noun_verb:
        try:
            ret = model.wv.most_similar(positive=word, topn=5)
            for item in ret:
                words.append(item[0])
                #print(item[0], item[1])
        except KeyError as error:
            print(error)
    

    already_words = []
    word_count = {}
    for word in words:
        if word in already_words:
            continue
        word_count[word] = words.count(word)

    #print(word_count)
    word_count = sorted(word_count.items(), key=lambda x:x[1], reverse=True)
    for i in range(0, 5):
        print(word_count[i])

    print("\n")   
