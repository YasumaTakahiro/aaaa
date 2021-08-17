import os
import mojimoji
import unicodedata
import difflib
import csv
import re
import cv2
from dateutil.relativedelta import relativedelta
from flask import render_template, request, redirect, url_for, jsonify
from sqlalchemy import or_, and_
from werkzeug.utils import secure_filename
from app import app, getConncection
from models import db, Kakashi, MlImage, Product, Order, OrderDetail, Customer, BillingDeadline, DeliveryDestination
from datetime import datetime, timedelta
# PDF読み込み
from pathlib import Path
from pdf_change_png import pdf_change, png_confirm
# 類似画像検索
from img_search import similar_image
# 画像位置補正
from img_move import png_position_move
# 画像に座標の赤線を引く
from img_redline_drow import redline_drow
# ラベルごとに画像をトリミング処理
from img_trimming import trimming
# 品番名の分類
from item_class import item_classification
# 数量の分類
from count_class import count_classification


@app.after_request
def add_header(r):
    """
    キャッシュを無効にする
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def index():
    deli_des = DeliveryDestination.query.filter(
            and_(
                # DeliveryDestination.納入先コード.like(f'%5200%'),
                # DeliveryDestination.住所1.like(f'%高崎止%')
                DeliveryDestination.納入先コード.like('%6711%'),
                DeliveryDestination.住所1.like('%福井%')
                )
            )

    return render_template('index.html', deli_des=deli_des)


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    """
    PDFをアップロードするページ
    """
    if request.method == 'GET':
        return render_template('upload_file.html')
    elif request.method == 'POST':
        file = request.files['file']
        if file:
            ascii_filename_pdf = Kakashi.japanese_to_ascii(file.filename)
            save_filename_pdf = secure_filename(ascii_filename_pdf)
            pdf_url = os.path.join('static/pdf_uploads', save_filename_pdf)
            file.save(pdf_url)
            # pdfからpngへ拡張子を変更する
            pdf_read = Path(pdf_url)
            pdf_change(
                pdf_file=pdf_read,
                png_path='./static/images/pdf_change_pngs',
                fmt='png',
                dpi=200)
            img_png = png_confirm()
            return redirect(url_for('image_seach', file_name=img_png))
        else:
            return redirect(request.url)


@app.route('/image_search/<string:file_name>')
def image_seach(file_name):
    """
    類似画像の検索結果を表示するページ
    """
    # 元画像の幅高さを取得
    src_file_size = cv2.imread('static/images/pdf_change_pngs/' + file_name)
    # 画像が読み込まれているか確認
    # print(src_file_size)
    src_height, src_width, src_channels = src_file_size.shape[:3]
    
    # テンプレート画像類似画像検索処理
    similar_lists = similar_image(file_name)
    
    return render_template(
        'image_seach.html',
        file_name=file_name,
        src_height=src_height,
        src_width=src_width,
        similar_lists=similar_lists)


# @app.route('/image_redline/<string:file_name>/<string:template_file_name>')
# def image_redline(file_name, template_file_name):
#     """
#     読み込んだ画像に赤線を引いたページ
#     """
#     # 画像位置合わせ処理
#     png_position_move(template_file_name, file_name)
#     similar_lists = similar_image(file_name)
#     # 赤線を引く処理
#     template_xml = template_file_name.replace('png', 'xml')
#     redline_drow('img_move.jpg', template_xml)
#     img_readline = os.path.basename(
#         './static/images/png_positon_move/img_move_redline.png')
#     return render_template(
#         'image_redline.html',
#         file_name=file_name,
#         template_file_name=template_file_name,
#         similar_lists=similar_lists,
#         img_redline=img_readline
#     )


