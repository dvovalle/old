import os
import sqlite3
import re

conn = sqlite3.connect(database="database.db", timeout=2.0)
cursor = conn.cursor()

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__LISTA_COMPLETA: str = f'{__DIR_PATH}/M3UListas/listaCompleta.m3u'
__LISTA_ALL: str = f'{__DIR_PATH}/M3UListas/listaFULL.m3u'


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
    id = m.group(1) if (m is not None) else ''

    m = re.search("tvg-logo=\"(.*?)\"", line)
    logo = m.group(1) if (m is not None) else ''

    m = re.search("group-title=\"(.*?)\"", line)
    group = m.group(1) if (m is not None) else ''

    m = re.search("pltv-subgroup=\"(.*?)\"", line)
    sub_group = m.group(1) if (m is not None) else ''

    m = re.search("[,](?!.*[,])(.*?)$", line)
    title = m.group(1) if (m is not None) else ''

    return dict({"title": title,
                 "tvg-name": name,
                 "tvg-id": id,
                 "tvg-logo": logo,
                 "tvg-group": group,
                 "pltv-subgroup": sub_group})


def _exists_db(cmd: str) -> bool:
    res = cursor.execute(cmd)
    res_value = res.fetchone()
    return True


def read_file(file_m3u: str, update: bool) -> None:
    count: int = 0
    linha: str = ''
    url: str = ''
    name: str = ''
    origem: str = ''
    logo: str = ''
    group: str = ''
    sub_group: str = ''
    title: str = ''
    id: str = ''
    num_lines: int = 0
    is_completo: bool = False

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
                        id = str(dict_value['tvg-id']).strip()

                        if len(logo) < 4:
                            logo = '0'

                        if len(group) < 2:
                            group = '0'

                        if len(sub_group) < 2:
                            sub_group = group

                        if len(title) < 2:
                            title = '0'

                        if len(title) < 2:
                            title = name

                        if len(title) > 2:
                            name = title

                        if len(id) < 5:
                            id = '0'

                    if is_completo and line.find('http') == 0:
                        is_completo = False
                        url = line.strip()
                        link: str = url.replace(
                            'http://', '').replace('https://', '')
                        link_pos: int = link.find('.')
                        origem = link[0:link_pos]
                        try:
                            cursor.execute(
                                'INSERT INTO tb_iptv (origem, url, id, name, logo, grupo, subgrupo, titulo, ativo, online) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                                (origem, url, id, name, logo, group, sub_group, title, 1, 1))
                            print(f'INSERT: Title: {
                                  title} - {count} de {num_lines}')
                        except Exception:
                            is_completo = False
                            if update:
                                cursor.execute(
                                    'UPDATE tb_iptv SET origem=?, url=?, id=?, logo=?, titulo=? WHERE name=?;',
                                    (origem, url, id, logo, title, name))
                                print(f'UPDATE: Title: {
                                    title} - {count} de {num_lines}')

            except Exception as err:
                print(f'******** -> Error: {err}')
                is_completo = False

        conn.commit()

        if os.path.exists(file_m3u):
            os.remove(file_m3u)


def get_sql(is_full: bool) -> list:
    command: str = 'SELECT url, id, name, logo, grupo, subgrupo, titulo, idlinha FROM tb_iptv WHERE ativo = 1 and online = 1 order by grupo ASC, name ASC;'
    if is_full:
        command = 'SELECT url, id, name, logo, grupo, subgrupo, titulo, idlinha FROM tb_iptv order by grupo ASC, name ASC;'
    res = cursor.execute(command)
    return res.fetchall()


def create_file(arquivo: str, is_full: bool) -> None:
    head: str = '#EXTM3U x-tvg-url="https://raw.githubusercontent.com/rootcoder/epgtv/main/guide.xml.gz"\n'
    # head: str = '#EXTM3U\n'
    obj: list = get_sql(is_full=is_full)

    if is_full:
        arquivo = __LISTA_ALL

    if obj is not None:
        if os.path.exists(arquivo):
            os.remove(arquivo)

        with open(file=arquivo, mode='w', encoding="utf-8") as file:
            file.write(head)

            for x in obj:
                try:
                    url: str = str(x[0]).strip()
                    id: str = str(x[1]).strip()
                    name: str = str(x[2].replace(',', ' ')).strip()
                    logo: str = str(x[3]).strip()
                    grupo: str = str(x[4]).strip()
                    title: str = str(x[6].replace(',', ' ')).strip()

                    if id == '0' or len(id) <= 3:
                        id = ''

                    if logo == '0' or len(logo) <= 3:
                        logo = ''

                    if len(name) > len(title):
                        title = name.replace(',', ' ')

                    # linha = f'#EXTGRP:{subgroup}\n#EXTINF:-{idlinha} tvg-id="{id}" tvg-name="{name}" tvg-logo="{logo}" group-title="{grupo}",{title}\n{url}\n'
                    # linha: str = f'#EXTINF:-{idlinha} tvg-id="{id}" tvg-name="{name}" tvg-logo="{logo}" group-title="{grupo}",{title}\n{url}\n'

                    file.write(
                        f'#EXTINF:-1 tvg-id="{id}" tvg-name="{name}" tvg-logo="{logo}" group-title="{grupo}",{title}\n{url}\n')

                except Exception as err:
                    print(f'******** -> Erro: {err}')

            file.close()


if __name__ == '__main__':
    # read_file(file_m3u=f'{__DIR_PATH}/M3UListas/001.m3u', update=False)
    create_file(arquivo=__LISTA_COMPLETA, is_full=False)
