import pykakasi
import re
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app


db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = 'products'

    品番コード = db.Column(db.String(20), primary_key=True, nullable=False)
    品番名 = db.Column(db.String(40), nullable=False)
    品番カナ名 = db.Column(db.String(40), nullable=False)
    規格 = db.Column(db.String(40), nullable=False)
    品番区分 = db.Column(db.String(20))
    ブランドコード = db.Column(db.String(20))
    諸口フラグ = db.Column(db.String(20))
    在庫管理不要フラグ = db.Column(db.String(20))
    出荷伝票印字フラグ = db.Column(db.String(20))
    出荷不要フラグ = db.Column(db.String(20))
    源泉税対象フラグ = db.Column(db.String(20))
    取扱開始日 = db.Column(db.DateTime)
    取扱終了日 = db.Column(db.DateTime)
    製造中止日 = db.Column(db.DateTime)
    メーカー商品コード = db.Column(db.String(20))
    単位コード = db.Column(db.String(20), db.ForeignKey('units.単位コード'), nullable=False)
    JANCD = db.Column(db.String(20))
    ITFCD = db.Column(db.String(20))
    品種コード = db.Column(db.String(20))
    主要仕入先コード = db.Column(db.String(20))
    サイズ1 = db.Column(db.String(20))
    サイズ2 = db.Column(db.String(20))
    サイズ3 = db.Column(db.String(20))
    品番重量 = db.Column(db.String(20))
    集計コード1 = db.Column(db.String(20))
    集計コード2 = db.Column(db.String(20))
    集計コード3 = db.Column(db.String(20))
    荷姿管理不要フラグ = db.Column(db.String(20))
    ロット管理フラグ = db.Column(db.String(20))
    ロット別引当管理フラグ = db.Column(db.String(20))
    シリアル管理フラグ = db.Column(db.String(20))
    有効期限管理フラグ = db.Column(db.String(20))
    有効期限変換区分 = db.Column(db.String(20))
    受託品フラグ = db.Column(db.String(20))
    アソートフラグ = db.Column(db.String(20))
    セット品フラグ = db.Column(db.String(20))
    販売可能商品ランク = db.Column(db.String(20))
    棚卸評価基準 = db.Column(db.String(20))
    消費税内外区分 = db.Column(db.String(20))
    消費税率区分 = db.Column(db.String(20))
    個別在庫評価単価計算区分 = db.Column(db.String(20))
    ロット個別在庫評価フラグ = db.Column(db.String(20))
    販売原価計算区分 = db.Column(db.String(20))
    標準原価単価 = db.Column(db.String(20))
    商品摘要 = db.Column(db.String(20))
    P_S区分 = db.Column(db.String(20))
    上代本体単価 = db.Column(db.String(20))
    上代単価消費税 = db.Column(db.String(20))
    売上本体単価 = db.Column(db.String(20))
    売上単価消費税 = db.Column(db.String(20))
    仕入本体単価 = db.Column(db.String(20))
    仕入単価消費税 = db.Column(db.String(20))
    有効期限チェック月数 = db.Column(db.String(20))
    レコード削除不可フラグ = db.Column(db.String(20))
    英字品番名1 = db.Column(db.String(20))
    英字品番名2 = db.Column(db.String(20))
    基準量1 = db.Column(db.String(20))
    基準量2 = db.Column(db.String(20))
    商品展開補助起動区分 = db.Column(db.String(20))
    特性値パターンコード = db.Column(db.String(20))
    ロイヤリティ掛率 = db.Column(db.String(20))
    発注リードタイム日数 = db.Column(db.String(20))
    出庫準備日数 = db.Column(db.String(20))
    特定保守管理区分 = db.Column(db.String(20))
    クラス分類区分 = db.Column(db.String(20))
    商品区分 = db.Column(db.String(20))
    償還分類コード = db.Column(db.String(20))
    掛率単価取得区分 = db.Column(db.String(20))
    検品区分 = db.Column(db.String(20))
    GS1_128商品コード = db.Column(db.String(20))
    MEDIS_DC商品分類コード = db.Column(db.String(20))
    MEDIS_DCデータ区分 = db.Column(db.String(20))
    MEDIS_DC製造販売業者名 = db.Column(db.String(20))
    MEDIS_DC国内総販売元業者名 = db.Column(db.String(20))
    MEDIS_DCJMDNコード = db.Column(db.String(20))
    MEDIS_DC設置管理区分 = db.Column(db.String(20))
    MEDIS_DC修理区分 = db.Column(db.String(20))
    MEDIS_DC薬事申請上の販売名 = db.Column(db.String(20))
    MEDIS_DC製品番号 = db.Column(db.String(20))
    MEDIS_DC薬事法承認番号または届出番号 = db.Column(db.String(20))
    MEDIS_DC生物由来製品分類区分 = db.Column(db.String(20))
    MEDIS_DC毒劇区分 = db.Column(db.String(20))
    MEDIS_DC危険物区分 = db.Column(db.String(20))
    MEDIS_DC保管区分 = db.Column(db.String(20))
    滅菌有無区分 = db.Column(db.String(20))
    製造販売業者コード = db.Column(db.String(20))
    外国特例承認取得者コード = db.Column(db.String(20))
    選任製造販売業者コード = db.Column(db.String(20))
    内容量 = db.Column(db.String(20))
    貼付数 = db.Column(db.String(20))
    単回使用 = db.Column(db.String(20))
    歯科用金属組成成分名称 = db.Column(db.String(20))
    歯科用金属組成成分分量 = db.Column(db.String(20))
    滅菌方法 = db.Column(db.String(20))
    ラベル発行データ出力フラグ = db.Column(db.String(20))
    有効期限チェック区分 = db.Column(db.String(20))
    貸出返却必須フラグ = db.Column(db.String(20))
    資産分類コード = db.Column(db.String(20))
    プロジェクト種別コード = db.Column(db.String(20))
    プロジェクト原価科目区分 = db.Column(db.String(20))
    単位換算数量 = db.Column(db.String(20))
    分析4コード = db.Column(db.String(20))
    分析5コード = db.Column(db.String(20))
    特定商品区分 = db.Column(db.String(20))
    オペレータ警告区分 = db.Column(db.String(20))
    商品付属情報コード01 = db.Column(db.String(20))
    商品付属情報コード02 = db.Column(db.String(20))
    商品付属情報コード03 = db.Column(db.String(20))
    商品付属情報コード04 = db.Column(db.String(20))
    商品付属情報コード05 = db.Column(db.String(20))
    商品付属情報コード06 = db.Column(db.String(20))
    商品付属情報コード07 = db.Column(db.String(20))
    商品付属情報コード08 = db.Column(db.String(20))
    商品付属情報コード09 = db.Column(db.String(20))
    商品付属情報コード10 = db.Column(db.String(20))
    商品付属情報コード11 = db.Column(db.String(20))
    商品付属情報コード12 = db.Column(db.String(20))
    商品付属情報コード13 = db.Column(db.String(20))
    商品付属情報コード14 = db.Column(db.String(20))
    商品付属情報コード15 = db.Column(db.String(20))
    商品付属情報コード16 = db.Column(db.String(20))
    商品付属情報コード17 = db.Column(db.String(20))
    商品付属情報コード18 = db.Column(db.String(20))
    商品付属情報コード19 = db.Column(db.String(20))
    商品付属情報コード20 = db.Column(db.String(20))
    商品付属情報名称01 = db.Column(db.String(20))
    商品付属情報名称02 = db.Column(db.String(20))
    商品付属情報名称03 = db.Column(db.String(20))
    商品付属情報名称04 = db.Column(db.String(20))
    商品付属情報名称05 = db.Column(db.String(20))
    商品付属情報名称06 = db.Column(db.String(20))
    商品付属情報名称07 = db.Column(db.String(20))
    商品付属情報名称08 = db.Column(db.String(20))
    商品付属情報名称09 = db.Column(db.String(20))
    商品付属情報名称10 = db.Column(db.String(20))
    商品付属情報名称11 = db.Column(db.String(20))
    商品付属情報名称12 = db.Column(db.String(20))
    商品付属情報名称13 = db.Column(db.String(20))
    商品付属情報名称14 = db.Column(db.String(20))
    商品付属情報名称15 = db.Column(db.String(20))
    商品付属情報名称16 = db.Column(db.String(20))
    商品付属情報名称17 = db.Column(db.String(20))
    商品付属情報名称18 = db.Column(db.String(20))
    商品付属情報名称19 = db.Column(db.String(20))
    商品付属情報名称20 = db.Column(db.String(20))
    店舗発注区分 = db.Column(db.String(20))
    店舗発注仕入先最低単位数 = db.Column(db.String(20))
    店舗発注倉庫最低単位数 = db.Column(db.String(20))
    定期契約商品区分 = db.Column(db.String(20))
    売上仕入展開区分 = db.Column(db.String(20))
    日割計算区分 = db.Column(db.String(20))
    作業商品区分 = db.Column(db.String(20))
    点検パターンコード = db.Column(db.String(20))
    機械付帯情報パターンコード = db.Column(db.String(20))
    製番手配区分 = db.Column(db.String(20))
    製番原価科目区分 = db.Column(db.String(20))
    進行基準消費税内外区分 = db.Column(db.String(20))
    進行基準消費税率区分 = db.Column(db.String(20))
    仕入単位コード = db.Column(db.String(20))
    品番重量単位コード = db.Column(db.String(20))
    特性1 = db.Column(db.String(20))
    特性値1 = db.Column(db.String(20))
    特性2 = db.Column(db.String(20))
    特性値2 = db.Column(db.String(20))
    特性3 = db.Column(db.String(20))
    特性値3 = db.Column(db.String(20))
    特性4 = db.Column(db.String(20))
    特性値4 = db.Column(db.String(20))
    特性5 = db.Column(db.String(20))
    特性値5 = db.Column(db.String(20))
    特性6 = db.Column(db.String(20))
    特性値6 = db.Column(db.String(20))
    特性7 = db.Column(db.String(20))
    特性値7 = db.Column(db.String(20))
    特性8 = db.Column(db.String(20))
    特性値8 = db.Column(db.String(20))
    特性9 = db.Column(db.String(20))
    特性値9 = db.Column(db.String(20))
    特性10 = db.Column(db.String(20))
    特性値10 = db.Column(db.String(20))
    支払取引種類コード = db.Column(db.String(20))

    @classmethod
    def order_detail_query(cls, ai_item_code):
        """
        productsテーブルから商品コードを取得
        """
        res = re.match(r'\d{10}', ai_item_code)
        # 正規表現で品番コードが10桁であることをチェック
        if res:
            return cls.query.filter_by(品番コード=res.group()).first()
        elif ai_item_code == 'empty':
            return 'empty'
        else:
            return ai_item_code

    @classmethod
    def order_detail_update(cls, item_code):
        """
        CSV編集画面から商品コードを更新
        """
        res = re.match(r'\d{10}', item_code)
        # 正規表現で品番コードが10桁であることをチェック
        if res:
            product = cls.query.filter_by(品番コード=res.group()).first()
            return product.品番コード
        else:
            return ''


