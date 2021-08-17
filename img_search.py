from PIL import Image
import numpy as np
import os
import re
import cv2


# ファイルパスを指定
search_dir = './static/images/img_template_search'
cache_dir = './static/images/img_template_search/cache_avhash'

if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)


def average_hash(fname, size=16):
    """
    画像データをAverage hashに変換
    """
    fname2 = fname[len(search_dir):]
    # 画像をキャッシュしておく
    cache_file = cache_dir + "/" + fname2.replace('/', '_') + ".csv"
    # ハッシュを作成
    if not os.path.exists(cache_file):
        img = Image.open(fname)
        img = img.convert('L').resize((size, size), Image.ANTIALIAS)
        pixels = np.array(img.getdata()).reshape((size, size))
        print(pixels)
        avg = pixels.mean()
        # 平均より大きければ値を1、平均以下で0に変換
        px = 1 * (pixels > avg)
        np.savetxt(cache_file, px, fmt="%.0f", delimiter=",")
    else:
        # すでにキャッシュがあればファイルから読込み
        px = np.loadtxt(cache_file, delimiter=",")
    return px


def hamming_dist(a, b):
    """
    簡単にハミング距離を求める
    """
    # 一次元の配列に変換
    aa = a.reshape(1, -1)
    ab = b.reshape(1, -1)
    dist = (aa != ab).sum()
    return dist


def find_image(fname, rate):
    """
    画像検索
    """
    src = average_hash(fname)
    for fname in enum_all_files(search_dir):
        dst = average_hash(fname)
        diff_r = hamming_dist(src, dst) / 256
        if diff_r < rate:
            yield (diff_r, fname)


def enum_all_files(path):
    """
    全てのディレクトリを列挙
    """
    for root, dirs, files in os.walk(path):
        for f in files:
            fname = os.path.join(root, f)
            if re.search(r'\.(jpg|jpeg|png)$', fname):
                yield fname


def similar_image(png_file):
    """
    検索元の画像を取得
    """
    src_file = './static/images/pdf_change_pngs/' + png_file

    html = ""
    sim = list(find_image(src_file, 0.4))
    sim = sorted(sim, key=lambda x: x[0])

    similar_diff = []
    similar_image = []
    similar_image_width = []
    similar_image_height = []
    for r, f in sim:
        if src_file not in f:
            # 差分とテンプレート画像ファイルを確認
            # print(r, ">", f)
            s = '<div style="float:left;"><h3>[差異:' + str(r) + '-' + \
                os.path.basename(f) + ']</h3>' + \
                '<p><a href="' + f + '"><img src="' + f + '" width=400>' + \
                '</a></p></div>'
            html += s
            similar_diff.append(r)
            similar_image.append(os.path.basename(f))
            img_size = cv2.imread('static/images/img_template_search/' + os.path.basename(f))
            # 画像の大きさを取得
            height, width, channels = img_size.shape[:3]
            similar_image_width.append(width)
            similar_image_height.append(height)

    # 類似率、テンプレート画像ファイル、テンプレート画像ファイル幅、テンプレート画像ファイル高さを確認
    # print(similar_diff, similar_image, similar_image_width, similar_image_height)
    sim = list(zip(similar_diff, similar_image, similar_image_width, similar_image_height))

    # HTMLを出力する
    html_output = """<html><body><h3>元画像</h3>
    <p><img src='{0}' width=400></p>{1}
    </body></html>""".format(src_file, html)
    with open('./log-avhash-search-output.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print('log-avhash-search-output.html出力完了')

    return sim
