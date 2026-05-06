@echo off
cls
echo --------------------------------------------
echo Adicionando todos os arquivos... 
git add . 
echo .
echo --------------------------------------------
echo Criando o commit -m "sobe"
git commit -m "sobe"
rem git commit -m %1
echo .
echo --------------------------------------------
echo Empurrando as alterações para o GitHub
git push 
rem git push -u origin main 
echo --------------------------------------------
echo .