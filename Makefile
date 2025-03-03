all: install buildAll

install:
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
	echo 0 > botType.txt
	make build
	if exist "dist\TheQueensBarcade.exe" ren "dist\TheQueensBarcade.exe" "The Queens Barcade.exe"
buildThreaded:
	echo 1 > botType.txt
	make build
	if exist "dist\TheQueensBarcade.exe" ren "dist\TheQueensBarcade.exe" "The Queens Barcade Threaded.exe"
buildCuda:
	echo 2 > botType.txt
	make build
	if exist "dist\TheQueensBarcade.exe" ren "dist\TheQueensBarcade.exe" "The Queens Barcade Cuda.exe"
build:
	python -m PyInstaller main.spec

clean:
	if exist build rd /s /q build