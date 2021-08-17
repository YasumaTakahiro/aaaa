from flask import Flask
import pymysql


# インスタンス生成
app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x89\xf1 ^L]*r\x97l\xcf\xadr\x03\xf2Z'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# SQLAlchemy DB設定
# ローカル
db_uri = 'mysql+pymysql://asahi-prod:eidai2021@localhost:3307/asahi-db?charset=utf8'
# GCP
# db_uri = 'mysql+pymysql://root:eidai2021@34.84.21.194:3306/asahi?charset=utf8'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False


def getConncection():
    """
    直接SQL文を使用する場合の関数
    """
    # データベースの接続情報 ローカル
    return pymysql.connect(
        host='localhost',
        port=3307,
        db='asahi-db',
        user='asahi-prod',
        password='eidai2021',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    # データベースの接続情報 GCP
    # return pymysql.connect(
    #     host='34.84.21.194',
    #     port=3306,
    #     db='asahi',
    #     user='root',
    #     password='eidai2021',
    #     charset='utf8',
    #     cursorclass=pymysql.cursors.DictCursor
    # )
