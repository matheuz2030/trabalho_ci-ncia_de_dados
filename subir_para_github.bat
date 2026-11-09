@echo off
chcp 65001 > nul
echo ========================================================
echo   Enviar Projeto FATEC para o GitHub
echo ========================================================
echo.
cd /d "%~dp0"

echo 1. Certifique-se de ter criado um repositorio vazio no GitHub:
echo    https://github.com/new
echo.
set /p REPO_URL="Cole aqui o link do seu repositorio (ex: https://github.com/usuario/repo.git): "

if "%REPO_URL%"=="" (
    echo [ERRO] Link nao informado. Operacao cancelada.
    pause
    exit /b
)

echo.
echo [*] Conectando ao repositorio remoto...
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git branch -M main

echo [*] Enviando arquivos para o GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo  [SUCESSO] Projeto enviado para o GitHub com sucesso!
    echo ========================================================
) else (
    echo.
    echo [AVISO] Se for a primeira vez, o Git pode pedir seu login do GitHub no navegador.
)

echo.
pause