@app.route('/order_create/<string:file_name>/<string:template_file_name>', methods=['GET', 'POST'])
def order_create(file_name, template_file_name):
    """
    分類結果を表示するページ
    """
    # pngに変換した画像とテンプレート画像を比較して、座標を調整する
    png_position_move(template_file_name, file_name)
    # 赤線を引く処理
    template_xml = template_file_name.replace('png', 'xml')
    redline_drow('img_move.jpg', template_xml)

    # ディレクトリ作成
    new_png_path = './static/images/trimming/' + file_name
    if not os.path.exists(new_png_path):
        os.makedirs(new_png_path)

    # ラベルごとに画像をトリミング処理
    template_xml = template_file_name.replace('png', 'xml')
    trimming(template_xml, file_name)

    # 得意先4桁を取得
    customer_number = template_file_name[:4]

    # 機械学習で使用した商品の画像サイズを取得
    item_img = MlImage.query.filter_by(得意先コード=customer_number).first()
    if item_img.ML商品ステータス == 1:
        img_w = item_img.ML商品幅
        img_h = item_img.ML商品高さ
    else:
        render_template('no_ml.html')

    # 品番名の分類処理
    items_dic, item_len_class = item_classification(customer_number, img_w, img_h, file_name)
    items_sorted = []
    items_db_result = {}
    for item_key, item_value in items_dic.items():
        item_count = 1
        items_sorted = sorted(item_value.items(), reverse=True, key=lambda x: x[1])
        items_db_result.setdefault(item_key, {})
        for item_sorted in items_sorted:
            if item_count <= 5:
                if 'empty' != item_sorted[0]:
                    items_db_result[item_key].setdefault(item_sorted[0], item_sorted[1])
                else:
                    items_db_result[item_key].setdefault('empty', item_sorted[1])
            item_count += 1

    # 数量の分類処理
    counts_dic = count_classification(file_name)
    counts_sorted = []
    counts_result = {}
    for count_key, count_value in counts_dic.items():
        counts_sorted = sorted(count_value.items(), reverse=True, key=lambda x: x[1])
        counts_result.setdefault(count_key, {})
        for count_sorted in counts_sorted:
            counts_result[count_key].setdefault(count_sorted[0], count_sorted[1])
            break
    
    # 品番名、数量の結果を結合する
    print('------------------')
    print('商品分類結果リスト')
    print(items_db_result)
    # print('------------------')
    # print(counts_result)

    # 本日の日付を取得
    dt = datetime.now()
    datetime_str = dt.strftime('%Y%m%d')
    order = Order.query.order_by(Order.id.desc()).first()

    # ordersテーブルにデータが未登録の場合
    if order is None:
        # YYYYMMDD0000
        datetime_db_str = datetime_str
        datetime_db_count = '0000'
    else:
        # ordersテーブルにデータが存在する場合
        # YYYYMMDD
        datetime_db_str = order.仮伝票番号[:8]
        # 0000
        datetime_db_count = order.仮伝票番号[8:12]

    # 仮伝票番号の発番処理
    if datetime_db_str == datetime_str:
        count_temp = (int(datetime_db_count) + 1)
        if count_temp <= 9999:
            slip_temp = datetime_str + str(count_temp).zfill(4)
    else:
        slip_temp = datetime_str + '0001'

    # Orderテーブルへデータ登録
    customer = Customer.query.filter_by(請求先コード=customer_number).first()

    # 配送業者がNullの場合のチェック
    if customer.配送業者コード is None:
        customer_delivery_company = ''
    else:
        customer_delivery_company = customer.配送業者コード

    # 回収方法
    collection = BillingDeadline.query.filter_by(請求先コード=customer.請求先コード).first()

    # 回収予定日計算
    dt_temp = dt + relativedelta(months=collection.回収月区分)
    dt_temp_str = dt_temp.strftime('%Y%m%d')

    if int(dt_temp_str[-2:]) <= collection.回収日:
        # 回収日が31日の場合
        if collection.回収日 == 31:
            dt_temp_31 = dt + relativedelta(months=collection.回収月区分) + relativedelta(months=1)
            dt_temp_31 = dt_temp_31.strftime('%Y%m%d')
            dt_temp_31_str = dt_temp_31[:6] + '01'
            dt_temp_31_date = datetime.strptime(dt_temp_31_str, '%Y%m%d')
            collection_date = (dt_temp_31_date - timedelta(days=1)).strftime('%Y%m%d')
        # 回収日が31日が以外の場合
        else:
            collection_date = dt_temp_str[:6] + str(collection.回収日).zfill(2)
    else:
        dt_re_temp = dt_temp + relativedelta(months=1)
        dt_re_temp_str = dt_re_temp.strftime('%Y%m%d')
        collection_date = dt_re_temp_str[:6] + str(collection.回収日).zfill(2)

    new_order = Order(slip_temp, datetime_str, datetime_str, datetime_str, datetime_str, customer.担当者コード,
                        customer.得意先コード, customer.請求先コード, collection_date, collection.支払方法コード,
                        '', '', '4003', '20210526', '1234',
                        '12345678', customer_delivery_company, '99', '1', '伝票摘要', '2', '社内摘要')
    # Ordersテーブルトランザクション
    with db.session.begin(subtransactions=True):
        new_order.create_order()
    db.session.commit()

    # Ordersテーブルの最新レコードidを取得
    order_id = Order.query.order_by(Order.id.desc()).first()
    new_order_details = []
    # 商品コードを一時保存するリスト
    items_code_temp = []
    line_count = 0

    for i in range(len(items_db_result)):
        # iは商品分類結果にemptyを含む 1から始まるカウント
        i = i + 1
        item_code_lists = list(items_db_result['item' + str(i).zfill(3)].keys())
        # 商品分類結果の先頭を取得する
        item_code_list_1 = item_code_lists[0]
        # 商品分類結果の先頭がemptyの場合はスキップする
        if 'empty' != item_code_list_1:
            # line_countは商品分類結果にempty除く 1から始まるカウント
            line_count = line_count + 1
            # 正規表現で品番コードが10桁であることをチェック
            res = re.match(r'\d{10}', item_code_list_1)
            if res:
                items_code_temp.append(res.group())
                item_code_list_1 = res.group()
                item_code = item_code_list_1
            else:
                # 点々問題
                # 発注書先頭の商品が存在しない場合
                if not items_code_temp:
                    return render_template('error_ai_item.html')
                
                else:
                    product = Product.query.filter_by(品番コード=items_code_temp[-1]).first()
                    # 品番コードが存在しない場合は空のリストを追加する
                    if not product:
                        item_code = ''
                        items_code_temp.append(item_code)
                    # 品番コードが存在する場合は、品番名とAI判定リストで全文検索を実施する
                    else:
                        items_all_search = sql_all_search(product.品番名, item_code_list_1)
                        
                        # 品番名の類似度順にソート
                        items_after_sort = item_rate(items_all_search, product.品番名)

                        if items_after_sort:
                            item_code = items_after_sort[0][0]
                            items_code_temp.append(item_code)
                        else:
                            item_code = ''
                            items_code_temp.append(item_code)
            
            print('------------------------------------')
            print('AI判定の結果 優先順位が高い5つ商品を確認')
            print('{}行目の商品：{}'.format(line_count, item_code_lists))
            print('点々問題 商品を確認')
            print(items_code_temp)
            
            # 商品を分類する個数が5以下のときにindexエラーが発生するため空リストを追加
            if len(item_code_lists) == 2:
                item_code_lists[len(item_code_lists):len(item_code_lists)] = ['', '', '']
            elif len(item_code_lists) == 3:
                item_code_lists[len(item_code_lists):len(item_code_lists)] = ['', '']
            elif len(item_code_lists) == 4:
                item_code_lists[len(item_code_lists):len(item_code_lists)] = ['']
            
            # item_code_list_1～5はAIが判定した結果が入る
            item_code_list_2 = item_code_lists[1]
            item_code_list_3 = item_code_lists[2]
            item_code_list_4 = item_code_lists[3]
            item_code_list_5 = item_code_lists[4]
            
            item_count = next(iter(counts_result['count' + str(i).zfill(3)]))
            # 数量結果がemptyの場合は0を代入する
            if 'empty' == item_count:
                item_count = 0
            # 商品分類結果の先頭が商品マスタに登録されている場合
            if item_code_list_1:
                new_order_detail = OrderDetail(order_id.id, line_count, 1, 1234, item_code,
                                                item_code_list_1, item_code_list_2, item_code_list_3, item_code_list_4, item_code_list_5,
                                                item_count, 20210527, 20210527, 20210527, 12345678, 12345678, 20210527, 20210527, item_count)
                new_order_details.append(new_order_detail)
    
    # Order_detailsトランザクション
    with db.session.begin(subtransactions=True):
        db.session.add_all(new_order_details)
    db.session.commit()

    return redirect(url_for('order_edit', order_id=order_id.id))