class Customer(db.Model):
    """
    テーブル名：得意先マスタ
    """
    __tablename__ = 'customers'
    
    得意先コード = db.Column(db.Integer, primary_key=True)
    得意先正式名 = db.Column(db.String(255))
    得意先名 = db.Column(db.String(120))
    得意先カナ名 = db.Column(db.String(120))
    郵便番号1 = db.Column(db.String(10))
    郵便番号2 = db.Column(db.String(10))
    住所1 = db.Column(db.String(120))
    住所2 = db.Column(db.String(120))
    住所3 = db.Column(db.String(10))
    住所4 = db.Column(db.String(10))
    住所5 = db.Column(db.String(10))
    電話番号1_1 = db.Column(db.String(10))
    電話番号1_2 = db.Column(db.String(10))
    電話番号1_3 = db.Column(db.String(10))
    内線番号 = db.Column(db.String(10))
    電話番号2_1 = db.Column(db.String(10))
    電話番号2_2 = db.Column(db.String(10))
    電話番号2_3 = db.Column(db.String(10))
    内線番号2 = db.Column(db.String(10))
    FAX番号1_1 = db.Column(db.String(10))
    FAX番号1_2 = db.Column(db.String(10))
    FAX番号1_3 = db.Column(db.String(10))
    電話番号 = db.Column(db.String(10))
    FAX番号 = db.Column(db.String(10))
    担当部署名 = db.Column(db.String(10))
    担当役職名 = db.Column(db.String(10))
    担当者名 = db.Column(db.String(10))
    メールアドレス = db.Column(db.String(10))
    請求先コード = db.Column(db.String(10))
    担当者コード = db.Column(db.String(10))
    担当者異動日付 = db.Column(db.String(10))
    新担当者コード = db.Column(db.String(10))
    在庫管理事業所コード = db.Column(db.Integer)
    諸口フラグ = db.Column(db.String(10))
    セグメントコード1 = db.Column(db.Integer)
    セグメントコード2 = db.Column(db.Integer)
    セグメントコード3 = db.Column(db.String(10))
    販売可能商品ランク = db.Column(db.Integer)
    見積書即伝区分 = db.Column(db.Integer)
    受注確認書不要フラグ = db.Column(db.String(10))
    受注確認書即伝区分 = db.Column(db.Integer)
    納品書不要フラグ = db.Column(db.String(10))
    納品書即伝区分 = db.Column(db.Integer)
    納品書区分 = db.Column(db.Integer)
    指定伝票必要フラグ = db.Column(db.String(10))
    指定伝票パターン = db.Column(db.String(10))
    特定商品譲受書必要フラグ = db.Column(db.String(10))
    納品書特定商品印字必要フラグ = db.Column(db.String(10))
    委託伝票不要フラグ = db.Column(db.String(10))
    DM不要フラグ = db.Column(db.String(10))
    売上計上基準 = db.Column(db.Integer)
    債権科目区分 = db.Column(db.Integer)
    取引開始日 = db.Column(db.String(50))
    取引終了日 = db.Column(db.String(50))
    会計用取引先コード = db.Column(db.Integer)
    伝票最大行数 = db.Column(db.Integer)
    有効期限チェック区分 = db.Column(db.Integer)
    基本通貨コード = db.Column(db.Integer)
    地区コード = db.Column(db.Integer)
    得意先区分 = db.Column(db.Integer)
    COD対象フラグ = db.Column(db.String(10))
    届出許可区分 = db.Column(db.Integer)
    届出期限日 = db.Column(db.String(10))
    貸出伝票単価印字必要フラグ = db.Column(db.String(10))
    納品書送付先区分 = db.Column(db.Integer)
    法人番号 = db.Column(db.String(10))
    分析1コード = db.Column(db.String(10))
    分析2コード = db.Column(db.String(10))
    分析3コード = db.Column(db.String(10))
    取引形態区分 = db.Column(db.String(10))
    業態区分 = db.Column(db.String(10))
    坪数 = db.Column(db.String(10))
    営業開始日 = db.Column(db.String(10))
    営業終了日 = db.Column(db.String(10))
    営業開始時間 = db.Column(db.String(10))
    営業終了時間 = db.Column(db.String(10))
    店舗ランク = db.Column(db.String(10))
    店舗分類区分1 = db.Column(db.String(10))
    店舗分類区分2 = db.Column(db.String(10))
    店舗分類区分3 = db.Column(db.String(10))
    店舗分類区分4 = db.Column(db.String(10))
    店舗分類区分5 = db.Column(db.String(10))
    店舗分類区分6 = db.Column(db.String(10))
    店舗分類区分7 = db.Column(db.String(10))
    店舗分類区分8 = db.Column(db.String(10))
    店舗分類区分9 = db.Column(db.String(10))
    店舗分類区分10 = db.Column(db.String(10))
    出荷売上区分 = db.Column(db.String(10))
    移動積送管理FLG = db.Column(db.String(10))
    倉庫ランク = db.Column(db.String(10))
    代表振分パターンコード = db.Column(db.String(10))
    代表納入先コード = db.Column(db.String(10))
    代表振分係数 = db.Column(db.String(50))
    代表優先順 = db.Column(db.Integer)
    レコード削除不可フラグ = db.Column(db.String(10))
    小計対象 = db.Column(db.Integer)
    配送業者コード = db.Column(db.String(10))
    ジャケット1 = db.Column(db.String(100))
    ジャケット2 = db.Column(db.String(100))
    エルボ1 = db.Column(db.String(100))
    エルボ2 = db.Column(db.String(100))
    その他1 = db.Column(db.String(100))
    その他2 = db.Column(db.String(100))
    予備項目1_区分 = db.Column(db.String(100))
    予備項目2_区分 = db.Column(db.String(100))
    予備項目3_区分 = db.Column(db.String(100))
    予備項目1_数値 = db.Column(db.String(100))
    予備項目2_数値 = db.Column(db.String(100))
    予備項目3_数値 = db.Column(db.String(100))
    予備項目1_文字 = db.Column(db.String(100))
    予備項目2_文字 = db.Column(db.String(100))
    予備項目3_文字 = db.Column(db.String(100))


