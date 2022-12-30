@echo off
cls
echo --------------------------------------------
echo Adicionando todos os arquivos... 
git add . 
echo .
echo --------------------------------------------
echo Criando o commit -M %1
git commit -M %1
echo .
echo --------------------------------------------
echo Empurrando as alterações para o GitHub
git push -u origin main 
echo --------------------------------------------
echo .