@app.route('/order_edit/<int:order_id>', methods=['GET', 'POST'])
def order_edit(order_id):
    order = Order.query.get(order_id)
    # 得意先正式名取得
    customer = Customer.query.filter_by(得意先コード=order.得意先コード).first()

    order_details = order.order_details
    # 商品コードのリスト初期化
    order_products = []
    # AI判定リストを初期化
    order_ai_item_lists = []
    for order_detail in order_details:
        order_prodcut = Product.query.filter_by(品番コード=order_detail.商品コード).first()
        order_products.append(order_prodcut)
        # productsテーブルから品番コードを取得
        order_ai_item1 = Product.order_detail_query(order_detail.AI判定商品コード1)
        order_ai_item2 = Product.order_detail_query(order_detail.AI判定商品コード2)
        order_ai_item3 = Product.order_detail_query(order_detail.AI判定商品コード3)
        order_ai_item4 = Product.order_detail_query(order_detail.AI判定商品コード4)
        order_ai_item5 = Product.order_detail_query(order_detail.AI判定商品コード5)
        order_ai_item_list = [order_ai_item1, order_ai_item2, order_ai_item3, order_ai_item4, order_ai_item5]
        order_ai_item_lists.append(order_ai_item_list)

    return render_template(
            'order_edit.html', order=order, order_details=order_details,
            order_products=order_products, order_ai_item_lists=order_ai_item_lists,
            customer=customer
        )


