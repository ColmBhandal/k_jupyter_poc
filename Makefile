all: uninstall clean
	pip install .
	sudo python3 -m k_jupyter_poc.install

uninstall:
	jupyter kernelspec uninstall k
	pip uninstall k_jupyter_poc

clean:
	rm -rf build
	rm -rf dist
	rm -rf k_jupyter_poc.egg-info
