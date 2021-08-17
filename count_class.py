import glob
import cv2
import numpy as np
import pandas as pd
from keras.models import load_model


def img_count_read(img, img_w, img_h):
    """
    引数から画像ファイルを読込み 判定するデータへ変更
    """
    im = cv2.imread(img)
    im = cv2.resize(im, (img_w, img_h))
    data = np.array(im) / 255.0
    X = []
    X.append(data)
    return np.array(X)


def count_predict(model, X):
    '''
    数量を予測する
    '''
    r = model.predict(X, batch_size=32, verbose=1)
    res = r[0]
    return res


def count_classification(file_name):
    """
    数量を判定する
    """
    # 数量のcsvファイルを読み込む
    df_counts = pd.read_csv('./read_csv_files/数量.csv', converters={'数量': lambda x: str(x)})
    df_counts_values = df_counts[['数量']].values
    counts_classes = [_[0] for _ in df_counts_values]

    # クラス個数を確認
    # counts_num_classes = len(counts_classes)
    # print('クラス' + str(counts_num_classes))

    # 数量モデルのロード
    count_model = load_model('./classfication_files/counts-transfer.h5')

    # 判定する画像を数値データへ変換
    counts_imgs = glob.glob('./static/images/trimming/' + file_name + '/*count*.png')
    print(counts_imgs)

    counts_predicted = []

    for i, count_img in enumerate(counts_imgs):
        count_X = img_count_read(count_img, 90, 90)
        # 数量を予測する
        count_predicted = count_predict(count_model, count_X)
        # 結果を表示する
        counts_predicted.append(count_predicted)
        # for j, acc in enumerate(count_predicted):
        #     print('分類結果=', counts_classes[j], '一致率=', int(acc * 100), '%')
        # print('予測した結果=', counts_classes[count_predicted.argmax()])
    
    # データを辞書型に変換
    counts_dic = {}
    for i, count_predicted in enumerate(counts_predicted, 1):
        # print(item_predicted)
        counts_dic.setdefault('count' + f'{i:03}', {})
        for j, count_class in enumerate(counts_classes):
            counts_dic['count' + f'{i:03}'].setdefault(count_class, count_predicted[j])

    return counts_dic


# count_class.pyの動作確認コメントアウト
# counts_dic = count_classification()
# print(counts_dic)
# for count in counts_dic.items():
#     print(count)