@app.route('/order_update/<int:order_id>', methods=['GET', 'POST'])
def order_update(order_id):
    # フォームから値取得
    order = Order.query.get(order_id)
    order_date = request.form['order_date']
    shipping_date = request.form['shipping_date']
    due_date = request.form['due_date']
    customer = request.form['customer']
    rep = request.form['rep']
    delivery_destination = request.form['delivery_destination']
    supplier = request.form['supplier']
    delivery_company = request.form['delivery_company']
    time = request.form['time']
    slip_memo = request.form['slip_memo']
    # 注文番号
    # order_number = request.form['order_number']
    in_company_memo = request.form['in_company_memo']
    item_codes = request.form.getlist('item_code')
    item_counts = request.form.getlist('item_count')
    order_kubun = request.form.getlist('order_kubun')

    print('-----------------')
    print(order_kubun)

    # Ordersテーブル更新
    with db.session.begin(subtransactions=True):
        order.受注日 = order_date
        order.ヘッダ出荷日 = shipping_date
        order.ヘッダ納期 = due_date
        order.得意先コード = customer
        order.担当者コード = rep
        order.納入先コード = delivery_destination
        order.仕入先コード = supplier
        order.配送業者コード = delivery_company
        order.時間 = time
        order.伝票摘要 = slip_memo
        order.社内摘要 = in_company_memo
    db.session.commit()

    order_details = order.order_details
    print(order_details)

    with db.session.begin(subtransactions=True):
        for i, items_detail in enumerate(zip(item_codes, item_counts, order_kubun)):
            order_details[i].商品コード = Product.order_detail_update(items_detail[0])
            order_details[i].内訳数量 = items_detail[1]
            order_details[i].明細受注区分 = items_detail[2]
    db.session.commit()

    # CSV出力
    # CSVカラム
    csv_header_colum = ['仮伝票番号', 'ヘッダ受注区分', '事業所コード', '受注日', 'ヘッダ出荷日', 'ヘッダ納期', 'ヘッダ売上予定日', '担当者コード',
                            '得意先コード', '請求先コード', '請求帳端区分', '回収予定日', '回収方法コード', '納入先コード', '仕入先コード', '支払先コード',
                            '支払帳端区分', '支払予定日', '支払方法コード', 'ヘッダ倉庫コード', 'ヘッダ得意先注文番号', '配送業者コード', '時間',
                            '伝票摘要コード', '伝票摘要', '社内摘要コード', '社内摘要',
                            '明細行番号', '明細受注区分', '債権科目区分', '明細倉庫コード', '商品コード',
                            '売上税率区分', '仕入税率区分','明細数量', 'PS区分', '売上単価','売上金額',
                            '売上消費税額', '明細出荷日', '明細受注納期', '明細売上予定日', '受注明細摘要コード',
                            '受注明細摘要', '仕入単価', '仕入金額', '仕入消費税額', '入荷予定日', '仕入予定日',
                            '内訳行番号', '内訳数量']
    
    # 日付取得
    dt = datetime.now()
    file_timestamp = dt.strftime('%Y_%m%d_%H%M%S')

    customer_id = order.得意先コード
    customer = Customer.query.filter_by(得意先コード=customer_id).first()
    customer_name = customer.得意先正式名.replace('　', '').replace(' ', '_')

    with open('./output_csv_files/' + customer_name + '_' + file_timestamp + '.csv', 'w', newline='', encoding='cp932') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(csv_header_colum)
        for order_detail in order.order_details:
            # 商品コードが空以外はCSV出力する
            if order_detail.商品コード != '':
                writer.writerow([order.仮伝票番号, order.ヘッダ受注区分, order.事業所コード, str(order.受注日).replace('-', '/'),
                                str(order.ヘッダ出荷日).replace('-', '/'), str(order.ヘッダ納期).replace('-', '/'), str(order.ヘッダ売上予定日).replace('-', '/'),
                                order.担当者コード, order.得意先コード, order.請求先コード, order.請求帳端区分,
                                str(order.回収予定日).replace('-', '/'), order.回収方法コード, order.納入先コード, order.仕入先コード,
                                order.支払先コード, str(order.支払帳端区分).replace('-', '/'), str(order.支払予定日).replace('-', '/'), order.支払方法コード,
                                order.ヘッダ倉庫コード, order.ヘッダ得意先注文番号, order.配送業者コード, order.時間,
                                order.伝票摘要コード, order.伝票摘要, order.社内摘要コード, order.社内摘要,
                                order_detail.明細行番号, order_detail.明細受注区分, order_detail.債権科目区分, order_detail.明細倉庫コード,
                                order_detail.商品コード, order_detail.売上税率区分, order_detail.仕入税率区分, order_detail.明細数量,
                                order_detail.PS区分, order_detail.売上単価, order_detail.売上金額, order_detail.売上消費税額,
                                str(order_detail.明細出荷日).replace('-', '/'), str(order_detail.明細受注納期).replace('-', '/'), str(order_detail.明細売上予定日).replace('-', '/'), order_detail.受注明細摘要コード,
                                order_detail.受注明細摘要, order_detail.仕入単価, order_detail.仕入金額, order_detail.仕入消費税額,
                                str(order_detail.入荷予定日).replace('-', '/'), str(order_detail.仕入予定日).replace('-', '/'), order_detail.内訳行番号, order_detail.内訳数量])

    return redirect(url_for('order_edit', order_id=order.id))


