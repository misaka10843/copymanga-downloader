import os
import zipfile

import config


def create_cbz(index, title, manga_name, save_dir, cbz_dir, path_word):
    xml_data = f'<?xml version="1.0"?>' \
               '<ComicInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" ' \
               'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' \
               f'<Title>{title}</Title>' \
               f'<Series>{manga_name}</Series>' \
               f'<Number>{index}</Number>' \
               f'</ComicInfo>'
    with open(os.path.join(os.path.join(config.SETTINGS['download_path'], save_dir), "ComicInfo.xml"), "w",
              encoding='utf8') as file:
        file.write(xml_data)

    start_dir = os.path.join(config.SETTINGS['download_path'], save_dir)
    file_name = f"{manga_name}-{title}.cbz"
    cbz_dir = os.path.join(cbz_dir, path_word)
    file_path = os.path.join(cbz_dir, file_name)

    # 检测漫画保存目录是否存在
    if not os.path.exists(cbz_dir):
        os.makedirs(cbz_dir)

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
