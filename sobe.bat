@echo off
cls
echo --------------------------------------------
echo Adicionando todos os arquivos... 
git add . 
echo .
echo --------------------------------------------
echo Criando o commit -m "update %date% %time:~0,8%"
git commit -m "update %date% %time:~0,8%"
rem git commit -m %1
echo .
echo --------------------------------------------
echo Empurrando as alterações para o GitHub
git push 
rem git push -u origin main 
echo --------------------------------------------
echo .


rem git pull
rem git add . 
rem git commit -m 'sonhagro' 
rem git commit -m "update %date% %time:~0,8%"
rem git push --force 
rem git push origin main
rem powershell -c "[console]::beep(1000,1000)" 