class Supply(db.Model):
    """
    テーブル名：仕入先マスタ
    """
    __tablename__ = 'suppliers'

    仕入先コード = db.Column(db.Integer)
    仕入先正式名 = db.Column(db.String(120))
    仕入先名 = db.Column(db.String(120))
    仕入先カナ名 = db.Column(db.String(50))
    郵便番号1 = db.Column(db.String(10))
    郵便番号2 = db.Column(db.String(10))
    住所1 = db.Column(db.String(255))
    住所2 = db.Column(db.String(120))
    住所3 = db.Column(db.String(10))
    住所4 = db.Column(db.String(10))
    住所5 = db.Column(db.String(10))
    電話番号1_1 = db.Column(db.String(10))
    電話番号1_2 = db.Column(db.String(10))
    電話番号1_3 = db.Column(db.String(10))
    内線番号1 = db.Column(db.String(10))
    電話番号2_1 = db.Column(db.String(10))
    電話番号2_2 = db.Column(db.String(10))
    電話番号2_3 = db.Column(db.String(10))
    内線番号2 = db.Column(db.String(10))
    FAX番号1_1 = db.Column(db.String(10))
    FAX番号1_2 = db.Column(db.String(10))
    FAX番号1_3 = db.Column(db.String(10))
    TEL = db.Column(db.String(10))
    FAX = db.Column(db.String(10))
    担当部署名 = db.Column(db.String(10))
    担当役職名 = db.Column(db.String(10))
    担当者名 = db.Column(db.String(10))
    メールアドレス = db.Column(db.String(10))
    支払先コード = db.Column(db.String(10), primary_key=True, nullable=False)
    担当者コード = db.Column(db.Integer)
    担当者異動日付 = db.Column(db.String(10))
    新担当者コード = db.Column(db.String(10))
    在庫管理事業所コード = db.Column(db.Integer)
    諸口フラグ = db.Column(db.String(10))
    セグメントコード1 = db.Column(db.Integer)
    セグメントコード2 = db.Column(db.Integer)
    セグメントコード3 = db.Column(db.String(10))
    発注書不要フラグ = db.Column(db.String(10))
    発注書即伝区分 = db.Column(db.Integer)
    DM不要フラグ = db.Column(db.String(10))
    入荷入力計上元 = db.Column(db.Integer)
    仕入計上基準 = db.Column(db.Integer)
    債務科目区分 = db.Column(db.Integer)
    取引開始日 = db.Column(db.String(50))
    取引終了日 = db.Column(db.String(10))
    会計用取引先コード = db.Column(db.Integer)
    伝票最大行数 = db.Column(db.Integer)
    有効期限チェック区分 = db.Column(db.Integer)
    基本通貨コード = db.Column(db.Integer)
    加工先フラグ = db.Column(db.String)
    有償支給用得意先コード = db.Column(db.String(10))
    製造指示書パターン区分 = db.Column(db.Integer)
    下請対象フラグ = db.Column(db.String(10))
    発注書パターン区分 = db.Column(db.Integer)
    レコード削除不可フラグ = db.Column(db.Integer)
    法人番号 = db.Column(db.String(10))
    分析1コード = db.Column(db.String(10))
    分析2コード = db.Column(db.String(10))
    分析3コード = db.Column(db.String(10))
    最低発注金額 = db.Column(db.Integer)
    旅費経費連携フラグ = db.Column(db.String(10))
    発注内示書不要フラグ = db.Column(db.String(10))


