# Listas

- <https://raw.githubusercontent.com/dvovalle/old/main/M3UListas/listaCompleta.m3u>
- <https://siptv.app/mylist/>

## Inst

```bash

# mypy: disable-error-code="import-untyped, assignment"

python -m venv venv
pip install --upgrade pip
pip install -r requirements.txt
pip install wheel mypy pylint pyflakes flake8 bandit pycodestyle pre-commit
pre-commit install
npm i -g gitmoji-cli
gitmoji -i
npm install -g git-changelog
git config --global user.name "Seu Nome"
git config --global user.email "sem email ka@kalunga.com.br"
git config --bool flake8.strict true
git config --bool mypy.strict true
pre-commit autoupdate
pre-commit run --all-files
npm install
gulp

```

## Create Database

```sql

https://raw.githubusercontent.com/dvovalle/old/main/M3UListas/listaCompleta.m3u


# database.db

CREATE TABLE tb_iptv (
 codid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 url TEXT(500) NOT NULL,
 id TEXT(128) NOT NULL,
 name TEXT(128) NOT NULL,
 logo TEXT(500) NOT NULL,
 grupo TEXT(128) NOT NULL,
 titulo TEXT(128) NOT NULL,
 ativo INTEGER NOT NULL,
 expire datetime NOT NULL,
 dtanalise datetime NOT NULL,
 CONSTRAINT ix_tb_iptv_url UNIQUE (url)
);


SELECT  name, grupo, ativo
FROM tb_iptv
where name like '%Superman e Lois%'
order by name;

SELECT grupo, '"' || grupo || '",' AS ListGrupo, count(name) AS QtdLinhas
FROM tb_iptv
where ativo = 1
group by grupo
order by grupo ASC;

UPDATE tb_iptv SET grupo = TRIM(UPPER(grupo)), name = TRIM(name), titulo = TRIM(titulo), dtanalise = '1910-01-01';

UPDATE tb_iptv SET  ativo = 1, grupo = 'SERIES | SUPERMAN E LOIS'
where name like '%Superman e Lois%'

```
