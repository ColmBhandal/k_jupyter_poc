install-local:
	pip3 install .
	python3 -m k_jupyter_poc.install --user

uninstall:
	jupyter kernelspec uninstall k
	pip3 uninstall k_jupyter_poc

clean:
	rm -rf build
	rm -rf dist
	rm -rf k_jupyter_poc.egg-info
