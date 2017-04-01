#!/bin/bash


folders=('chap2.1' 'chap2.2' 'chap2.3' 'chap3.0' 'chap3.1' 'chap3.3' 'chap3.4')
files=('activate' 'deactivate' 'setup' 'README.txt' '.gitignore')

for folder in ${folders[@]}; do
    for file in ${files[@]}; do
        rm ../${folder}/${file}
        echo "cp ./${file} ../${folder}"
        cp ./${file} ../${folder}
    done
done