class DeliveryDestination(db.Model):
    """
    テーブル名：納入先マスタ
    """
    __tablename__ = 'delivery_destinations'

    納入先コード = db.Column(db.Integer, primary_key=True, nullable=False)
    納入先正式名 = db.Column(db.String(120))
    納入先名 = db.Column(db.String(255))
    納入先カナ名 = db.Column(db.String(120))
    郵便番号1 = db.Column(db.String(10))
    郵便番号2 = db.Column(db.String(10))
    住所1 = db.Column(db.String(255))
    住所2 = db.Column(db.String(255))
    住所3 = db.Column(db.String(255))
    住所4 = db.Column(db.String(255))
    住所5 = db.Column(db.String(255))
    電話番号1_1 = db.Column(db.String(10))
    電話番号1_2 = db.Column(db.String(10))
    電話番号1_3 = db.Column(db.String(10))
    電話番号_eidai = db.Column(db.String(20))
    内線番号1 = db.Column(db.String(10))
    電話番号2_1 = db.Column(db.String(10))
    電話番号2_2 = db.Column(db.String(10))
    電話番号2_3 = db.Column(db.String(10))
    内線番号2 = db.Column(db.String(10))
    FAX番号1_1 = db.Column(db.String(10))
    FAX番号1_2 = db.Column(db.String(10))
    FAX番号1_3 = db.Column(db.String(10))
    電話番号 = db.Column(db.String(10))
    FAX番号 = db.Column(db.String(10))
    担当部署名 = db.Column(db.String(10))
    担当役職名 = db.Column(db.String(10))
    担当者名 = db.Column(db.String(10))
    メールアドレス = db.Column(db.String(10))
    担当者コード = db.Column(db.Integer)
    担当者異動日付 = db.Column(db.String(10))
    新担当者コード = db.Column(db.String(10))
    諸口フラグ = db.Column(db.String(10))
    セグメントコード1 = db.Column(db.String(10))
    セグメントコード2 = db.Column(db.String(10))
    セグメントコード3 = db.Column(db.String(10))
    指定伝票必要フラグ = db.Column(db.String(10))
    指定伝票パターン = db.Column(db.String(10))
    特定商品譲受書必要フラグ = db.Column(db.String(10))
    DM不要フラグ = db.Column(db.String(10))
    取引開始日 = db.Column(db.String(10))
    取引終了日 = db.Column(db.String(10))
    送り先区分 = db.Column(db.Integer)
    レコード削除不可フラグ = db.Column(db.String(10))
    法人番号 = db.Column(db.String(10))
    配送業者 = db.Column(db.String(10))
    得意先コード_旭 = db.Column(db.Integer)
    納入先コード_旭 = db.Column(db.Integer)


