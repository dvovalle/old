import multiprocessing
import re
import sqlite3
import subprocess
import unicodedata
from enum import Enum
from multiprocessing import Pool
from os import path, remove, listdir

import requests

__HEADERS: dict[str, str] = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"}
__MY_CPU_COUNT: int = int(multiprocessing.cpu_count() * 2) + 1

conn = sqlite3.connect(database="database.db", timeout=2.0)
cursor = conn.cursor()

__DIR_PATH = path.dirname(path.realpath(__file__))
__LISTA_COMPLETA: str = f"{__DIR_PATH}/M3UListas/listaCompleta.m3u"
__LISTA_ALL: str = f"{__DIR_PATH}/M3UListas/listaFULL.m3u"


class SQLAction(Enum):
    INSERT: int = 1
    UPDATE: int = 2
    INSERT_AND_REMOVE: int = 3
    UPDATE_AND_REMOVE: int = 4
    UPDATE_AND_REMOVE_CHECK: int = 5


def __start_backup() -> None:
    conn_old = sqlite3.connect(database="iptv.db", timeout=2.0)
    cursor_old = conn_old.cursor()
    command: str = "SELECT origem, url, id, name, logo, grupo, subgrupo, title, ativo, online FROM tb_iptv order by grupo ASC, name ASC;"
    res = cursor_old.execute(command)
    listold: list = res.fetchall()
    if listold is not None:
        for x in listold:
            try:
                cursor.execute(
                    "INSERT INTO tb_iptv (origem, url, id, name, logo, grupo, subgrupo, titulo, ativo, online) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    (x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]),
                )
            except Exception as err:
                print(f"******** -> Erro: {err}")

    conn.commit()


def get_el(texto: str, tag_name: str, ate_fim: bool) -> str:
    result: str = "0"
    start: int = texto.find(tag_name)
    if start > 2:
        texto_aux: str = texto.replace(tag_name, "")[start:]
        end: int = texto_aux.find('"')
        if ate_fim:
            result = f'"{texto_aux}'
        else:
            result = texto_aux[:end]

    return result


def extract(line: str) -> dict:
    m = re.search('tvg-name="(.*?)"', line)
    name = m.group(1) if (m is not None) else ""

    m = re.search('tvg-id="(.*?)"', line)
    tvg_id = m.group(1) if (m is not None) else ""

    m = re.search('tvg-logo="(.*?)"', line)
    logo = m.group(1) if (m is not None) else ""

    m = re.search('group-title="(.*?)"', line)
    group = m.group(1) if (m is not None) else ""

    m = re.search('pltv-subgroup="(.*?)"', line)
    sub_group = m.group(1) if (m is not None) else ""

    m = re.search('ativo="(.*?)"', line)
    ativo = m.group(1) if (m is not None) else ""

    m = re.search("[,](?!.*[,])(.*?)$", line)
    title = m.group(1) if (m is not None) else ""

    return dict(
        {
            "title": str(title),
            "tvg-name": str(name),
            "tvg-id": str(tvg_id),
            "tvg-logo": str(logo),
            "tvg-group": str(group),
            "ativo": str(ativo),
            "pltv-subgroup": str(sub_group),
        }
    )


def _exists_db(cmd: str) -> bool:
    res = cursor.execute(cmd)
    # res_value = res.fetchone()
    return res.fetchone()


