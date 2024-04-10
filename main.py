import os
import sqlite3
import re

conn = sqlite3.connect(database="iptv.db", timeout=1.0)
cursor = conn.cursor()


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


def read_file(file_m3u: str) -> None:
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
                        name = dict_value['tvg-name']
                        logo = dict_value['tvg-logo']
                        group = dict_value['tvg-group']
                        sub_group = dict_value['pltv-subgroup']
                        title = dict_value['title']
                        id = dict_value['tvg-id']

                        if len(logo) < 4:
                            logo = '0'

                        if len(group) < 2:
                            group = '0'

                        if len(sub_group) < 2:
                            sub_group = group

                        if len(title) < 2:
                            title = '0'

                        if len(name) < 2:
                            name = title

                        if len(id) < 5:
                            id = '0'

                    if is_completo and line.find('http') >= 0:
                        is_completo = False
                        url = line.strip()
                        link: str = url.replace(
                            'http://', '').replace('https://', '')
                        link_pos: int = link.find('.')
                        origem = link[0:link_pos]
                        cursor.execute(
                            'INSERT INTO tb_iptv (origem, linha, url, id, name, logo, grupo, subgrupo, title, ativo) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                            (origem, linha, url, id, name, logo, group, sub_group, title, 1))
                        print(f'Title: {title} - {count} de {num_lines}')

            except Exception as err:
                print(f'******** -> Error: {err}')
                is_completo = False

        conn.commit()

        if os.path.exists(file_m3u):
            os.remove(file_m3u)


def get_sql(is_full: bool) -> list:
    command: str = 'SELECT url AS [0], id AS [1], name AS [2], logo AS [3], grupo AS [4], subgrupo AS [5], title AS [6] FROM tb_iptv where online = 1 and ativo = 1 order by grupo ASC, name ASC;'
    if is_full:
        command = 'SELECT url AS [0], id AS [1], name AS [2], logo AS [3], grupo AS [4], subgrupo AS [5], title AS [6] FROM tb_iptv order by grupo ASC, name ASC;'
    res = cursor.execute(command)
    return res.fetchall()


def create_file(arquivo: str, is_full: bool) -> None:
    obj: list = get_sql(is_full=is_full)

    if obj is not None:
        try:
            if os.path.exists(arquivo):
                os.remove(arquivo)
        except Exception as err:
            print(f'******** -> Error: {err}')

        head: str = '#EXTM3U x-tvg-url="https://raw.githubusercontent.com/rootcoder/epgtv/main/guide.xml.gz"\n'
        with open(file=arquivo, mode='w', encoding="utf-8") as file:
            file.write(head)

            for x in obj:
                try:
                    url: str = x[0]
                    id: str = x[1]
                    name: str = x[2].replace(',', ' ')
                    logo: str = x[3]
                    grupo: str = x[4]
                    subgroup: str = x[5]
                    title: str = x[6].replace(',', ' ')

                    if id == '0' or len(id) <= 3:
                        id = ''

                    if logo == '0' or len(logo) <= 3:
                        logo = ''

                    if len(name) > len(title):
                        title = name.replace(',', ' ')

                    # grupo_sub: str = f'{grupo} | {name[0:1]}'

                    # linha: str = f'#EXTINF:-1 tvg-id="" tvg-name="{name}" tvg-logo="{logo}" group-title="{subgroup}" pltv-subgroup="{grupo}", {title}\n{url}\n'

                    file.write(
                        f'#EXTINF:-1 tvg-id="{id}" tvg-name="{name}" tvg-logo="{logo}" group-title="{grupo}",{title}\n{url}\n')

                except Exception as err:
                    print(f'******** -> Erro: {err}')

            file.close()


if __name__ == '__main__':
    # read_file('/home/danilo/GitHub/iptv/M3UListas/001.m3u')
    create_file(
        arquivo='/home/danilo/GitHub/iptv/M3UListas/listaCompleta.m3u', is_full=False)
