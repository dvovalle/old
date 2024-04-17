# Remove Linha e mais uma linha abaixo
sed -i '/group-title="CHILE/,+1d' /home/danilo/GitHub/iptv/M3UListas/005.m3u


sed -i '/#EXTM3U/d' /home/danilo/GitHub/iptv/M3UListas/001.m3u
sed -i '/##/d' /home/danilo/GitHub/iptv/M3UListas/001.m3u
sed -i '/^[[:space:]]*$/d' /home/danilo/GitHub/iptv/M3UListas/001.m3u

sed -i -e 's/#EXTINF/EXTINF/g' /home/danilo/GitHub/iptv/M3UListas/001.m3u
sed -i -e 's/EXTINF/#EXTINF/g' /home/danilo/GitHub/iptv/M3UListas/001.m3u

https://raw.githubusercontent.com/dvovalle/old/main/M3UListas/listaCompleta.m3u

> http://4tv.site/get.php?username=valterversa0103&password=versavalter0103&type=m3u_plus
> https://raw.githubusercontent.com/SaTecnologiacell/satecnologia.iptv-canais/main/iptvlista.m3u
> https://github.com/SaTecnologiacell/satecnologia.iptv-canais/blob/main/iptvlista.m3u
> https://apkgara.com/lista-iptv/
> https://tecnohive.com/pt/listas-m3u-iptv/
> https://empreendedorismobrasil.com/melhores-lista-iptv-brasil-definitiva-gratis-m3u-atualizada/



## Create Database
```sql

CREATE TABLE tb_iptv (
	url TEXT(2048) NOT NULL,
	id TEXT(2048) NOT NULL,
	name TEXT(2048) NOT NULL,
	logo TEXT(2048) NOT NULL,
	grupo TEXT(2048) NOT NULL,
	subgrupo TEXT(2048) NOT NULL,
	titulo TEXT(2048) NOT NULL,
	tipo TEXT(1024) NOT NULL,
	ativo INTEGER DEFAULT (1) NOT NULL,
	CONSTRAINT pk_tb_iptv PRIMARY KEY (name),
	CONSTRAINT ix_tb_iptv_titulo UNIQUE (titulo)
);

```

https://siptv.app/mylist/
https://raw.githubusercontent.com/dvovalle/old/main/M3UListas/listaCompleta.m3u


http://4tv.site/get.php?username=Valzezinho10&password=Pikadilha226789&type=m3u_plus