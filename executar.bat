@echo off
chcp 65001 > nul
echo ========================================================
echo  Executando Analise do Vestibular FATEC (Trabalho 4)
echo ========================================================
cd /d "%~dp0"
python executar_analise.py
pause
