#!/bin/bash

echo "Iniciando el Servidor..."
gnome-terminal -- bash -c "python3 servidor.py; exec bash"

# Espero al servidor
sleep 2

echo "Lanzando cliente que tipea"
gnome-terminal -- bash -c "python3 cliente.py; exec bash"

echo "Lanzando los bots de prueba..."
gnome-terminal -- bash -c "python3 cliente1boot.py; exec bash"
gnome-terminal -- bash -c "python3 cliente2boot.py; exec bash"
gnome-terminal -- bash -c "python3 cliente3boot.py; exec bash"
gnome-terminal -- bash -c "python3 cliente4boot.py; exec bash"
gnome-terminal -- bash -c "python3 cliente5boot.py; exec bash"
gnome-terminal -- bash -c "python3 cliente6boot.py; exec bash"
gnome-terminal -- bash -c "python3 cliente7boot.py; exec bash"
gnome-terminal -- bash -c "python3 cliente8boot.py; exec bash"
gnome-terminal -- bash -c "python3 cliente9boot.py; exec bash"

echo "Listo! Todos los procesos fueron lanzados en ventanas independientes."
echo "Dirijase al proceso servidor para ver los procesos correr en paralelo."
echo "----------------------------------------------------------------------"
echo "El usuario que tipea puede ingresar:"
echo "                    - Texto por teclado "
echo "                    - /users = Ver cantidad de usuarios conectados"
echo "                    - /adios = Para desconectar"

read -p "Presione [Enter] para salir..."