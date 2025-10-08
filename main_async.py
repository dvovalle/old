# mypy: disable-error-code="import-untyped"
import multiprocessing
import asyncio
import aiosqlite
import aiofiles
import aiohttp
import re
import unicodedata
from enum import Enum
from os import listdir, path, remove
from datetime import datetime
from typing import List, Dict, Any, Optional
import subprocess

__HEADERS: dict[str, str] = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}
__MY_CPU_COUNT: int = int(multiprocessing.cpu_count() * 2)

__DIR_PATH = path.dirname(path.realpath(__file__))
__LISTA_COMPLETA: str = f"{__DIR_PATH}/M3UListas/listaCompleta.m3u"
__LISTA_ALL: str = f"{__DIR_PATH}/M3UListas/listaFULL.m3u"


class SQLAction(Enum):
    INSERT = 1
    UPDATE = 2
    INSERT_AND_REMOVE = 3
    UPDATE_AND_REMOVE = 4
    UPDATE_AND_REMOVE_CHECK = 5


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
    m = re.search('tvg-name="(.*?)"', line)
    name = m.group(1) if (m is not None) else ''

    m = re.search('tvg-id="(.*?)"', line)
    tvg_id = m.group(1) if (m is not None) else ''

    m = re.search('tvg-logo="(.*?)"', line)
    logo = m.group(1) if (m is not None) else ''

    m = re.search('group-title="(.*?)"', line)
    group = m.group(1) if (m is not None) else ''

    m = re.search('pltv-subgroup="(.*?)"', line)
    sub_group = m.group(1) if (m is not None) else ''

    m = re.search('ativo="(.*?)"', line)
    ativo = m.group(1) if (m is not None) else ''

    m = re.search('[,](?!.*[,])(.*?)$', line)
    title = m.group(1) if (m is not None) else ''

    return dict(
        {
            'title': str(title),
            'tvg-name': str(name),
            'tvg-id': str(tvg_id),
            'tvg-logo': str(logo),
            'tvg-group': str(group),
            'ativo': str(ativo),
            'pltv-subgroup': str(sub_group),
        },
    )


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
    val_unicode = unicodedata.normalize('NFD', txt_value).encode('ascii', 'ignore')
    txt_value = val_unicode.decode('utf-8')
    result: str = re.sub(' +', ' ', txt_value)

    if force:
        result = str(re.sub(r'[^a-zA-Z0-9 ]', r'', txt_value)).strip()

    result = result.replace('  ', ' ')
    return result.strip()


async def update_values(db: aiosqlite.Connection, expire: str, name: str, logo: str, title: str, id_iptv: str, url: str) -> None:
    try:
        async with db.execute(
            'UPDATE tb_iptv SET url=?, id=?, logo=?, titulo=?, expire=?, ativo=? WHERE name=?;',
            (url, id_iptv, logo, title, expire, '0', name),
        ) as cursor:
            await db.commit()
    except Exception as err:
        print(f"Error update_values: {err}")


async def read_file(db: aiosqlite.Connection, file_m3u: str, action: SQLAction, expire: str, origem: str) -> None:
    count: int = 0
    name: str = ''
    logo: str = ''
    group: str = ''
    sub_group: str = ''
    title: str = ''
    id_iptv: str = ''
    ativo: str = ''
    is_completo: bool = False
    url_ok: bool = False

    async with aiofiles.open(file=file_m3u, encoding='utf-8') as file:
        async for line in file:
            try:
                count += 1
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

                    if origem is not None and len(origem) > 0:
                        name = __remove_char(texto=f"{name} {origem}", force=True)
                        title = __remove_char(texto=f"{title} {origem}", force=True)

                    name = __remove_char(texto=name, force=True)
                    title = __remove_char(texto=title, force=True)
                    group = __remove_char(texto=group, force=False)

                    if is_completo and line.find('http') == 0:
                        is_completo = False
                        url = line.strip()

                        url_ok = True
                        if action == SQLAction.UPDATE_AND_REMOVE_CHECK:
                            result = await __consulta_status(url=url)
                            if result:
                                url_ok = True
                            else:
                                url_ok = False

                        if url_ok:
                            try:
                                ativo = '0'
                                async with db.execute(
                                    'INSERT INTO tb_iptv (url, id, name, logo, grupo, titulo, ativo, expire, dtanalise) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);',
                                    (
                                        url,
                                        id_iptv,
                                        name,
                                        logo,
                                        group,
                                        title,
                                        ativo,
                                        expire,
                                        '1990-01-01'
                                    ),
                                ) as cursor:
                                    await db.commit()

                            except Exception:
                                is_completo = False
                                if action == SQLAction.UPDATE or action == SQLAction.UPDATE_AND_REMOVE:
                                    await update_values(db=db, expire=expire, name=name, logo=logo, title=title, id_iptv=id_iptv, url=url)

            except Exception as err:
                print(f"Erro analise: {err}")
                is_completo = False

        if action == SQLAction.INSERT_AND_REMOVE or action == SQLAction.UPDATE_AND_REMOVE:
            if path.exists(file_m3u):
                remove(file_m3u)