class CutomerSupply(db.Model):
    """
    テーブル名：得意先納入先マスタ
    """
    __tablename__ = 'customers_suppliers'

    得意先コード = db.Column(db.Integer)
    納入先コード = db.Column(db.Integer, primary_key=True, nullable=False)
    倉庫コード = db.Column(db.String(10))


class BillingDeadline(db.Model):
    """
    テーブル名：請求締日マスタ
    """
    __tablename__ = 'billing_deadlines'

    請求先コード = db.Column(db.Integer, primary_key=True, nullable=False)
    現場コード = db.Column(db.String(10))
    請求締日 = db.Column(db.Integer)
    基準金額未満 = db.Column(db.Integer)
    回収月区分 = db.Column(db.Integer)
    回収日 = db.Column(db.Integer)
    サイト = db.String(db.String(10))
    支払方法コード = db.Column(db.Integer)


class Unit(db.Model):
    """
    テーブル名：単位マスタ
    """
    __tablename__ = 'units'

    単位コード = db.Column(db.String(20), primary_key=True, nullable=False)
    単位名 = db.Column(db.String(50))
    単位記号 = db.Column(db.String(10))
    英字単位記号 = db.Column(db.String(10))
    単位区分 = db.Column(db.Integer)
    数量小数以下桁数 = db.Column(db.Integer)
    レコード削除不可フラグ = db.Column(db.String(10))
    # リレーション One to Many
    product = db.relationship('Product', backref='units')