def __remove_char(texto: str, force: bool) -> str:
    if texto is None:
        texto = ""

    txt_value: str = str(texto.replace("(", "")).strip()
    txt_value = txt_value.replace(")", "")
    txt_value = txt_value.replace("[", "")
    txt_value = txt_value.replace("]", "")
    txt_value = txt_value.replace("º", "")
    txt_value = txt_value.replace("ª", "")
    txt_value = txt_value.replace("{", "")
    txt_value = txt_value.replace("}", "")
    txt_value = txt_value.replace("/", "")
    txt_value = txt_value.replace("\\", "")
    txt_value = txt_value.replace("-", "")
    txt_value = txt_value.replace("#", "")
    txt_value = txt_value.replace("!", "")
    txt_value = txt_value.replace(",", "")
    txt_value = txt_value.replace(".", "")
    txt_value = txt_value.replace("_", "")
    txt_value = txt_value.replace("@", "")
    txt_value = txt_value.replace("&", "")
    txt_value = txt_value.replace("*", "")
    txt_value = txt_value.replace("+", "")
    txt_value = txt_value.replace("$", "")
    txt_value = txt_value.replace("%", "")
    txt_value = txt_value.replace("ç", "c")
    txt_value = txt_value.replace("Ç", "C")
    txt_value = txt_value.replace("?", "")
    txt_value = txt_value.replace("Á", "A")
    txt_value = txt_value.replace("á", "a")
    txt_value = txt_value.replace("Ã", "A")
    txt_value = txt_value.replace("Â", "A")
    txt_value = txt_value.replace("À", "A")
    txt_value = txt_value.replace("ã", "a")
    txt_value = txt_value.replace("É", "E")
    txt_value = txt_value.replace("é", "e")
    txt_value = txt_value.replace("  ", " ")
    val_unicode = unicodedata.normalize("NFD", txt_value).encode("ascii", "ignore")
    txt_value = val_unicode.decode("utf-8")
    result: str = re.sub(" +", " ", txt_value)

    if force:
        result = str(re.sub(r"[^a-zA-Z0-9 ]", r"", txt_value)).strip()

    result = result.replace("  ", " ")
    return result.strip()


def update_values(expire: str, name: str, logo: str, title: str, id_iptv: str, url: str) -> None:
    try:
        cursor.execute("UPDATE tb_iptv SET url=?, id=?, logo=?, titulo=?, expire=?, ativo=? WHERE name=?;", (url, id_iptv, logo, title, expire, "0", name))

    except Exception as err:
        print(f"Error update_values: {err}")


def read_file(file_m3u: str, action: SQLAction, expire: str, origem: str) -> None:
    count: int = 0
    name: str = ""
    logo: str = ""
    group: str = ""
    sub_group: str = ""
    title: str = ""
    id_iptv: str = ""
    ativo: str = ""
    is_completo: bool = False
    url_ok: bool = False
    num_lines: int = 0

    with open(file=file_m3u, mode="r", encoding="utf-8") as file:
        num_lines = sum(1 for _ in file)

    with open(file=file_m3u, mode="r", encoding="utf-8") as file:
        while num_lines >= count:
            try:
                count += 1
                line = file.readline()
                if line is not None and len(line) > 0:
                    if line.find("EXTINF:") >= 0:
                        is_completo = True
                        linha = line.strip()
                        dict_value = extract(line=linha)
                        name = str(dict_value["tvg-name"]).strip()
                        logo = str(dict_value["tvg-logo"]).strip()
                        group = str(dict_value["tvg-group"]).strip()
                        sub_group = str(dict_value["pltv-subgroup"]).strip()
                        title = str(dict_value["title"]).strip()
                        id_iptv = str(dict_value["tvg-id"]).strip()
                        ativo = str(dict_value["ativo"]).strip()

                        if len(ativo) <= 0:
                            ativo = "1"

                        if len(logo) < 4:
                            logo = "0"

                        if len(group) < 2:
                            group = "0"

                        if len(sub_group) < 2:
                            sub_group = group

                        if len(name) < 2:
                            name = "0"

                        if len(title) < 2:
                            title = "0"

                        if len(title) < 2:
                            title = name

                        if len(title) > 2:
                            name = title

                        if len(id_iptv) < 5:
                            id_iptv = "0"

                    if origem is not None and len(origem) > 0:
                        name = __remove_char(texto=f"{name} {origem}", force=True)
                        title = __remove_char(texto=f"{title} {origem}", force=True)

                    name = __remove_char(texto=name, force=True)
                    title = __remove_char(texto=title, force=True)
                    group = __remove_char(texto=group, force=False)

                    if is_completo and line.find("http") == 0:
                        is_completo = False
                        url = line.strip()

                        url_ok = True
                        if action == SQLAction.UPDATE_AND_REMOVE_CHECK:
                            result = __consulta_status(url=url)
                            if result:
                                url_ok = True
                            else:
                                url_ok = False

                        if url_ok:
                            try:
                                ativo = "0"
                                cursor.execute(
                                    "INSERT INTO tb_iptv (url, id, name, logo, grupo, titulo, ativo, expire) VALUES(?, ?, ?, ?, ?, ?, ?, ?);",
                                    (
                                        url,
                                        id_iptv,
                                        name,
                                        logo,
                                        group,
                                        title,
                                        ativo,
                                        expire,
                                    ),
                                )

                            except Exception:
                                is_completo = False
                                if action == SQLAction.UPDATE or action == SQLAction.UPDATE_AND_REMOVE:
                                    update_values(expire=expire, name=name, logo=logo, title=title, id_iptv=id_iptv, url=url)

            except Exception as err:
                print(f"Erro analise: {err}")
                is_completo = False

        conn.commit()

        if action == SQLAction.INSERT_AND_REMOVE or action == SQLAction.UPDATE_AND_REMOVE:
            if path.exists(file_m3u):
                remove(file_m3u)


