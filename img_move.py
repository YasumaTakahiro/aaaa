import cv2
import numpy as np


def png_position_move(temp_png, change_png):
    """
    テンプレート画像に合わせて読み込んだを画像の位置を修正する
    """
    # 画像を読み込む
    template_img = cv2.imread('./static/images/template_xml_img/' + temp_png)
    img_png = cv2.imread('./static/images/pdf_change_pngs/' + change_png)

    # print(template_img)
    # print(img_png)

    akaze = cv2.AKAZE_create()
    template_img_kp, template_img_des = akaze.detectAndCompute(template_img, None)
    img_png_kp, img_png_des = akaze.detectAndCompute(img_png, None)

    # 特徴のマッチング
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(template_img_des, img_png_des, k=2)

    # 正しいマッチングの保持
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append([m])

    # 適切なキーポイントを選択
    template_matched_kpts = np.float32([template_img_kp[m[0].queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    img_matched_kpts = np.float32([img_png_kp[m[0].trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # ホモグラフィを計算
    H, status = cv2.findHomography(img_matched_kpts, template_matched_kpts, cv2.RANSAC, 5.0)

    # 画像を変換
    img_position_move = cv2.warpPerspective(img_png, H, (img_png.shape[1], img_png.shape[0]))

    cv2.imwrite('./static/images/png_positon_move/img_move.jpg', img_position_move)
