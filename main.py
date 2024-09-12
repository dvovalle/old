from os import path, remove
import sqlite3
import re
import unicodedata
from log_error import set_logging_exception
from enum import Enum

conn = sqlite3.connect(database="database.db", timeout=2.0)
cursor = conn.cursor()

__DIR_PATH = path.dirname(path.realpath(__file__))
__LISTA_COMPLETA: str = f'{__DIR_PATH}/M3UListas/listaCompleta.m3u'
__LISTA_ALL: str = f'{__DIR_PATH}/M3UListas/listaFULL.m3u'


class SQLAction(Enum):
    INSERT: int = 1
    UPDATE: int = 2
    INSERT_AND_REMOVE: int = 3
    UPDATE_AND_REMOVE: int = 4    


def __start_backup() -> None:
    conn_old = sqlite3.connect(database="iptv.db", timeout=2.0)
    cursor_old = conn_old.cursor()
    command: str = 'SELECT origem, url, id, name, logo, grupo, subgrupo, title, ativo, online FROM tb_iptv order by grupo ASC, name ASC;'
    res = cursor_old.execute(command)
    listold: list = res.fetchall()
    if listold is not None:
        for x in listold:
            try:
                cursor.execute(
                    'INSERT INTO tb_iptv (origem, url, id, name, logo, grupo, subgrupo, titulo, ativo, online) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                    (x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]))
            except Exception as err:
                print(f'******** -> Erro: {err}')

    conn.commit()


def get_el(texto: str, tag_name: str, ate_fim: bool) -> str:
    result: str = '0'
    start: int = texto.find(tag_name)
    if start > 2:
        texto_aux: str = texto.replace(tag_name, '')[start:]
        end: int = texto_aux.find('"')
        if ate_fim:
            result = f'"{texto_aux}'
        else:
            result = texto_aux[:end]

    return result


def extract(line: str) -> dict:
    m = re.search("tvg-name=\"(.*?)\"", line)
    name = m.group(1) if (m is not None) else ''

    m = re.search("tvg-id=\"(.*?)\"", line)
    tvg_id = m.group(1) if (m is not None) else ''

    m = re.search("tvg-logo=\"(.*?)\"", line)
    logo = m.group(1) if (m is not None) else ''

    m = re.search("group-title=\"(.*?)\"", line)
    group = m.group(1) if (m is not None) else ''

    m = re.search("pltv-subgroup=\"(.*?)\"", line)
    sub_group = m.group(1) if (m is not None) else ''

    m = re.search("ativo=\"(.*?)\"", line)
    ativo = m.group(1) if (m is not None) else ''

    m = re.search("[,](?!.*[,])(.*?)$", line)
    title = m.group(1) if (m is not None) else ''

    return dict({"title": str(title),
                 "tvg-name": str(name),
                 "tvg-id": str(tvg_id),
                 "tvg-logo": str(logo),
                 "tvg-group": str(group),
                 "ativo": str(ativo),
                 "pltv-subgroup": str(sub_group)})


def _exists_db(cmd: str) -> bool:
    res = cursor.execute(cmd)
    # res_value = res.fetchone()
    return res.fetchone()


def __remove_char(texto: str, force: bool) -> str:
    if texto is None:
        texto = ''

    txt_value: str = str(texto.replace('(', '')).strip()
    txt_value = txt_value.replace(')', '')
    txt_value = txt_value.replace('[', '')
    txt_value = txt_value.replace(']', '')
    txt_value = txt_value.replace('º', '')
    txt_value = txt_value.replace('ª', '')
    txt_value = txt_value.replace('{', '')
    txt_value = txt_value.replace('}', '')
    txt_value = txt_value.replace('/', '')
    txt_value = txt_value.replace('\\', '')
    txt_value = txt_value.replace('-', '')
    txt_value = txt_value.replace('#', '')
    txt_value = txt_value.replace('!', '')
    txt_value = txt_value.replace(',', '')
    txt_value = txt_value.replace('.', '')
    txt_value = txt_value.replace('_', '')
    txt_value = txt_value.replace('@', '')
    txt_value = txt_value.replace('&', '')
    txt_value = txt_value.replace('*', '')
    txt_value = txt_value.replace('+', '')
    txt_value = txt_value.replace('$', '')
    txt_value = txt_value.replace('%', '')
    txt_value = txt_value.replace('ç', 'c')
    txt_value = txt_value.replace('Ç', 'C')
    txt_value = txt_value.replace('?', '')
    txt_value = txt_value.replace('Á', 'A')
    txt_value = txt_value.replace('á', 'a')
    txt_value = txt_value.replace('Ã', 'A')
    txt_value = txt_value.replace('Â', 'A')
    txt_value = txt_value.replace('À', 'A')
    txt_value = txt_value.replace('ã', 'a')
    txt_value = txt_value.replace('É', 'E')
    txt_value = txt_value.replace('é', 'e')
    txt_value = txt_value.replace('  ', ' ')
    val_unicode = unicodedata.normalize(
        "NFD", txt_value).encode("ascii", "ignore")
    txt_value = val_unicode.decode("utf-8")
    result: str = re.sub(' +', ' ', txt_value)

    if force:
        result = str(re.sub(r'[^a-zA-Z0-9 ]', r'', txt_value)).strip()

    result = result.replace('  ', ' ')
    return result.strip()


def read_file(file_m3u: str, action: SQLAction, expire: str) -> None:
    count: int = 0
    name: str = ''
    logo: str = ''
    group: str = ''
    sub_group: str = ''
    title: str = ''
    id_iptv: str = ''
    ativo: str = ''
    is_completo: bool = False
    num_lines: int = 0

    with open(file=file_m3u, mode='r', encoding="utf-8") as file:
        num_lines = sum(1 for _ in file)

    with open(file=file_m3u, mode='r', encoding="utf-8") as file:
        while num_lines >= count:
            try:
                count += 1
                line = file.readline()
                if line is not None and len(line) > 0:
                    if line.find('EXTINF:') >= 0:
                        is_completo = True
                        linha = line.strip()
                        dict_value = extract(line=linha)
                        name = str(dict_value['tvg-name']).strip()
                        logo = str(dict_value['tvg-logo']).strip()
                        group = str(dict_value['tvg-group']).strip()
                        sub_group = str(dict_value['pltv-subgroup']).strip()
                        title = str(dict_value['title']).strip()
                        id_iptv = str(dict_value['tvg-id']).strip()
                        ativo = str(dict_value['ativo']).strip()

                        if len(ativo) <= 0:
                            ativo = '1'

                        if len(logo) < 4:
                            logo = '0'

                        if len(group) < 2:
                            group = '0'

                        if len(sub_group) < 2:
                            sub_group = group

                        if len(name) < 2:
                            name = '0'                            

                        if len(title) < 2:
                            title = '0'

                        if len(title) < 2:
                            title = name

                        if len(title) > 2:
                            name = title

                        if len(id_iptv) < 5:
                            id_iptv = '0'

                    name = __remove_char(texto=name, force=True)
                    title = __remove_char(texto=title, force=True)
                    group = __remove_char(texto=group, force=False)

                    if is_completo and line.find('http') == 0:
                        is_completo = False
                        url = line.strip()
                        try:

                            cursor.execute('INSERT INTO tb_iptv (url, id, name, logo, grupo, subgrupo, titulo, tipo, ativo, expire) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (url, id_iptv, name, logo, group, sub_group, title, "IPTV", ativo, expire))
                            print(f'INSERT: Title: {title} - {count} de {num_lines}')

                        except Exception as err:
                            is_completo = False
                            if action == SQLAction.UPDATE or action == SQLAction.UPDATE_AND_REMOVE:
                                cursor.execute('UPDATE tb_iptv SET url=?, id=?, logo=?, titulo=?, expire=? WHERE name=?;', (url, id_iptv, logo, title, expire, name))                                
                                print(f'UPDATE: Title: {title} - {count} de {num_lines} - Err: {err}')

            except Exception as err:
                set_logging_exception(exc=err)
                is_completo = False

        conn.commit()

        if action == SQLAction.INSERT_AND_REMOVE or action == SQLAction.UPDATE_AND_REMOVE:
            if path.exists(file_m3u):
                remove(file_m3u)


def get_sql(is_full: bool) -> list:
    command: str = "SELECT url, id, name, logo, grupo, subgrupo, titulo, ativo FROM tb_iptv WHERE ativo = 1 and expire > date('now') order by grupo ASC, name ASC;"
    if is_full:
        command = 'SELECT url, id, name, logo, grupo, subgrupo, titulo, ativo FROM tb_iptv order by grupo ASC, name ASC;'
    res = cursor.execute(command)
    return res.fetchall()


def create_file(arquivo: str, is_full: bool) -> None:
    head: str = '#EXTM3U\n'
    obj: list = get_sql(is_full=is_full)

    if is_full:
        arquivo = __LISTA_ALL

    if obj is not None:
        if path.exists(arquivo):
            remove(arquivo)

        with open(file=arquivo, mode='w', encoding="utf-8") as file:
            file.write(head)

            for x in obj:
                try:
                    url: str = str(x[0]).strip()
                    tvg: str = str(x[1]).strip()
                    name: str = str(x[2].replace(',', ' ')).strip()
                    logo: str = str(x[3]).strip()
                    grupo: str = str(x[4]).strip()
                    title: str = str(x[6].replace(',', ' ')).strip()
                    ativo: str = str(x[7])

                    if tvg == '0' or len(tvg) <= 3:
                        tvg = ''

                    if logo == '0' or len(logo) <= 3:
                        logo = ''

                    if len(name) > len(title):
                        title = name.replace(',', ' ')

                    linha: str = f'#EXTINF:-1 tvg-id="{tvg}" tvg-name="{name}" tvg-logo="{logo}" group-title="{grupo}",{title}\n{url}\n'

                    if is_full:
                        linha = f'#EXTINF:-1 tvg-id="{tvg}" ativo="{ativo}" tvg-name="{name}" tvg-logo="{logo}" group-title="{grupo}",{title}\n{url}\n'

                    file.write(linha)

                except Exception as err:
                    set_logging_exception(exc=err)

            file.close()


if __name__ == '__main__':
    # m3u: str = f'{__DIR_PATH}/M3UListas/006.m3u'
    # read_file(file_m3u=m3u, action=SQLAction.INSERT_AND_REMOVE, expire='2024-11-01')
    create_file(arquivo=__LISTA_COMPLETA, is_full=False)