async def get_sql(db: aiosqlite.Connection, is_full: bool, grupo: str) -> list:
    command: str = "SELECT url, id, name, logo, grupo, titulo, ativo, codid FROM tb_iptv WHERE ativo = 1 and expire > date('now') order by grupo ASC, name ASC;"

    if len(grupo) > 5:
        command = f"SELECT url, id, name, logo, grupo, titulo, ativo, codid FROM tb_iptv WHERE grupo = '{grupo}' and ativo = 1 and expire > date('now') order by grupo ASC, name ASC;"

    if is_full:
        command = 'SELECT url, id, name, logo, grupo, titulo, ativo, codid FROM tb_iptv order by grupo ASC, name ASC;'

    async with db.execute(command) as cursor:
        return await cursor.fetchall()


async def create_file(db: aiosqlite.Connection, arquivo: str, is_full: bool) -> None:
    head: str = '#EXTM3U\n'
    obj: list = await get_sql(db=db, is_full=is_full, grupo='*')

    if is_full:
        arquivo = __LISTA_ALL

    if obj is not None:
        if path.exists(arquivo):
            remove(arquivo)

        async with aiofiles.open(file=arquivo, mode='w', encoding='utf-8') as file:
            await file.write(head)

            for x in obj:
                try:
                    url: str = str(x[0]).strip()
                    tvg: str = str(x[1]).strip()
                    name: str = str(x[2].replace(',', ' ')).strip()
                    logo: str = str(x[3]).strip()
                    grupo: str = str(x[4]).strip()
                    title: str = str(x[5].replace(',', ' ')).strip()
                    ativo: str = str(x[6])

                    if tvg == '0' or len(tvg) <= 3:
                        tvg = ''

                    if logo == '0' or len(logo) <= 3:
                        logo = ''

                    if len(name) > len(title):
                        title = name.replace(',', ' ')

                    linha: str = f'#EXTINF:-1 tvg-id="{tvg}" tvg-name="{name}" tvg-logo="{logo}" group-title="{grupo}",{title}\n{url}\n'

                    if is_full:
                        linha = f'#EXTINF:-1 tvg-id="{tvg}" ativo="{ativo}" tvg-name="{name}" tvg-logo="{logo}" group-title="{grupo}",{title}\n{url}\n'

                    await file.write(linha)

                except Exception as err:
                    print(f"Erro analise: {err}")


def contem(texto, busca):
    return busca.lower() in texto.lower()


async def verificar_stream(url: str) -> bool:
    result: bool = False
    try:
        comando: list[str] = ['ffmpeg', '-i', url, '-t', '2', '-f', 'null', '-']
        process = await asyncio.create_subprocess_exec(
            *comando,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=5)
            result = process.returncode == 0
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            result = True  # Timeout é considerado como possível conexão

    except Exception as err:
        msgerror: str = f"Erro: {err}"
        if contem(msgerror, 'timed'):
            result = True
        else:
            print(f"verificar_stream: {url} {msgerror}")
            result = False

    return result


async def __consulta_status(url: str, verify: bool = True, session: Optional[aiohttp.ClientSession] = None) -> bool:
    result: bool = False
    msgerror: str = 'OK'
    
    close_session = False
    if session is None:
        session = aiohttp.ClientSession(headers=__HEADERS)
        close_session = True

    try:
        async with session.head(url=url, timeout=aiohttp.ClientTimeout(total=5)) as response:
            if response is not None and int(response.status) == 200:
                result = True
            else:
                result = False
                verify = False
                print(url)

            if result and verify:
                result = await verificar_stream(url=url)

            if not response:
                print(f"URl invalida: {url}")

    except aiohttp.ClientError as ex:
        msgerror = f"Erro: {ex}"
        if contem(msgerror, 'ConnectTimeout'):
            result = True
        else:
            print(f"Consulta: {url} {msgerror}")
            result = False

    except Exception as err:
        msgerror = f"Erro: {err}"
        if contem(msgerror, 'ConnectTimeout'):
            result = True
        else:
            print(f"Consulta: {url} {msgerror}")
            result = False
    finally:
        if close_session and session:
            await session.close()

    return result


