from split_node import ParseNode
from getAozora import aozora
from getWikipedia import wikipedia
import MeCab
import itertools
import sys

JIRITSUGO = (
"動詞","形容詞","接続詞",
"名詞","副詞","連体詞","感動詞")#自立後のリスト
FUZOKUGO = ("助詞","助動詞")

def FindTanka(text,neologd=False):
    """
    テキストをぶちこむと短歌のリストを返してくれる風流な関数。
    """
    Nodes = ParseNode(text,neologd=neologd)
    TankaPoint = (5,12,17,24,31,32)
    Tankas = []
    for sentence in Nodes:
        l = len(sentence)
        for n,StartWord in enumerate(sentence):
            if StartWord["Yomi"] =="*" or\
            StartWord["Hinshi"] not in JIRITSUGO:continue
            sound = 0
            curpos = n
            tanka = ""
            tankalen = 0
            while sound<=32 and curpos<l:
                w = sentence[curpos]
                #句(57577)の始まりが助詞や助動詞でないかどうか
                if sound in TankaPoint and tankalen<=4:
                    if w["Hinshi"] not in ("名詞","動詞","連体詞","副詞","形容詞"):
                        break    
                if w["Yomi"]!="*":
                    tanka += w["Text"]
                    sound += w["Length"]
                    if sound ==TankaPoint[tankalen]:
                        tankalen+=1
                    if tankalen == 5:#短歌が完成した場合
                        if (w["Hinshi"] in JIRITSUGO and "連用" not in w["Katsuyo"])  or (curpos<l-1 and sentence[curpos+1]["Hinshi"] in JIRITSUGO):
                            Tankas.append(tanka)
                            break
                    if tankalen == 6:#31文字でうまく終わらなかった場合の安全策
                        Tankas.append(tanka)
                        break
                curpos+=1
                
    return(Tankas)

if __name__ == "__main__":
    print(FindTanka(aozora(input("url:")),neologd = True))