def sql_all_search(sinabanmei, sinabanmei_kikaku):
    """
    関数 点々問題sql全文検索
        以下 検索する値
        sinabanmei = '１０５(ﾆｭｰｸﾘｰﾑ)ｼﾞｬｹｯﾄ'
        sinabanmei_kikaku = 'らくえる　板取2S'
    """
    # DB接続
    connection = getConncection()
    cursor = connection.cursor()
    # sql文
    sql_word = sinabanmei + ' ' + sinabanmei_kikaku
    sql = "SELECT 品番コード, 品番名, 規格 FROM products WHERE MATCH(品番名, 規格) AGAINST(%s IN BOOLEAN MODE);"
    cursor.execute(sql, (sql_word))

    items = cursor.fetchall()
    items_sim = []

    # 品番名の先頭から3文字
    forward_matching = mojimoji.zen_to_han(sinabanmei).replace('　', '').replace(' ', '')[:3]
    # 品名規格を全角から半角へ変更する
    sinabanmei_kikaku_hankaku = mojimoji.zen_to_han(sinabanmei_kikaku).replace('　', '').replace(' ', '')

    # 品番名の先頭から3文字一致および規格の絞り込み
    for item in items:
        item_record = str(item['品番名']) + str(item['規格'])
        item_record_edit_after = mojimoji.zen_to_han(item_record).replace('　', '').replace(' ', '')
        # 商品の規格が1桁から4桁までを正規表現でチェック
        if bool(re.match(r'\d{1,4}', sinabanmei_kikaku_hankaku)):
            item_kikaku_edit_after = mojimoji.zen_to_han(str(item['規格'])).replace('　', '').replace(' ', '')
            if forward_matching == item_record_edit_after[:3] and sinabanmei_kikaku_hankaku == item_kikaku_edit_after:
                items_sim.append(item)
        else:
            if forward_matching == item_record_edit_after[:3] and sinabanmei_kikaku_hankaku in item_record_edit_after:
                items_sim.append(item)

    # 点々問題　商品名絞り込み結果
    # print(items_sim)
    # DB接続切断
    cursor.close()
    connection.close()

    return items_sim


