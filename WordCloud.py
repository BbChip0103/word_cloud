#-*-coding: utf-8

import sys
import re
from os import path
from PIL import Image
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import random
from konlpy.tag import Twitter
from wordcloud import WordCloud

# import pprint
# import operator

directory = path.dirname(__file__)
FONT_PATH = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'


def CustumNLP(_text) :
    words = Twitter().pos(phrase=_text,
                            norm=True,
                            #stem=True
                            )
    words = [data[0] for data in words
                if( (data[1] == 'Noun')
                     #or (data[1] == 'Verb')
                     )
            ]
    return words


def CustumClean(_words, _stop_words = []) :
    words = [data for data in _words
                if( (data not in _stop_words)
                     and (len(data) > 1) )
            ]
    return words


def CountWords(_words, _size) :
    cnt = Counter(_words).most_common(_size)
    dic_word = dict(cnt)

    return dic_word


def MakeColor(word, font_size, position, orientation,
                random_state=None, **kwargs):

    # facebook color - blue
    # return "hsl(221, %d%%, %d%%)" \
    #         %(random.randint(40, 50), random.randint(40, 50))

    # target color - black
    return "hsl(0, %d%%, %d%%)" \
    %(random.randint(0, 10), random.randint(90, 100))


def MakeWordCloud(_dic_words, _str_mask='mask.png',
                    _str_result='result.png', _show_image=True) :
    mask = np.array(Image.open(path.join(directory, _str_mask)))

    wc = WordCloud(font_path=FONT_PATH
                    , background_color='black'
                    , max_words=200
                    , mask=mask
                    , width=1920, height=1080
                    , color_func=MakeColor
                    )
    wc.generate_from_frequencies(_dic_words)
    wc.to_file(path.join(directory, _str_result))

    if _show_image == True :
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.figure()
        plt.imshow(mask, cmap=plt.cm.gray,
                    interpolation='bilinear')
        plt.axis("off")
        plt.show()


# 메인 함수
def main(argv):
    if len(argv) != 3:
        print('python [모듈 이름] [텍스트 파일명] [결과파일명]')
        print('ex) python WordCloud.py input.txt result.png')
        print('마스크 이미지 파일 이름은 mask.png로 해주세요.')
        return

    input_file = open(path.join(directory, argv[1]))
    text = input_file.read()
    #text = CleanText(text)
    #datas = Twitter().nouns(text)
    words = CustumNLP(text)
    words = CustumClean(words, ['익명',
                                '제보',
                                '익명제보',
                                '우리',
                                '진짜',
                                '오늘',
                                '너무',
                                '댓글',
                                '연락',
                                '내일',
                                '여기',
                                '혹시',
                                '지금',
                                '태그'
                                ])
    dic_words = CountWords(words, 200)
    # sorted_words = sorted(dic_words.items()
    #                         , key=operator.itemgetter(1)
    #                         , reverse=True
    #                         )
    # pprint.pprint(sorted_words)
    # return
    MakeWordCloud(_dic_words=dic_words,
                    _str_mask='mask.png',
                    _str_result=argv[2],
                    _show_image=True)
    input_file.close()


if __name__ == "__main__":
    main(sys.argv)
