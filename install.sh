#!/bin/bash

# Verificamos todo lo necesario

case $1 in
    'unistall')

    echo "Se necesita contraseña de administrador para borrar los datos del programa:"
    sudo rm /usr/share/applications/slim-wallpaper.desktop 
    sudo rm /usr/bin/slim-wallpaper 
    if [ $? -eq 1 ]; then
        echo "Ocurrio error :("
    else
        echo "Listo"
    fi
    ;;

    'install')
    declare -a dependencias=( pkexe slim pygtk ); n=0; faltante=''
    echo "Buscando dependencias..."
    for i in ${dependencias[*]}
    do
        if [[ $i == 'slim' || $i == 'pkexec' ]]; then 
            which $i &>> /dev/null
            if [ $? -eq 1 ]; then
                echo "No se encontro $i"
                faltante=${faltante}" $i"
            else 
                echo "Encontrado $i"
               let n+=1
            fi
        else
            pydoc $i &>> /dev/null
            if [ $? -eq 1 ]; then 
                echo "No se encontro $i"
                faltante=${faltante}" $i"
            else 
                echo "Encontrado $i"
                let n+=1
            fi
        fi
    done

    if [ $n -eq 3 ]; then
        echo "Instalando..."
        echo "Necesita contraseña de administrador: "
        sudo cp slim-wallpaper.desktop /usr/share/applications/
        sudo cp slim-wallpaper.py /usr/bin/slim-wallpaper
        if [ $? -eq 1 ]; then
            echo "Ocurrio error inesperado :("
        else
            echo "Listo"
        fi
    else
        echo "Imposible instalar faltan dependencias"
        echo "Falta $faltante"
    fi
    ;;
    *)
    echo -e 'Uso:\nbash install.sh install\nbash install.sh unistall'
    ;;
esac