def item_rate(items_all_search, sinabanmei):
    """
    関数 品番名の類似度順にソート

    """
    # 比較元をUnicode正規化
    normalized_src = unicodedata.normalize('NFKC', sinabanmei + '_')
    comparison_target_lists = []
    match_raito_lists = []
    sinabancodes_lists = []

    for item in items_all_search:
        # 比較先をUnicode正規化
        comparison_target = str(item['品番名']) + '_' + str(item['規格'])
        comparison_target_lists.append(comparison_target)
        normalized_dst = unicodedata.normalize('NFKC', comparison_target)

        # 類似度を計算、0.0~1.0 で結果を返す
        s = difflib.SequenceMatcher(None, normalized_src, normalized_dst).ratio()
        match_raito_lists.append(s)

        sinabancode = item['品番コード']
        sinabancodes_lists.append(sinabancode)

    items_before_sort = zip(sinabancodes_lists, comparison_target_lists, match_raito_lists)
    # 類似度の高い順にソート
    items_after_sort = sorted(items_before_sort, key=lambda x: x[2], reverse=True)
    
    return items_after_sort


@app.route('/db_item_check', methods=['POST'])
def db_item_check():
    """
    AI判定リストを変更したときに、商品コードを変更する
    """
    if request.method == "POST":
        number = request.form['select_change_number']
        ai_item_select = request.form['ai_item_select']
        product = Product.query.filter_by(品番コード=ai_item_select).first()

        return jsonify({'item_code': product.品番コード,
                        'item_name': product.品番名,
                        'item_standard': product.規格,
                        'number': number})


@app.route('/db_item_on_line_one', methods=['POST'])
def db_item_on_line_one():
    """
    点々問題の処理
    例
    1行目  １０５(ﾆｭｰｸﾘｰﾑ)ｼﾞｬｹｯﾄ　14
    2行目       〃　15
    """
    if request.method == "POST":
        number = request.form['select_change_number']
        db_item_on_line_one = request.form['item_on_line_one']
        product = Product.query.filter_by(品番コード=db_item_on_line_one).first()
        sinabanmei = product.品番名
        sinabanmei_kikaku = request.form['ai_item_select']

    print(sinabanmei)
    print(sinabanmei_kikaku)

    # 全文検索処理
    items_all_search = sql_all_search(sinabanmei, sinabanmei_kikaku)

    # 全文検索が存在する場合
    if items_all_search:
        # 品番名の類似度順にソート
        items_after_sort = item_rate(items_all_search, sinabanmei)
        # print('---------------')
        # print(items_after_sort[0][0])

        return jsonify({'item_code': items_after_sort[0][0] + '_' + items_after_sort[0][1],
                        'number': number})
    # 全文検索が存在しない場合
    else:
        return jsonify({'item_code': '', 'number': number})


