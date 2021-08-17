import os
import glob
import webbrowser
# import mojimoji
# import unicodedata
# import difflib
# import csv
# from flask import render_template, request, redirect, url_for, jsonify
# from sqlalchemy import or_, and_
# from werkzeug.utils import secure_filename
# from app import app, getConncection
# from models import db, Kakashi, Image, Product, LineDict, Order, OrderDetail, Customer
# スケジューラーライブラリ
from apscheduler.schedulers.blocking import BlockingScheduler
# from datetime import datetime
# PDF読み込み
from pathlib import Path
from pdf_change_png import pdf_change, png_confirm
# 類似画像検索
# from img_search import similar_image
# 画像位置補正
# from img_move import png_position_move
# 画像に座標の赤線を引く
# from img_redline_drow import redline_drow
# ラベルごとに画像をトリミング処理
# from img_trimming import trimming
# 品番名の分類
# from item_class import item_classification
# 数量の分類
# from count_class import count_classification
# 単位の分類
# from unit_class import unit_classification


def auto_png():
    # タスクスケジューラー関数
    print('3秒後')
    pdf_path = './static/pdf_uploads'
    try:
        pdf_files = glob.glob(pdf_path + '/' + '*pdf')
        # pdfからpngへ拡張子を変更する
        pdf_remove = pdf_files[0]
        pdf_read = Path(pdf_files[0])
        print(pdf_read)
        if pdf_read:
            pdf_change(pdf_file=pdf_read, png_path='./static/images/pdf_change_pngs', fmt='png', dpi=200)
            img_png = png_confirm()
            print(img_png)
            os.remove(pdf_remove)
            img_png_file = os.path.basename(img_png)
            url = 'http://127.0.0.1:5000/image_search/' + img_png_file
            # http://127.0.0.1:5000/image_search/ok_shinyo_4_2021_0609_1645_57_01p.png
            # browser = webbrowser.get('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %s')
            webbrowser.open(url)
    except IndexError:
        print('pdfが格納されておりません。')


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(auto_png, 'interval', seconds=1)
    scheduler.start()