# Remove Linha e mais uma linha abaixo
sed -i '/group-title="CHILE/,+1d' M3UListas/005.m3u


sed -i '' '/#EXTM3U/d' M3UListas/001.m3u
sed -i '' '/##/d' M3UListas/001.m3u
sed -i '' '/^[[:space:]]*$/d' M3UListas/001.m3u

sed -i -e 's/#EXTINF/EXTINF/g' M3UListas/001.m3u
sed -i -e 's/EXTINF/#EXTINF/g' M3UListas/001.m3u

https://raw.githubusercontent.com/dvovalle/old/main/M3UListas/listaCompleta.m3u

> http://4tv.site/get.php?username=valterversa0103&password=versavalter0103&type=m3u_plus
> http://4tv.site/get.php?username=02gilson01&password=02as012023&type=m3u_plus
> https://apkgara.com/lista-iptv/
> https://tecnohive.com/pt/listas-m3u-iptv/
> https://empreendedorismobrasil.com/melhores-lista-iptv-brasil-definitiva-gratis-m3u-atualizada/


▄▄︻デ𝗠𝟯𝗨⚡𝐋𝐢𝐧𝐤1═一※ http://4tv.site/get.php?username=75529172&password=548272982&type=m3u_plus&output=m3u8
▄▄︻デ𝗠𝟯𝗨⚡𝐋𝐢𝐧𝐤2═一※ http://4tv.site/get.php?username=75529172&password=548272982&type=m3u_plus
▄▄︻デ𝗠𝟯𝗨⚡𝐋𝐢𝐧𝐤1═一※ http://4tv.site/get.php?username=PAmeLLaa888&password=MESwuitaa222&type=m3u_plus&output=m3u8
▄▄︻デ𝗠𝟯𝗨⚡𝐋𝐢𝐧𝐤2═一※ http://4tv.site/get.php?username=PAmeLLaa888&password=MESwuitaa222&type=m3u_plus


> curl -o 001.m3u "https://raw.githubusercontent.com/SaTecnologiacell/satecnologia.iptv-canais/main/iptvlista.m3u"
> curl -o 002.m3u "https://gist.githubusercontent.com/raphacmartin/eb975dfa240ff36ec42a0557aff91485/raw/a0f65e2753841daa665e71e74829b277a7d393f2/iptv.m3u"
> curl -o 003.m3u "https://gist.githubusercontent.com/fabiomagno/82e617e8e8c0d9bb60b605aad0bb107d/raw/95e7660ffb8e4eac2ff0109a949bd1449570556c/lista%2520oficial.m3u"
> curl -o 004.m3u "https://gist.githubusercontent.com/dranimboy/bc3c6162e5afe1083d13354c25e95827/raw/b8a980cbb09c9d9bfee005b8be4c2cacf45c5fd3/LISTA%2520GRANDE.m3u"



## Create Database


```sql

# database.db

CREATE TABLE tb_iptv (
	url TEXT(2048) NOT NULL,
	id TEXT(2048) NOT NULL,
	name TEXT(2048) NOT NULL,
	logo TEXT(2048) NOT NULL,
	grupo TEXT(2048) NOT NULL,
	subgrupo TEXT(2048) NOT NULL,
	titulo TEXT(2048) NOT NULL,
	tipo TEXT(128) NOT NULL,
	ativo INTEGER NOT NULL,
	CONSTRAINT pk_tb_iptv PRIMARY KEY (name),
	CONSTRAINT ix_tb_iptv_titulo UNIQUE (titulo)
);




SELECT  name, grupo, ativo
FROM tb_iptv
where grupo = 'X'
order by name;


SELECT DISTINCT grupo
FROM tb_iptv
where ativo = 1
order by grupo ASC;



UPDATE tb_iptv SET  ativo = 0
WHERE grupo = 'XXXXXXXX'


```

https://siptv.app/mylist/
https://raw.githubusercontent.com/dvovalle/old/main/M3UListas/listaCompleta.m3u


http://4tv.site/get.php?username=373973275&password=038894280&type=m3u_plus