@app.route('/db_customer_search', methods=['POST'])
def db_customer_search():
    """
    得意先の検索処理
    検索キーワードは以下の3つ
        得意先コード、得意先正式名、得意先名
    """
    if request.method == 'POST':
        customer_keywords = request.form['customer_keywords']

        # 全角スペースがある場合、半角スペースに変更する
        keywords_lists = customer_keywords.replace('　', ' ').split()

        # 全角から半角へ 半角から全角へ変換
        hankaku_change_keywords = []
        zenkaku_change_keywords = []

        for keyword in keywords_lists:
            hankaku_keyword = mojimoji.zen_to_han(keyword)
            hankaku_change_keywords.append(hankaku_keyword)
            zenkaku_keyword = mojimoji.han_to_zen(keyword)
            zenkaku_change_keywords.append(zenkaku_keyword)

        change_keywords_lists = zip(hankaku_change_keywords, zenkaku_change_keywords)

        print(change_keywords_lists)

        sql_keywords = []

        # 全角または半角で得意先コード、得意先正式名、得意先名を抽出する
        for change_keyword in change_keywords_lists:
            sql_keywords.append(and_(
                                    or_(
                                        Customer.得意先コード.like(f'%{change_keyword[0]}%'),
                                        Customer.得意先コード.like(f'%{change_keyword[1]}%'),
                                        Customer.得意先正式名.like(f'%{change_keyword[0]}%'),
                                        Customer.得意先正式名.like(f'%{change_keyword[1]}%'),
                                        Customer.得意先名.like(f'%{change_keyword[0]}%'),
                                        Customer.得意先名.like(f'%{change_keyword[1]}%')
                                    )
                                )
                            )
        
        print(sql_keywords)

        # SQL文を実行
        customers = Customer.query.filter(*sql_keywords).all()

        # HTML作成
        db_result_customer_html = '<label for="customer-result">得意先検索結果</label>'
        # 得意先が存在する場合
        if customers:
            db_result_customer_html += '<select id="customer-result" class="form-control">'
            for customer in customers:
                db_result_customer_html += '<option value="{0}_{1}">{2}_{3}</option>'.format(customer.得意先コード, customer.得意先正式名, customer.得意先コード, customer.得意先正式名)
        else:
            db_result_customer_html += '<select id="customer-result" class="form-control text-primary">'
            db_result_customer_html += '<option>検索結果はありません</option>'
            db_result_customer_html += '</select>'
    
        return jsonify({
            'db_result_customer_area': '#db-result-customer-area',
            'db_result_customer_html': db_result_customer_html,
        })


@app.route('/db_rep_search', methods=['POST'])
def db_rep_search():
    """
    得意先検索結果リストを変更したときに、担当者コードを取得する処理
    """
    if request.method == 'POST':
        rep_number = request.form['rep_number']
        customer = Customer.query.filter_by(得意先コード=rep_number).first()
        
        if customer:
            return jsonify({'rep_number': customer.担当者コード})
        else:
            return jsonify({'rep_number': ''})


@app.route('/db_delivery_des_search', methods=['POST'])
def db_delivery_des_search():
    """
    納入先の検索処理
    検索キーワードは以下の5つ
        得意先コード、納入先コード、納入先正式名、納入先名、電話番号
    """
    if request.method == 'POST':
        customer_number = request.form['customer_number']
        delivery_des_keywords = request.form['delivery_des_keywords']

        # 全角スペースがある場合、半角スペースに変更する
        keywords_lists = delivery_des_keywords.replace('　', ' ').split()

        # 全角から半角へ 半角から全角へ変換
        hankaku_change_keywords = []
        zenkaku_change_keywords = []

        for keyword in keywords_lists:
            hankaku_keyword = mojimoji.zen_to_han(keyword)
            hankaku_change_keywords.append(hankaku_keyword)
            zenkaku_keyword = mojimoji.han_to_zen(keyword)
            zenkaku_change_keywords.append(zenkaku_keyword)

        change_keywords_lists = zip(hankaku_change_keywords, zenkaku_change_keywords)

        sql_keywords = []

        # 全角または半角で得意先コード、得意先正式名、得意先名を抽出する
        for change_keyword in change_keywords_lists:
            sql_keywords.append(and_(
                                DeliveryDestination.納入先コード.like(f'%{customer_number}%'),
                                or_(
                                    DeliveryDestination.納入先コード.like(f'%{change_keyword[0]}%'),
                                    DeliveryDestination.納入先コード.like(f'%{change_keyword[1]}%'),
                                    DeliveryDestination.納入先正式名.like(f'%{change_keyword[0]}%'),
                                    DeliveryDestination.納入先正式名.like(f'%{change_keyword[1]}%'),
                                    DeliveryDestination.納入先名.like(f'%{change_keyword[0]}%'),
                                    DeliveryDestination.納入先名.like(f'%{change_keyword[1]}%'),
                                    DeliveryDestination.電話番号_eidai.like(f'%{change_keyword[0]}%'),
                                    DeliveryDestination.電話番号_eidai.like(f'%{change_keyword[1]}%')
                                    )
                                )
                            )

        # SQL文を実行
        delivery_des = DeliveryDestination.query.filter(*sql_keywords).all()
        print('--------------------')
        print(delivery_des)
        # HTML作成
        db_result_delivery_des_html = f'<label for="delivery-destination-result">納入先検索結果</label>'
        # 納入先が存在する場合
        if delivery_des:
            db_result_delivery_des_html += f'<select id="delivery-destination-result" class="form-control">'
            for delivery in delivery_des:
                db_result_delivery_des_html += '<option value="{0}_{1}">{2}_{3}</option>'.format(delivery.納入先コード, delivery.納入先正式名, delivery.納入先コード, delivery.納入先正式名)
        else:
            db_result_delivery_des_html += f'<select id="delivery-destination-result" class="form-control text-primary">'
            db_result_delivery_des_html += '<option>検索結果はありません</option>'
            db_result_delivery_des_html += '</select>'
    
        return jsonify({
            'db_result_delivery_des_area':f'#db-result-delivery-des-area',
            'db_result_delivery_des_html': db_result_delivery_des_html
        })


