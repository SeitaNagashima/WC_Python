#Windows,janome,wordcloudが必要です。

from janome.tokenizer import Tokenizer

# テキストデータの読み込み
text_data = open("gakutika.txt", "rb").read()
# テキストデータの文字コードをUTF-8に指定
text = text_data.decode('utf-8')

# 形態素解析
t = Tokenizer()
seps = t.tokenize(text)

gakutika_list = []
# 抽出する品詞を指定
tags = ["名詞","動詞", "副詞", "形容詞", "形容動詞"]

for _ in seps:
    #単語の抽出
    if _.base_form == '*':
        word = _.surface
    else:
        word = _.base_form

    #品詞の抽出
    ps = _.part_of_speech
    word_class = ps.split(',')[0]

    #特定の品詞のみ抽出
    if word_class in tags:
        gakutika_list.append(word)

print(gakutika_list)

#wordcloudをインポート
from wordcloud import WordCloud, ImageColorGenerator

text = ' '.join(gakutika_list)

#日本語テキストデータを取り扱うパス
fpath = "C:/Windows/Fonts/YuGothM.ttc"
#背景を白に、幅と高さも設定
wordcloud = WordCloud(background_color="White",font_path=fpath,width = 800,height = 600).generate(text)

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def get_wordcrowd_mask(text, imgpath):
    #画像を取得して、numpy形式に変換
    img_color = np.array(Image.open(imgpath))
    #wordcloudでも画像形式を設定
    wc = WordCloud(width=800,
                   height=600,
                   font_path=fpath,
                   mask=img_color,
                   collocations=False,#単語の重複防止
                   #background_color="White",
                   stopwords={'こと', 'する','会'},#禁止単語の設定
                   colormap="YlOrRd"
                   ).generate(text)

    image_colors = ImageColorGenerator(img_color)
    #図のサイズを６＊６指定、１インチあたりのドット数を２００に指定
    plt.figure(figsize=(6,6),dpi=500)
    #画像を補完
    plt.imshow(wc,interpolation="bilinear")
    plt.axis("off")
    plt.show()
    #pngで保存
    wc.to_file("./gakutika_mask.png")

get_wordcrowd_mask(text,".\sun.jpg")

#pngで保存
wordcloud.to_file("./gakutika.png")