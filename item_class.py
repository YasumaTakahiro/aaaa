import glob
import cv2
import numpy as np
import pandas as pd
from keras.models import load_model


def img_item_read(img, img_w, img_h):
    """
    引数から画像ファイルを読込み 判定するデータへ変更
    """
    im = cv2.imread(img)
    im = cv2.resize(im, (img_w, img_h))
    data = np.array(im) / 255.0
    X = []
    X.append(data)
    return np.array(X)


def item_predict(model, X):
    """
    品番名を予測する
    """
    r = model.predict(X, batch_size=32, verbose=1)
    res = r[0]
    return res


def item_classification(customer_number, item_w, item_h, file_name):
    """
    品番名の分類のメイン処理
    """
    # 得意先ごとの得意先をcsvファイルを読み込む
    df_items = pd.read_csv('./read_csv_files/' + str(customer_number) + '_商品マスタ.csv', converters={'品番コード': lambda x: str(x)})
    df_items_values = df_items[['品番コード', '品番コード日本語対応']].values
    items_classes = [_ for _ in df_items_values]
    
    # 商品分類するクラス個数を確認
    items_num_classes = len(items_classes)
    print('--------------------------------------')
    print('商品分類クラス' + str(items_num_classes))
    print('--------------------------------------')
    
    # print(customer_number)
    # 各得意先の品番名モデルのロード
    item_model = load_model('./classfication_files/' + str(customer_number) + '_item-transfer.h5')

    print(item_model)

    # 判定する画像を数値データへ変換
    items_imgs = glob.glob('./static/images/trimming/' + file_name + '/*item*.png')
    # print(items_imgs)

    items_predicted = []

    for i, item_img in enumerate(items_imgs):
        item_X = img_item_read(item_img, item_w, item_h)
        # item_X = img_item_read(item_img, 400, 90)
        # 品番名を予測する
        item_predicted = item_predict(item_model, item_X)
        # 結果を表示する
        items_predicted.append(item_predicted)
        # for j, acc in enumerate(item_predicted):
        #     print('分類結果=', items_classes[j], '一致率=', int(acc * 100), '%')
        # print('予測した結果=', items_classes[item_predicted.argmax()])
    
    # データを辞書型に変換
    items_dic = {}
    for i, item_predicted in enumerate(items_predicted, 1):
        # print(item_predicted)
        items_dic.setdefault('item' + f'{i:03}', {})
        for j, item_class in enumerate(items_classes):
            # print('######################')
            # print(i)
            # print(item_class[0])
            # print(item_predicted[j])
            if item_class[0][:4] == customer_number:
                items_dic['item' + f'{i:03}'].setdefault(item_class[1], item_predicted[j])
            else:
                items_dic['item' + f'{i:03}'].setdefault(item_class[0], item_predicted[j])

    return items_dic, items_num_classes

# item_class.pyの動作確認コメントアウト
# items_dic = item_classification('5487')
# print(items_dic)
# for item in items_dic.items():
#     print(item[0], item[1].keys(), item[1].values())