def get_sql(is_full: bool, grupo: str) -> list:
    command: str = "SELECT url, id, name, logo, grupo, titulo, ativo, codid FROM tb_iptv WHERE ativo = 1 and expire > date('now') order by grupo ASC, name ASC;"

    if len(grupo) > 5:
        command: str = f"SELECT url, id, name, logo, grupo, titulo, ativo, codid FROM tb_iptv WHERE grupo = '{grupo}' and ativo = 1 and expire > date('now') order by grupo ASC, name ASC;"

    if is_full:
        command = "SELECT url, id, name, logo, grupo, titulo, ativo, codid FROM tb_iptv order by grupo ASC, name ASC;"

    res = cursor.execute(command)
    return res.fetchall()


def create_file(arquivo: str, is_full: bool, grupo: str) -> None:
    head: str = "#EXTM3U\n"
    obj: list = get_sql(is_full=is_full, grupo=grupo)

    if len(grupo) > 5:
        arquivo = grupo.replace("|", "")
        arquivo = arquivo.replace("SERIES", "")
        arquivo = arquivo.replace("FILMES", "")
        arquivo = f"{arquivo}.m3u".strip()
        print(arquivo)

    if is_full:
        arquivo = __LISTA_ALL

    if obj is not None:
        if path.exists(arquivo):
            remove(arquivo)

        with open(file=arquivo, mode="w", encoding="utf-8") as file:
            file.write(head)

            for x in obj:
                try:
                    url: str = str(x[0]).strip()
                    tvg: str = str(x[1]).strip()
                    name: str = str(x[2].replace(",", " ")).strip()
                    logo: str = str(x[3]).strip()
                    grupo: str = str(x[4]).strip()
                    title: str = str(x[5].replace(",", " ")).strip()
                    ativo: str = str(x[6])

                    if tvg == "0" or len(tvg) <= 3:
                        tvg = ""

                    if logo == "0" or len(logo) <= 3:
                        logo = ""

                    if len(name) > len(title):
                        title = name.replace(",", " ")

                    linha: str = f'#EXTINF:-1 tvg-id="{tvg}" tvg-name="{name}" tvg-logo="{logo}" group-title="{grupo}",{title}\n{url}\n'

                    if is_full:
                        linha = f'#EXTINF:-1 tvg-id="{tvg}" ativo="{ativo}" tvg-name="{name}" tvg-logo="{logo}" group-title="{grupo}",{title}\n{url}\n'

                    file.write(linha)

                except Exception as err:
                    print(f"Erro analise: {err}")

            file.close()


def contem(texto, busca):
    return busca.lower() in texto.lower()


def verificar_stream(url: str) -> bool:
    result: bool = False
    try:
        comando: list[str] = ["ffmpeg", "-i", url, "-t", "2", "-f", "null", "-"]
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        result = resultado.returncode == 0

    except Exception as err:
        msgerror: str = f"Erro: {err}"
        if contem(msgerror, "timed"):
            result = True
        else:
            print(f"verificar_stream: {url} {msgerror}")
            result = False

    return result


def __consulta_status(url: str, verify: bool = True) -> bool:
    result: bool = False
    msgerror: str = "OK"
    try:
        response = requests.head(url=url, headers=__HEADERS, data={}, timeout=5, verify=True, allow_redirects=True)

        if response is not None and int(response.status_code) == 200:
            result = True
        else:
            result = False
            verify = False
            print(url)

        if result and verify:
            result = verificar_stream(url=url)

        if not response:
            print(f"URl invalida: {url}")

    except requests.RequestException as ex:
        msgerror = f"Erro: {ex}"
        if contem(msgerror, "ConnectTimeout"):
            result = True
        else:
            print(f"Consulta: {url} {msgerror}")
            result = False

    except Exception as err:
        msgerror = f"Erro: {err}"
        if contem(msgerror, "ConnectTimeout"):
            result = True
        else:
            print(f"Consulta: {url} {msgerror}")
            result = False

    return result


