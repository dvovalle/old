# Remove Linha e mais uma linha abaixo
sed -i '/group-title="CHILE/,+1d' /home/danilo/GitHub/iptv/M3UListas/005.m3u


sed -i '/#EXTM3U/d' /home/danilo/GitHub/iptv/M3UListas/001.m3u
sed -i '/##/d' /home/danilo/GitHub/iptv/M3UListas/001.m3u
sed -i '/^[[:space:]]*$/d' /home/danilo/GitHub/iptv/M3UListas/001.m3u

sed -i -e 's/#EXTINF/EXTINF/g' /home/danilo/GitHub/iptv/M3UListas/001.m3u
sed -i -e 's/EXTINF/#EXTINF/g' /home/danilo/GitHub/iptv/M3UListas/001.m3u


> http://4tv.site/get.php?username=valterversa0103&password=versavalter0103&type=m3u_plus
> https://raw.githubusercontent.com/SaTecnologiacell/satecnologia.iptv-canais/main/iptvlista.m3u
> https://apkgara.com/lista-iptv/
> https://tecnohive.com/pt/listas-m3u-iptv/
> https://empreendedorismobrasil.com/melhores-lista-iptv-brasil-definitiva-gratis-m3u-atualizada/

alessandra5380

http://4tv.site/get.php?username=alessandra5380&password=6172992108276&type=m3u_plus

https://raw.githubusercontent.com/dvovalle/old/main/M3UListas/listaCompleta.m3u
               https://github.com/dvovalle/old/blob/main/M3UListas/listaCompleta.m3u



https://raw.githubusercontent.com/SaTecnologiacell/satecnologia.iptv-canais/main/iptvlista.m3u
              https://github.com/SaTecnologiacell/satecnologia.iptv-canais/blob/main/iptvlista.m3u


```sql

CREATE TABLE tb_iptv (
	idlinha INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	origem TEXT(128) NOT NULL,
	url TEXT(2048) NOT NULL,
	id TEXT(512) NOT NULL,
	name TEXT(1024) NOT NULL,
	logo TEXT(1024) NOT NULL,
	grupo TEXT(1024) NOT NULL,
	subgrupo TEXT(1024) NOT NULL,
	titulo TEXT(1024) NOT NULL,
	ativo INTEGER DEFAULT (1) NOT NULL,
	online INTEGER DEFAULT (1) NOT NULL,
	CONSTRAINT ix_tb_iptv_name UNIQUE (name)
);

```