async def __analise_all(item: tuple, db: aiosqlite.Connection) -> bool:
    result: bool = False
    try:
        data_atual: datetime = datetime.now()
        data_formatada: str = data_atual.strftime('%Y-%m-%d')
        url: str = str(item[0]).strip()
        codid: str = str(item[1])
        rs_grupo: str = str(item[2])
        
        async with aiohttp.ClientSession(headers=__HEADERS) as session:
            result = await __consulta_status(url=url, verify=False, session=session)
            
            if result:
                msg = f"ID {codid} - {rs_grupo} - OK!!!!"
                await db.execute('UPDATE tb_iptv SET dtanalise=? WHERE codid=?;', (data_formatada, codid))
            else:
                msg = f"ID {codid} - {rs_grupo} - erro"
                await db.execute('UPDATE tb_iptv SET ativo=?, name=?, dtanalise=? WHERE codid=?;', ('0', 'Erro para exibir', data_formatada, codid))
            
            await db.commit()
            print(msg)

    except Exception as err:
        print(f"Erro analise: {err}")

    return result


async def __start_analise(db: aiosqlite.Connection, verify: bool = True) -> None:

    try:
        command = "SELECT url, codid, grupo FROM tb_iptv WHERE ativo = 1 and dtanalise <= '2025-10-07' order by codid ASC;"
        
        async with db.execute(command) as cursor:
            obj = await cursor.fetchall()

        if obj is not None and len(obj) > 0:
            # Processamento assíncrono com semáforo para limitar concorrência
            semaphore = asyncio.Semaphore(__MY_CPU_COUNT)
            
            async def process_with_semaphore(item):
                async with semaphore:
                    return await __analise_all(item, db)
            
            tasks = [process_with_semaphore(item) for item in obj]
            await asyncio.gather(*tasks, return_exceptions=True)

    except Exception as err:
        print(f"Erro em __start_analise: {err}")


async def __read_all_files(db: aiosqlite.Connection, sqlAction: SQLAction) -> None:
    dir_local: str = f"{__DIR_PATH}/M3UListas/"
    files: list[str] = listdir(dir_local)
    files.sort()
    
    if files is not None and len(files) > 0:
        # Processar arquivos em paralelo com limitação
        semaphore = asyncio.Semaphore(5)  # Limitar a 5 arquivos simultâneos
        
        async def process_file(file_name: str):
            async with semaphore:
                m3u: str = f"{dir_local}{file_name}"
                print(f"Lendo: {file_name}")
                await read_file(db=db, file_m3u=m3u, action=sqlAction, expire='2026-12-12', origem='')
        
        tasks = [process_file(file_name) for file_name in files]
        await asyncio.gather(*tasks, return_exceptions=True)


async def __valida_grupos(db: aiosqlite.Connection) -> None:
    command: str = 'SELECT grupo, count(name) AS QtdLinhas FROM tb_iptv where ativo = 1 group by grupo order by grupo ASC;'
    
    async with db.execute(command) as cursor:
        grupos: list = await cursor.fetchall()
    
    if grupos is not None and len(grupos) > 0:
        grupos.sort()
        print('Defina Sim(s) Não(n) ou Rename(r) grupo')
        for x in grupos:
            grupo_name: str = str(x[0])
            value: str = input(f"{x} - s/n or r: ").upper()
            is_commit: bool = False
            
            if value == 'N':
                is_commit = True
                await db.execute('UPDATE tb_iptv SET ativo=? where grupo=?;', ('0', grupo_name))
            if value == 'R':
                is_commit = True
                new_group: str = input(f"Informe o novo grupo -> {grupo_name}: ").strip()
                if new_group is None or (new_group is not None and len(new_group) <= 1):
                    new_group = grupo_name
                await db.execute('UPDATE tb_iptv SET ativo=1, grupo=? where grupo=?;', (new_group, grupo_name))

            if is_commit:
                await db.commit()


async def main() -> None:
    try:
        async with aiosqlite.connect(database='database.db', timeout=2.0) as db:
            # await __read_all_files(db=db, sqlAction=SQLAction.INSERT_AND_REMOVE)
            await __start_analise(db=db, verify=False)
            # await __valida_grupos(db=db)
            # await create_file(db=db, arquivo=__LISTA_COMPLETA, is_full=False)

    except Exception as err:
        print(f"******** -> Erro: {err}")


if __name__ == '__main__':
    asyncio.run(main())