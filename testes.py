import socket
import re

__HOST: str = '192.168.1.201'
__PORT: int = 51236


def get_val(data: bytes) -> dict:
    result: dict = dict(
        {'Exists': False, 'Tipo': 'Caixa', 'Key': 'X', 'Value': []})
    texto: str = '...'
    if data is not None:
        texto = str(data.decode('utf-8'))

    txt: str = str(re.sub(r'[^a-zA-Z0-9;]', r'', texto)).strip().upper()

    if len(txt) > 5:
        val: list[str] = []
        if ';' in txt:
            val = txt.split(";")
        else:
            val.append(txt)

        result['Exists'] = True

        if 'CX0039' in txt:
            result['Tipo'] = 'Caixa'
            result['Key'] = str(next(x for x in val if 'CX0039' in x))
            result['Value'] = [x for x in val if 'CX0039' not in x]
        elif 'D39' in txt:
            result['Tipo'] = 'Etiqueta'
            result['Key'] = str(next(x for x in val if 'D39' in x))
            result['Value'] = [x for x in val if 'D39' not in x]
        else:
            result['Tipo'] = 'Outros'
            result['Key'] = 'Outros'
            result['Value'] = [x for x in val]

    return result


def __sql_save(pack: dict) -> None:
    pass


def start() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((__HOST, __PORT))
        s.settimeout(0.5)
        for contador in range(1, 5000):
            try:
                data: bytes = s.recv(255)
                dict_result: dict = get_val(data=data)
                if (dict_result is not None) and (dict_result['Exists']):
                    __sql_save(pack=dict_result)

            except Exception as err:
                msg = f'Error: {err}'


if __name__ == '__main__':
    # start()
    val = get_val(data=b'CX003900779BR;476120;123456')
