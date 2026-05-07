@echo off
:: 1. Carrega Drivers (Opcional, deixei o que estava no seu original)
c:\windows\smarcatdrv.exe

:: 2. Configura Variaveis de Ambiente e Placa de Som
SET PATH=C:\DOS;C:\GAMES;C:\APPs\BANNER;C:\APPs\RDP;C:\WINDOWS;C:\WINDOWS\SYSTEM;C:\W32;C:\4DOS 
SET TEMP=C:\WINDOWS\TEMP
SET SOUND=C:\SB16
SET BLASTER=A220 I7 D1 H5 P330 T6
SET MIDI=SYNTH:1 MAP:E
C:\SB16\MIXERSET /P /Q

:: 3. Cria o 4START na hora (usamos .BTM para ser nativo e rapido no 4DOS)
echo @echo off > C:\4START.BTM
rem echo cls >> C:\4START.BTM
rem echo call C:\dos\lista.bat >> C:\4START.BTM
echo call menu >> C:\4START.BTM

:: 4. Transfere o controle para o 4DOS
C:\4DOS\4DOS.COM