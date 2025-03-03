all: install buildAll

install: requirements.txt
	pip install -r requirements.txt
	pip install --upgrade -r requirements.txt

buildAll: 
	make buildMain
	make clean
	make buildThreaded
	make clean
	make buildCuda 
	make clean
buildMain:
	echo def ai(input): from bot import ai as a; return a(input) > botType.py
	make build
	if exist "dist\TheQueensBarcade.exe" ren "dist\TheQueensBarcade.exe" "The Queens Barcade.exe"
buildThreaded:
	echo def ai(input): from multibot import ai as a; return a(input) > botType.py
	make build
	if exist "dist\TheQueensBarcade.exe" ren "dist\TheQueensBarcade.exe" "The Queens Barcade Threaded.exe"
buildCuda:
	echo def ai(input): from cubot import ai as a; return a(input) > botType.py
	make build
	if exist "dist\TheQueensBarcade.exe" ren "dist\TheQueensBarcade.exe" "The Queens Barcade Cuda.exe"
build:
	python -m PyInstaller main.spec

clean:
	if exist build rd /s /q build
cleanAll: clean
	if exist dist rd /s /q dist