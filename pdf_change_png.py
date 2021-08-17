import os
import glob
import datetime
from pathlib import Path
from pdf2image import convert_from_path


def pdf_change(pdf_file, png_path, fmt='png', dpi=200):
    '''
    PDFからPNGへ拡張子を変換する
    '''
    pdf_path = Path(pdf_file)
    png_dir = Path(png_path)
    pages = convert_from_path(pdf_path, dpi)
    png_name = []
    # PDFファイルを1ページずつ保存
    for i, page in enumerate(pages):
        date = datetime.datetime.now().strftime('%Y_%m%d_%H%M_%S')
        png_file_name = '{0}_{1}_{2:02d}p.{3}'.format(pdf_file.stem, date, i + 1, fmt)
        png_output_path = png_dir / png_file_name
        print(png_output_path)
        page.save(png_output_path, fmt)
        png_name.append(png_output_path)


def png_confirm():
    '''
    PDFからPNGへ変換したファイルを取得する
    '''
    late_png_files = glob.glob('./static/images/pdf_change_pngs/*.png')
    late_png_file = max(late_png_files, key=os.path.getctime)
    return os.path.basename(late_png_file)
