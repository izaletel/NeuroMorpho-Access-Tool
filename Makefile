build:
	pyinstaller neuromorpho.spec
clean:
	rm -r build
	rm -r dist