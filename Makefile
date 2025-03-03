all: install buildAll
buildAll: 
	make buildThreaded
	make clean
	make buildCuda 
	make clean
	make buildMain
	make clean

ifeq ($(OS), Windows_NT)
install: requirements.txt
	pip install -r requirements.txt
	pip install --upgrade -r requirements.txt

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
build: main.spec
	python -m PyInstaller main.spec

clean:
	if exist build rd /s /q build
cleanAll: clean
	if exist dist rd /s /q dist

else
install:
	sudo apt-get update
	sudo apt-get install -y python3-tk pipx
	pipx ensurepath --force
	pipx install cupy-cuda12x --include-deps
	pipx install pyinstaller --include-deps
buildMain:
	echo 'def ai(input): from bot import ai as a; return a(input)' > botType.py
	make build
buildThreaded:
	echo 'def ai(input): from multibot import ai as a; return a(input)' > botType.py
	make build
	mv "dist/TheQueensBarcade" "dist/TheQueensBarcadeThreaded"
buildCuda:
	echo 'def ai(input): from cubot import ai as a; return a(input)' > botType.py
	make build
	mv "dist/TheQueensBarcade" "dist/TheQueensBarcadeCuda"
build: main.spec
	pyinstaller main.spec

clean:
	rm -rf build
cleanAll: clean
	rm -rf dist


endif