## EXT Tags
| EXT | Meaning |
| --- | ------- |
| #EXTM3U | Indicates that the file is an M3U playlist file |
| #EXTINF | Specifies the duration and title of a media file in the playlist |
| #EXT-X-VERSION | Indicates the version of the HLS protocol used in the playlist |
| #EXT-X-TARGETDURATION | Specifies the maximum duration of any media file in the playlist |
| #EXT-X-MEDIA-SEQUENCE | Specifies the sequence number of the first media file in the playlist |
| #EXT-X-PLAYLIST-TYPE | Indicates the type of playlist, such as "VOD" (video on demand) or "EVENT" |
| #EXT-X-ALLOW-CACHE | Indicates whether the client is allowed to cache the media files |
| #EXT-X-STREAM-INF | Specifies the URI of a variant stream playlist and its properties |
| #EXT-X-MEDIA | Specifies the URI of a media file and its properties |
| #EXT-X-KEY | Specifies encryption information for media files in the playlist |
| #EXT-X-BYTERANGE | Specifies the byte range of a media file in the playlist |
| #EXT-X-DISCONTINUITY | Indicates a discontinuity between two media segments |
| #EXT-X-DISCONTINUITY-SEQUENCE | Specifies the sequence number of the next media file after a discontinuity |
| #EXT-X-PROGRAM-DATE-TIME | Specifies the date and time of the first sample in a media file |
| #EXT-X-INDEPENDENT-SEGMENTS | Indicates whether each media file is a standalone segment or part of a larger media file |
| #EXT-X-ENDLIST | Indicates the end of the playlist |
| #EXT-X-MAP | Specifies the media initialization section for a media file |
| #EXT-X-START | Specifies the time offset and precise start time for a live event |
| #EXT-X-RENDITION-REPORT | Specifies the availability and properties of alternate renditions of a media file |
| #EXT-X-MEDIA-SEQUENCE-DISCONTINUITY | Indicates a discontinuity in the media sequence number |
| #EXT-X-DATERANGE | Specifies a range of dates for a media file or playlist |
| #EXT-X-TARGETDURATION-REACHED | Indicates that the maximum duration of a media file has been reached |
| #EXT-X-SERVER-CONTROL | Specifies server-side control parameters for the playlist |
| #EXT-X-VERSIONING | Specifies versioning information for the playlist |
| #EXT-X-I-FRAMES-ONLY | Indicates that the playlist contains only I-frame media files |
| #EXT-X-INDEPENDENT-SEGMENTS-DISCONTINUITY | Indicates a discontinuity in the independent segments |
| #EXT-X-SESSION-DATA | Specifies arbitrary data associated with the playlist |
| #EXT-X-SESSION-KEY | Specifies encryption information for the entire session |
| #EXT-X-PRELOAD-HINT | Indicates media files that the client should preload |
| #EXT-X-RENDITION-GROUP-ID | Identifies a group of alternate renditions |
| #EXT-X-RENDITION-LANGUAGE | Specifies the language of an alternate rendition |
| #EXT-X-RENDITION-ASSOCIATED-PROPERTY | Specifies a property associated with an alternate rendition |
| #EXT-X-RENDITION-URI | Specifies the URI of an alternate rendition |
| #EXT-X-CUE-OUT | Indicates the start time of a commercial break |
| #EXT-X-CUE-IN | Indicates the end time of a commercial break |
| #EXT-X-RENDITION-GROUP | Identifies a group of alternate renditions |
| #EXT-X-RENDITION-TO-PROGRAM | Specifies the mapping from a rendition to a program |
| #EXT-X-PROGRAM-DATE-TIME-OFFSET | Specifies the offset of the date and time for a live event |
| #EXT-X-CONTENT-IDENTIFIER | Specifies a unique identifier for a media file or playlist |
| #EXT-X-DATERANGE-ID | Specifies the identifier for a date range |
| #EXT-X-SERVER-CONTROL-COMMAND | Specifies a command to be sent to the server |
| #EXT-X-SERVER-CONTROL-HOLD-BACK | Specifies the amount of time to hold back media files |
| #EXT-X-SERVER-CONTROL-PART-HOLD-BACK | Specifies the amount of time to hold back partial media files |
| #EXT-X-SERVER-CONTROL-MAX-DURATION | Specifies the maximum duration of media files to send |
| #EXT-X-SERVER-CONTROL-MAX-AGE | Specifies the maximum age of cached media files |
| #EXT-X-SERVER-CONTROL-CAN-SKIP-UNTIL | Specifies the earliest time to skip to in a media file |
| #EXT-X-SERVER-CONTROL-CAN-SKIP-DATERANGES | Specifies whether the client can skip date ranges |
| #EXT-X-START-DURATION | Specifies the duration of a live event |
| #EXT-X-CUE-OUT-CONT-DURATION | Specifies the duration of a partial cue-out |
| #EXT-X-PROGRAM-DATE-TIME-SERVER | Specifies the date and time of the server |
| #EXT-X-CONTENT-KEY | Specifies a content key for a media file or playlist |
| #EXT-X-DISCONTINUITY-ITEM | Indicates a discontinuity between two media items |
| #EXT-X-SCTE35 | Specifies an SCTE-35 cue message |
| #EXT-X-CUE-OUT-PTS | Indicates the PTS value of a cue-out |
| #EXT-X-CUE-IN-PTS | Indicates the PTS value of a cue-in |
| #EXT-X-CUE-START-PTS | Indicates the PTS value of a cue-start |
| #EXT-X-CUE-END-PTS | Indicates the PTS value of a cue-end |
| #EXT-X-CUE-OUT-CONT-PTS | Indicates the PTS value of a partial cue-out |
| #EXT-X-MEDIA-RENDITION-REPORT | Specifies the availability and properties of alternate media renditions |
| #EXT-X-RELATIVE-CUE-OUT | Indicates the relative start time of a cue-out |
| #EXT-X-RELATIVE-CUE-IN | Indicates the relative end time of a cue-in |
| #EXT-X-RELATIVE-CUE-OUT-CONT | Indicates the relative start time and duration of a partial cue-out. |
| #EXT-X-MAP-BYTERANGE | Specifies the byte range of a media initialization section |
| #EXT-X-CUE-OUT-DURATION | Specifies the duration of a cue-out |
| #EXT-X-CUE-OUT-CONT-ID | Specifies the identifier of a partial cue-out |
| #EXT-X-CUE-IN-DURATION | Specifies the duration of a cue-in |
| #EXT-X-CUE-START-DURATION | Specifies the duration of a cue-start |
| #EXT-X-CUE-END-DURATION | Specifies the duration of a cue-end |
| #EXT-X-CUE-OUT-CONT-DURATION-MS | Specifies the duration of a partial cue-out in milliseconds |

