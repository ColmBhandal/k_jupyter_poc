all: clean
	pip install .

clean:
	rm -rf build
	rm -rf dist
	rm -rf k_jupyter_poc.egg-info
