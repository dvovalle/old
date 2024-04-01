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

    m = re.search("[,](?!.*[,])(.*?)$", line)
    title = m.group(1) if (m is not None) else ''

    return dict({"title": title,
                 "tvg-name": name,
                 "tvg-id": id,
                 "tvg-logo": logo,
                 "tvg-group": group})


def read_file(file_m3u: str) -> None:
    count: int = 0
    linha: str = ''
    url: str = ''
    name: str = ''
    logo: str = ''
    group: str = ''
    title: str = ''
    num_lines: int = 0
    is_completo: bool = False

    with open(file=file_m3u, mode='r', encoding="utf-8") as file:
        num_lines = sum(1 for _ in file)

    with open(file=file_m3u, mode='r', encoding="utf-8") as file:
        while num_lines >= count:
            try:
                count += 1
                print(f'Linha: {count} de {num_lines}')
                line = file.readline()
                if line is not None and len(line) > 0:
                    if line.find('EXTINF:') >= 0:
                        is_completo = True
                        linha = line.strip()
                        dict_value = extract(line=linha)
                        name = dict_value['tvg-name']
                        logo = dict_value['tvg-logo']
                        group = dict_value['tvg-group']
                        title = dict_value['title']

                        if len(logo) < 4:
                            logo = '0'

                        if len(group) < 2:
                            group = '0'

                        if len(title) < 2:
                            title = '0'

                        if len(name) < 2:
                            name = title

                    if is_completo and line.find('http') >= 0:
                        is_completo = False
                        url = line.strip()
                        cursor.execute(
                            'INSERT INTO TB_IPTV_Lista (linha, url, "tvg-name", "tvg-logo", "tvg-group", ativo, title) VALUES(?, ?, ?, ?, ?, ?, ?);', (linha, url, name, logo, group, 1, title))
                        conn.commit()
                        print(f'Title: {title} inserido..')

                        # UPDATE TB_IPTV_Lista SET  grupo  = TRIM(substring("tvg-group", 0, charindex('|', "tvg-group"))), subgrupo = TRIM(substring("tvg-group", charindex('|', "tvg-group") + 1, 128))

            except Exception as err:
                print(f'Erro: {err}')
                is_completo = False


def get_sql() -> list:
    res = cursor.execute(
        'SELECT TRIM(url) AS [0], TRIM("tvg-name") AS [1], TRIM("tvg-logo") AS [2], TRIM("tvg-group") AS [3], TRIM(title) AS [4], TRIM(grupo) AS [5], TRIM(subgrupo) AS [6] FROM TB_IPTV_Lista WHERE ativo = 1 ORDER BY "tvg-group" ASC, "tvg-name" ASC;')
    return res.fetchall()


def create_file(arquivo: str) -> None:
    obj: list = get_sql()
    if obj is not None:
        if os.path.exists(arquivo):
            os.remove(arquivo)

        head: str = '#EXTM3U x-tvg-url="https://raw.githubusercontent.com/rootcoder/epgtv/main/guide.xml.gz"\n'
        with open(file=arquivo, mode='w', encoding="utf-8") as file:
            file.write(head)

            for x in obj:
                try:
                    url: str = x[0]
                    name: str = x[1].replace(',', ' ')
                    logo: str = x[2]
                    grupo: str = x[3]
                    subgroup: str = x[6]
                    title: str = x[4].replace(',', ' ')

                    if len(name) > len(title):
                        title = name.replace(',', ' ')

                    # grupo_sub: str = f'{grupo} | {name[0:1]}'

                    file.write(
                        f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{logo}" group-title="{grupo}",{title}\n{url}\n')

                except Exception as err:
                    print(f'Erro: {err}')

            file.close()


if __name__ == '__main__':
    # read_file('/home/danilo/GitHub/iptv/M3UListas/tv_channels_valterversa0103_plus.m3u')
    create_file(arquivo='/home/danilo/GitHub/iptv/M3UListas/listaCompleta.m3u')
