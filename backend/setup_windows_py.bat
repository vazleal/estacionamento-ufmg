@echo off
REM Script para configurar ambiente virtual Python e instalar dependências

REM Criar ambiente virtual
python -m venv venv

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Instalar dependências
pip install --upgrade pip
pip install fastapi uvicorn

REM Mensagem final
echo.
echo Ambiente configurado com sucesso!
echo Para ativar manualmente depois, use: call venv\Scripts\activate.bat
echo Para rodar o servidor: uvicorn main:app --reload
pause