class Time(db.Model):
    """
    テーブル名：時間マスタ
    """
    __tablename__ = 'times'

    Shubetu = db.Column(db.Integer)
    CDValue = db.Column(db.Integer)
    Hyouzijun = db.Column(db.Integer, primary_key=True, nullable=False)
    ShubetuName = db.Column(db.String(10))
    CDName = db.Column(db.String(50))


class DeliveryCompanyTime(db.Model):
    """
    テーブル名：配送業者⇒時間マスタ
    """
    __tablename__ = 'delivery_company_times'
    
    ZigyoushoCD = db.Column(db.String(10), primary_key=True, nullable=False)
    SoukoCD = db.Column(db.String(10))
    HaisouGyoushaCD = db.Column(db.String(10))
    Jikan = db.Column(db.String(10))


class Order(db.Model):
    """
    テーブル名：受注確認書ヘッダ
    """
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    deleted_at = db.Column(db.DateTime)
    仮伝票番号 = db.Column(db.String(12))
    ヘッダ受注区分 = db.Column(db.SmallInteger, default='1')
    事業所コード = db.Column(db.String(6), default='100')
    受注日 = db.Column(db.DateTime)
    ヘッダ出荷日 = db.Column(db.DateTime)
    ヘッダ納期 = db.Column(db.DateTime)
    ヘッダ売上予定日 = db.Column(db.DateTime)
    担当者コード = db.Column(db.String(10))
    得意先コード = db.Column(db.String(10))
    請求先コード = db.Column(db.String(10))
    請求帳端区分 = db.Column(db.SmallInteger, default='0')
    回収予定日 = db.Column(db.DateTime)
    回収方法コード = db.Column(db.String(5))
    納入先コード = db.Column(db.String(10))
    仕入先コード = db.Column(db.String(10))
    支払先コード = db.Column(db.String(10))
    支払帳端区分 = db.Column(db.SmallInteger, default='0')
    # 外部キー設定必要 支払締切マスタなし
    支払予定日 = db.Column(db.DateTime)
    # 外部キー設定必要 支払締切マスタなし
    支払方法コード = db.Column(db.String(5))
    ヘッダ倉庫コード = db.Column(db.String(10), default='100')
    ヘッダ得意先注文番号 = db.Column(db.String(30))
    # 外部キー設定必要
    配送業者コード = db.Column(db.String(10))
    時間 = db.Column(db.String(2), default='99')
    伝票摘要コード = db.Column(db.String(2))
    伝票摘要 = db.Column(db.String(40))
    社内摘要コード = db.Column(db.String(2))
    社内摘要 = db.Column(db.String(40))
    # リレーション
    order_details = db.relationship('OrderDetail', backref='orders')

    def __init__(self, 仮伝票番号, 受注日, ヘッダ出荷日, ヘッダ納期, ヘッダ売上予定日,
                    担当者コード, 得意先コード, 請求先コード, 回収予定日, 回収方法コード,
                    納入先コード, 仕入先コード, 支払先コード, 支払予定日, 支払方法コード,
                    ヘッダ得意先注文番号, 配送業者コード,
                    時間, 伝票摘要コード, 伝票摘要, 社内摘要コード, 社内摘要):

        self.仮伝票番号 = 仮伝票番号
        self.受注日 = 受注日
        self.ヘッダ出荷日 = ヘッダ出荷日
        self.ヘッダ納期 = ヘッダ納期
        self.ヘッダ売上予定日 = ヘッダ売上予定日
        self.担当者コード = 担当者コード
        self.得意先コード = 得意先コード
        self.請求先コード = 請求先コード
        self.回収予定日 = 回収予定日
        self.回収方法コード = 回収方法コード
        self.納入先コード = 納入先コード
        self.仕入先コード = 仕入先コード
        self.支払先コード = 支払先コード
        self.支払予定日 = 支払予定日
        self.支払方法コード = 支払方法コード
        self.ヘッダ得意先注文番号 = ヘッダ得意先注文番号
        self.配送業者コード = 配送業者コード
        self.時間 = 時間
        self.伝票摘要コード = 伝票摘要コード
        self.伝票摘要 = 伝票摘要
        self.社内摘要コード = 社内摘要コード
        self.社内摘要 = 社内摘要
    
    def create_order(self):
        db.session.add(self)