def __analise(grupo: str = "*", verify: bool = True) -> bool:
    result: bool = False
    index: int = 0
    msg: str = ""

    try:
        command: str = f"SELECT url, codid, grupo FROM tb_iptv WHERE grupo = '{grupo}' and ativo = 1 order by codid ASC;"
        if grupo == "*":
            command = "SELECT url, codid, grupo FROM tb_iptv WHERE ativo = 1 order by grupo ASC, codid ASC;"

        res = cursor.execute(command)
        obj: list = res.fetchall()

        if obj is not None:
            total: int = len(obj)
            for x in obj:
                index += 1
                msg = f"{index} de {total}"
                try:
                    url: str = str(x[0]).strip()
                    codid: str = str(x[1])
                    rs_grupo: str = str(x[2])
                    result = __consulta_status(url=url, verify=verify)
                    if result:
                        msg = f"{index} de {total} ID {codid} - {rs_grupo} - OK!!!!"
                    else:
                        msg = f"{index} de {total} ID {codid} - {rs_grupo} - erro"
                        cursor.execute("UPDATE tb_iptv SET ativo=? WHERE codid=?;", ("0", codid))
                        conn.commit()
                    print(msg)

                except Exception as err:
                    print(f"Erro analise: {err}")

    except Exception as err:
        print(f"Erro analise: {err}")

    return result


def __start_analise(verify: bool = True) -> None:
    list_gr: list[str] = ["FILMES | CAPITAO AMERICA"]

    if list_gr is not None and len(list_gr) > 0:
        if len(list_gr) > 1:
            cpu_count: int = min(__MY_CPU_COUNT, len(list_gr))
            with Pool(processes=cpu_count) as p:
                p.map(__analise, list_gr)
        else:
            for grupo in list_gr:
                __analise(grupo=grupo, verify=verify)
    else:
        __analise(grupo="*", verify=verify)


def __read_all_files(sqlAction: SQLAction) -> None:
    dir_local: str = f"{__DIR_PATH}/M3UListas/"
    files: list[str] = listdir(dir_local)
    files.sort()
    if files is not None and len(files) > 0:
        for x in files:
            m3u: str = f"{dir_local}{x}"
            print(f"Lendo: {x}")
            read_file(file_m3u=m3u, action=sqlAction, expire="2025-12-12", origem="")


def __valida_grupos() -> None:
    command: str = "SELECT grupo, count(name) AS QtdLinhas FROM tb_iptv where ativo = 1 group by grupo order by grupo ASC;"
    res = cursor.execute(command)
    grupos: list = res.fetchall()
    grupos.sort()
    if grupos is not None and len(grupos) > 0:
        grupos.sort()
        print("Defina Sim(s) Não(n) ou Rename(r) grupo")
        for x in grupos:
            grupo_name: str = str(x[0])
            value: str = input(f"{x} - s/n or r: ").upper()
            is_commit: bool = False
            if value == "N":
                is_commit = True
                cursor.execute("UPDATE tb_iptv SET ativo=? where grupo=?;", ("0", grupo_name))
            if value == "R":
                is_commit = True
                new_group: str = input(f"Informe o novo grupo -> {grupo_name}: ").strip()
                if new_group is None or (new_group is not None and len(new_group) <= 1):
                    new_group = grupo_name
                cursor.execute("UPDATE tb_iptv SET ativo=1, grupo=? where grupo=?;", (new_group, grupo_name))

            if is_commit:
                conn.commit()


if __name__ == "__main__":
    try:
        __read_all_files(sqlAction=SQLAction.INSERT_AND_REMOVE)
        # __start_analise(verify=True)
        # __valida_grupos()
        # create_file(arquivo=__LISTA_COMPLETA, is_full=False, grupo="*")

    except Exception as err:
        print(f"******** -> Erro: {err}")
