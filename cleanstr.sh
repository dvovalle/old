#!/bin/bash

for x in $(ls M3UListas/)
do
    echo $x
    sed -i '' '/#EXTM3U/d' M3UListas/$x
    sed -i '' '/TUTORIAIS/d' M3UListas/$x
    sed -i '' '/##/d' M3UListas/$x
    sed -i '' '/^[[:space:]]*$/d' M3UListas/$x
    sed -i '' '/#EXT-X-SESSION/d' M3UListas/$x
done