class OrderDetail(db.Model):
    """
    テーブル名：明細テーブル
    """
    __tablename__ = "order_details"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    deleted_at = db.Column(db.DateTime)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    明細行番号 = db.Column(db.SmallInteger)
    明細受注区分 = db.Column(db.SmallInteger)
    債権科目区分 = db.Column(db.SmallInteger, default='1130')
    明細倉庫コード = db.Column(db.String(10))
    商品コード = db.Column(db.String(10))
    AI判定商品コード1 = db.Column(db.String(10))
    AI判定商品コード2 = db.Column(db.String(10))
    AI判定商品コード3 = db.Column(db.String(10))
    AI判定商品コード4 = db.Column(db.String(10))
    AI判定商品コード5 = db.Column(db.String(10))
    売上税率区分 = db.Column(db.SmallInteger, default='0')
    仕入税率区分 = db.Column(db.SmallInteger, default='0')
    明細数量 = db.Column(db.DECIMAL(10, 6))
    PS区分 = db.Column(db.SmallInteger, default='0')
    売上単価 = db.Column(db.DECIMAL(10, 6))
    売上金額 = db.Column(db.DECIMAL(10, 6))
    売上消費税額 = db.Column(db.DECIMAL(10, 0))
    明細出荷日 = db.Column(db.DateTime)
    明細受注納期 = db.Column(db.DateTime)
    明細売上予定日 = db.Column(db.DateTime)
    受注明細摘要コード = db.Column(db.String(40))
    受注明細摘要 = db.Column(db.String(40))
    仕入単価 = db.Column(db.DECIMAL(10, 6))
    仕入金額 = db.Column(db.DECIMAL(10, 6))
    仕入消費税額 = db.Column(db.DECIMAL(10, 0))
    入荷予定日 = db.Column(db.DateTime)
    仕入予定日 = db.Column(db.DateTime)
    内訳行番号 = db.Column(db.SmallInteger, default='1')
    内訳数量 = db.Column(db.Integer)

    def __init__(self, order_id, 明細行番号, 明細受注区分, 明細倉庫コード, 商品コード,
                        AI判定商品コード1, AI判定商品コード2, AI判定商品コード3, AI判定商品コード4, AI判定商品コード5,
                        明細数量, 明細出荷日, 明細受注納期, 明細売上予定日,
                        受注明細摘要コード, 受注明細摘要, 入荷予定日, 仕入予定日, 内訳数量):

        self.order_id = order_id
        self.明細行番号 = 明細行番号
        self.明細受注区分 = 明細受注区分
        self.明細倉庫コード = 明細倉庫コード
        self.商品コード = 商品コード
        self.AI判定商品コード1 = AI判定商品コード1
        self.AI判定商品コード2 = AI判定商品コード2
        self.AI判定商品コード3 = AI判定商品コード3
        self.AI判定商品コード4 = AI判定商品コード4
        self.AI判定商品コード5 = AI判定商品コード5
        self.明細数量 = 明細数量
        self.明細出荷日 = 明細出荷日
        self.明細受注納期 = 明細受注納期
        self.明細売上予定日 = 明細売上予定日
        self.受注明細摘要コード = 受注明細摘要コード
        self.受注明細摘要 = 受注明細摘要
        self.入荷予定日 = 入荷予定日
        self.仕入予定日 = 仕入予定日
        self.内訳数量 = 内訳数量

# class Image(db.Model):
#     __tablename__ = 'images'

#     得意先コード = db.Column(db.String(20), primary_key=True, nullable=False)
#     ML商品幅 = db.Column(db.Integer, nullable=False)
#     ML商品高さ = db.Column(db.Integer, nullable=False)


class MlImage(db.Model):
    __tablename__ = 'ml_images'

    得意先コード = db.Column(db.String(20), primary_key=True, nullable=False)
    ML商品ステータス = db.Column(db.Integer, nullable=False)
    ML商品幅 = db.Column(db.Integer, nullable=False)
    ML商品高さ = db.Column(db.Integer, nullable=False)


class Kakashi:
    """
    ファイルをアップロードした時の漢字をローマ字に変換
    """
    kakashi = pykakasi.kakasi()
    kakashi.setMode('H', 'a')
    kakashi.setMode('K', 'a')
    kakashi.setMode('J', 'a')
    conv = kakashi.getConverter()

    @classmethod
    def japanese_to_ascii(cls, japanese):
        return cls.conv.do(japanese)


class LineDict(dict):
    """
    FLASKからHTMLへデータを送る時に、辞書型に変換させるクラス
    """
    def __missing__(self, key):
        v = self[key] = type(self)()
        return v
