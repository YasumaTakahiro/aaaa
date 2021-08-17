# import os
import cv2
# import glob
# import matplotlib.pyplot as plt
# xmlからテンプレート情報の読み込み
import xml.etree.ElementTree as ET


def trimming(template_xml, file_name):
    
    # delete_filelist = glob.glob('./static/images/trimming/' + file_name + '*png')
    # [os.remove(f) for f in delete_filelist]
        
    # パス設定
    img_path = './static/images/png_positon_move/img_move.jpg'
    # 画像を読込み
    img = cv2.imread(img_path)

    # 画像が読み込んでいるのか確認 アプリ起動中はコメントアウト
    # plt.axis('off')
    # plt.imshow(img[:,:,::-1])
    # plt.show()

    # xmlからテンプレート情報の読み込み
    xml_path = './static/template_xml/' + template_xml
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # トリミングした画像を一時フォルダへ保存するパス
    tri_path = './static/images/trimming/' + file_name + '/'

    img_labeled = img.copy()
    for obj in root.findall("./object"):
        name = obj.find('name').text
        xmin = obj.find('bndbox').find('xmin').text
        ymin = obj.find('bndbox').find('ymin').text
        xmax = obj.find('bndbox').find('xmax').text
        ymax = obj.find('bndbox').find('ymax').text
        xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
        # cv2形式で画像を保存
        # img[top:bottom, left:right]
        print('width：{0},height：{1}'.format(xmax - xmin, ymax - ymin))
        img_tri = img_labeled[ymin:ymax, xmin:xmax]
        # 一時フォルダに保存
        cv2.imwrite(tri_path + name + '.png', img_tri)


# trimming('5120_001.xml')
