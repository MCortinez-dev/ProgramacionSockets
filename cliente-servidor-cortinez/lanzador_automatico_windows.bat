@echo off
echo Iniciando el Servidor...
start cmd /k "python servidor.py"

:: Espero al servidor
timeout /t 2 /nobreak > nul

echo Lanzando cliente que tipea
start cmd /k "python cliente.py"

echo Lanzando los bots de prueba...
start cmd /k "python cliente1boot.py"
start cmd /k "python cliente2boot.py"
start cmd /k "python cliente3boot.py"
start cmd /k "python cliente4boot.py"
start cmd /k "python cliente5boot.py"
start cmd /k "python cliente6boot.py"
start cmd /k "python cliente7boot.py"
start cmd /k "python cliente8boot.py"
start cmd /k "python cliente9boot.py"

echo Listo! Todos los procesos fueron lanzados en ventanas independientes.
echo Dirijase al proceso servidor para ver los procesos correr en paralelo.
echo ----------------------------------------------------------------------
echo El usuario que tipea puede ingresar:
echo					- Texto por teclado 
echo					- /users = Ver cantidad de usuarios conectados
echo					- /adios = Para desconectar

pause