## TVG Tags
| TVG | Meaning |
| --- | ------- |
| TVG-ID | Specifies the unique identifier of the current media file. This tag is used to identify individual channels in the playlist. |
| TVG-NAME | Specifies the name of the current channel. This tag is used to display the name of the channel in the IPTV player. |
| TVG-LOGO | Specifies the URL of the logo for the current channel. This tag is used to display the logo of the channel in the IPTV player. |
| TVG-COUNTRY | Specifies the country code of the current channel. This tag is used to group channels by country in the playlist. |
| TVG-LANGUAGE | Specifies the language code of the current channel. This tag is used to group channels by language in the playlist. |
| TVG-TYPE | Specifies the type of the current channel. This tag is used to group channels by type (e.g. news, sports, entertainment) in the playlist. |
| TVG-URL | Specifies the URL of the website for the current channel. This tag is used to provide additional information about the channel. |
| TVG-GROUP | Specifies the name of the group that the current channel belongs to. This tag is used to group channels in the playlist. |
| TVG-EPGID | Specifies the unique identifier of the electronic program guide (EPG) for the current channel. This tag is used to associate the channel with its program guide. |
| TVG-EPGURL | Specifies the URL of the electronic program guide (EPG) for the current channel. This tag is used to provide the location of the channel's program guide. |
| TVG-EPGSHIFT | Specifies the time shift (in hours) of the electronic program guide (EPG) for the current channel. This tag is used to adjust the program guide for time zone differences. |
| TVG-RADIO | Specifies whether the current channel is a radio channel. This tag is used to differentiate between TV and radio channels in the playlist. |
| TVG-TIMESHIFT | Specifies the time shift (in hours) of the current channel. This tag is used to adjust the channel's start time for time zone differences. |
| TVG-ARCHIVE | Specifies whether the current channel has an archive. This tag is used to indicate whether the channel offers archived content. |
| TVG-TVGPLAYLIST | Specifies the URL of the TVG playlist for the current channel. This tag is used to provide additional playlist information. |
| TVG-ASPECT-RATIO | Specifies the aspect ratio of the current channel. This tag is used to set the aspect ratio for the channel. |
| TVG-AUDIO-TRACK | Specifies the audio track for the current channel. This tag is used to set the audio track for the channel. |
| TVG-CLOSED-CAPTIONS | Specifies whether the current channel has closed captions. This tag is used to indicate whether the channel offers closed captions. |
| TVG-CLOSED-CAPTIONS-LANGUAGE | Specifies the language of the closed captions for the current channel. This tag is used to set the language of the closed captions. |
| TVG-CLOSED-CAPTIONS-TYPE | Specifies the type of the closed captions for the current channel. This tag is used to set the type of the closed captions. |
| TVG-CONTENT-TYPE | Specifies the content type for the current channel. This tag is used to indicate the type of content being broadcast (e.g. movie, TVshow, documentary). |
| TVG-COPYRIGHT | Specifies the copyright information for the current channel. This tag is used to display the copyright information for the channel. |
| TVG-DURATION | Specifies the duration of the current media file. This tag is used to set the duration of the media file. |
| TVG-EXT-X-DISCONTINUITY | Specifies a discontinuity point in the media file. This tag is used to signal a break in the stream. |
| TVG-EXT-X-ENDLIST | Specifies the end of the media file. This tag is used to indicate the end of the playlist. |
| TVG-EXT-X-KEY | Specifies the encryption key for the media file. This tag is used to encrypt the media file. |
| TVG-EXT-X-MEDIA-SEQUENCE | Specifies the sequence number for the media file. This tag is used to indicate the order of the media files in the playlist. |
| TVG-EXT-X-PROGRAM-DATE-TIME | Specifies the date and time of the current media file. This tag is used to synchronize the media file with the program guide. |
| TVG-EXT-X-VERSION | Specifies the version of the M3U8 playlist format being used. This tag is used to indicate the version of the playlist. |
| TVG-GAP | Specifies the time gap (in seconds) between the end of the previous media file and the start of the current media file. This tag is used to synchronize the media files. |
| TVG-INDEPENDENT-SEGMENTS | Specifies whether the media files are independent segments. This tag is used to indicate whether the media files can be played independently. |
| TVG-MEDIA | Specifies the media type for the current media file. This tag is used to indicate the type of media being played (e.g. video, audio). |
| TVG-MEDIA-SEQUENCE | Specifies the sequence number for the media file. This tag is used to indicate the order of the media files in the playlist. |
| TVG-PLAYLIST-TYPE | Specifies the type of playlist being used. This tag is used to indicate whether the playlist is dynamic or static. |
| TVG-START | Specifies the start time (in seconds) for the current media file. This tag is used to set the start time for the media file. |
| TVG-TARGETDURATION | Specifies the maximum duration (in seconds) of the media files. This tag is used to set the maximum duration for the media files. |
| TVG-X-BYTERANGE | Specifies the byte range of the current media file. This tag is used to specify a byte range within a media file. |
| TVG-X-ENDLIST | Specifies the end of the media file. This tag is used to indicate the end of the playlist. |
| TVG-X-KEY | Specifies the encryption key for the media file. This tag is used to encrypt the media file. |
| TVG-X-MEDIA-SEQUENCE | Specifies the sequence number for the media file. This tag is used to indicate the order of the media files in the playlist. |
| TVG-X-PROGRAM-DATE-TIME | Specifies the date and time of the current media file. This tag is used to synchronize the media file with the program guide. |
| TVG-X-VERSION | Specifies the version of the M3U8 playlist format being used. This tag is used to indicate the version of the playlist. |
| TVG-RESOLUTION | Specifies the resolution of the current media file. This tag is used to set the resolution for the media file. |
| TVG-FRAMERATE | Specifies the frame rate of the current media file. |