@app.route('/db_search_auto', methods=['POST'])
def db_search_auto():
    """
    品番コード、品番名、規格の全検索処理
    """
    if request.method == "POST":
        keywords = request.form['keywords']
        box_number = request.form['box_number']

        # 全角スペースがある場合、半角スペースに変更する
        keywords_lists = keywords.replace('  ', ' ').split()

        # 全角から半角へ 半角から全角へ変換
        hankaku_change_keywords = []
        zenkaku_change_keywords = []
        for keyword in keywords_lists:
            hankaku_keyword = mojimoji.zen_to_han(keyword)
            hankaku_change_keywords.append(hankaku_keyword)
            zenkaku_keyword = mojimoji.han_to_zen(keyword)
            zenkaku_change_keywords.append(zenkaku_keyword)

        change_keywords_lists = zip(hankaku_change_keywords, zenkaku_change_keywords)
    
        sql_keywords = []

        # 全角OR半角で品番コード、品番名、規格を抽出する    
        for change_keyword in change_keywords_lists:
            sql_keywords.append(and_(
                                    or_(
                                        Product.品番コード.like(f'%{change_keyword[0]}%'),
                                        Product.品番コード.like(f'%{change_keyword[1]}%'),
                                        Product.品番名.like(f'%{change_keyword[0]}%'),
                                        Product.品番名.like(f'%{change_keyword[1]}%'),
                                        Product.規格.like(f'%{change_keyword[0]}%'),
                                        Product.規格.like(f'%{change_keyword[1]}%')
                                        )
                                    )
                                )
        # SQL文を実施
        items = Product.query.filter(*sql_keywords).all()

        # HTML作成
        db_all_html = f'<label for="db-all-{box_number}" class="h7">全件検索結果(リスト)</label>'
        if items:
            db_all_html += f'<select id="db-all-{box_number}" name="search-item-{box_number}" class="form-control">'
            for item in items:
                db_all_html += '<option value={0}>{1}_{2}_{3}</option>'.format(item.品番コード, item.品番コード, item.品番名, item.規格)
        else:
            db_all_html += f'<select id="db-all-{box_number}" name="search-item-{box_number}" class="form-control text-primary">'
            db_all_html += '<option>検索結果はありません</option>'
        db_all_html += '</select>'
        db_all_html += '<span></span>'

        return jsonify({'db_all_html': db_all_html,
                        'db_all_area': f'#result-box-{box_number}',
                        'number': box_number})


@app.route('/db_nothing_check', methods=['POST'])
def db_nothing_check():
    """
    選択した行の1行上が検索結果が存在しなかった場合メッセージを表示する
    """
    if request.method == "POST":
        select_change_number = request.form['select_change_number']
        item_code = request.form['item_label']
        product = Product.query.filter_by(品番コード=item_code).first()
        if product is None:
            # HTML作成
            db_no_html = f'<label for="db-list-{select_change_number}" class="h7">同上検索結果(リスト)</label>'
            db_no_html += f'<select id="db-list-{select_change_number}" name="same-above-{select_change_number}" class="form-control text-primary">'
            db_no_html += '<option>検索結果はありません</option>'
            db_no_html += '</select>'
            db_no_html += f'<span id="validate-same-message-{select_change_number}"></span>'

            return jsonify({'db_no_html': db_no_html,
                            'db_check_area': f'#db-check-{select_change_number}',
                            'number': select_change_number})


if __name__ == '__main__':
    """
    Flask起動
    """
    app.run(debug=True)