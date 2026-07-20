@echo off
cd /d "%~dp0"
set NUXT_API_BASE=http://localhost:8000
set NUXT_API_BASE_BROWSER=http://localhost:8000
call npm run dev
