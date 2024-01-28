import os
import zipfile

from xpinyin import Pinyin

import config


def create_cbz(index, title, manga_name, save_dir, cbz_dir):
    pinyin = Pinyin()
    xml_data = f"<?xml version=\"1.0\"?>\n<ComicInfo xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" " \
               f"xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n  " \
               f"<Title>{pinyin.get_pinyin(title)}</Title>\n  " \
               f"<Series>{pinyin.get_pinyin(manga_name)}</Series>\n  " \
               f"<Number>{pinyin.get_pinyin(index)}</Number>\n" \
               f"</ComicInfo>"
    with open(os.path.join(os.path.join(config.SETTINGS['download_path'], save_dir), "ComicInfo.xml"), "w") as file:
        file.write(xml_data)

    start_dir = os.path.join(config.SETTINGS['download_path'], save_dir)
    file_name = f"{save_dir}/{pinyin.get_pinyin(manga_name)}/{manga_name}{title}.cbz"
    file_path = os.path.join(cbz_dir, file_name)

    # 只添加指定类型的文件到zip文件中
    allowed_ext = ['.xml', '.jpg', '.png', '.jpeg', '.webp']
    with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for dir_path, dir_names, filenames in os.walk(start_dir):
            fpath = dir_path.replace(start_dir, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                ext = os.path.splitext(filename)[1].lower()
                if ext in allowed_ext:
                    zip_file.write(os.path.join(dir_path, filename), fpath + filename)
