import cv2
# import matplotlib.pyplot as plt
# xmlからテンプレート情報の読み込み
import xml.etree.ElementTree as ET


def redline_drow(png_file, template_xml):
    """
    元画像に赤線を引く処理
    """
    # パス設定
    img_path = './static/images/png_positon_move/' + png_file
    
    # 画像を読込み
    img = cv2.imread(img_path)

    # 画像が読み込んでいるのか確認 アプリ起動中はコメントアウト
    # plt.axis('off')
    # plt.imshow(img[:, :, ::-1])
    # plt.show()

    # # xmlからテンプレート情報の読み込み
    xml_path = './static/template_xml/' + template_xml
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # # トリミングした画像を一時フォルダへ保存するパス
    # tri_path = './tmp_image_trimming/'

    img_labeled = img.copy()
    for obj in root.findall("./object"):
        name = obj.find('name').text
        xmin = obj.find('bndbox').find('xmin').text
        ymin = obj.find('bndbox').find('ymin').text
        xmax = obj.find('bndbox').find('xmax').text
        ymax = obj.find('bndbox').find('ymax').text
        xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
        cv2.rectangle(img_labeled, (xmin, ymin), (xmax, ymax),
                      (0, 0, 255), thickness=5, lineType=cv2.LINE_4)
        cv2.putText(img_labeled, name, (xmin + 10, ymin + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 128, 0), thickness=3)

    # 座標を指定したときの画像を確認　アプリ起動はコメントアウト
    # plt.figure(figsize=[10, 10])
    # plt.imshow(img_labeled[:, :, ::-1])
    # plt.title("img_labeled")
    # plt.show()

    cv2.imwrite('./static/images/png_positon_move/img_move_redline.png',
                img_labeled[:, :, :])

# 切り取る画像およびテンプレートxmlファイルを選択
# redline_drow('img_move.jpg', '5120_001.xml')
