#!/bin/bash

arquivo_original="/Users/danilovalle/GitHub/iptv/list_base.txt"
arquivo_temporario="/Users/danilovalle/GitHub/iptv/base_list.txt"

# Contador de linhas
contador=1
total_linhas=$(wc -l < "$arquivo_original")

echo "Processando $total_linhas URLs..."
echo "=========================================="

# Processa cada linha
while IFS= read -r linha; do
    printf "Baixando %03d/%03d: %s\n" "$contador" "$total_linhas" "$linha"

    if curl --max-time 30 --silent --fail -o "M3UListas/lista_$(printf "%03d" $contador).m3u" "$linha"; then
        echo "  ✓ Sucesso"
        # Se for sucesso, mantém a linha no arquivo temporário
        echo "$linha" >> "$arquivo_temporario"
    else
        echo "  ✗ Falha (removendo do arquivo)"
        # Se falhar, NÃO adiciona ao arquivo temporário (remove a linha)
    fi

    ((contador++))

done < "$arquivo_original"

echo "=========================================="
echo "Processamento concluído!"

# Substitui o arquivo original pelo temporário
if mv "$arquivo_temporario" "$arquivo_original"; then
    linhas_finais=$(wc -l < "$arquivo_original")
    linhas_removidas=$((total_linhas - linhas_finais))
    echo "Arquivo atualizado: $arquivo_original"
    echo "Linhas removidas: $linhas_removidas"
    echo "Linhas restantes: $linhas_finais"
else
    echo "Erro ao atualizar o arquivo!"
    rm "$arquivo_temporario"
    exit 1
fi
