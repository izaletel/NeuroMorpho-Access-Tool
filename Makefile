build:
	pyinstaller -D -F -w -n neuromorpho "main.py"
clean:
	rm -r build dist