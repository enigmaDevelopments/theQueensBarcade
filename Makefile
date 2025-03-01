all: install build clean
install:
	pip install -r requirements.txt
build:
	python -m PyInstaller main.spec
clean:
	if exist build rd /s /q build