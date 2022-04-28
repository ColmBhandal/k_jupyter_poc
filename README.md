[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ColmBhandal/k_jupyter_demo/HEAD?filepath=home/jovyan/notebooks)

# k-jupyter-poc

POC of a K-Kernel for IPyton that is intended to be used with Jupyter Noteboooks. As the name suggests, this is just a POC and hasn't been rigorously tested or built to feature comppletion. However, it does demonstrate that Jupyter Notebooks may be a useful way to expose the ``K`` language interactively online.

## K-Notebooks

Since ``K`` is a meta-language, this makes Notebooks a little more complex than a standard language. For this reason, there are four types of code cells:
 1. ``K``-definition fragments - all cells are treated as fragments of one giant ``K`` definition, by default. The cells are not compiled when you "run" them in the Notebook. Rather they are simply buffered for later use.
 1. Kompile cells. These are any cells that start with the term ``kompile``. Such cells will ``kompile`` all previously encountered ``K``-fragments into a new file, according to the ``kompile`` command given.
 1. Kommand cells. These are cells that run specific ``K`` commands like ``krun`` or ``kparse``.
 1. Kode cells. These cells should start with a comment on the first line in the format ``//kode-file: FILE_NAME``. Subsequent lines should contain the code. Such cells  will result in a file by the name of ``FILE_NAME`` being created, whose contents are the code.

## Installation

The installation assumes you have ``K`` installed and also ``python3``. It also assumes that you've aliased ``python3`` as ``python`` e.g. see [here](https://askubuntu.com/questions/320996/how-to-make-python-program-command-execute-python-3). Since this is a POC only, it has only been published to test PyPi. To install as a user, do:

```
pip install --index-url https://test.pypi.org/simple/ k_jupyter_poc
python -m k_jupyter_poc.install --user
```

To uninstall, do:

```
jupyter kernelspec uninstall k
pip uninstall k_jupyter_poc
```

Note: the pakcage will be listed in ``pip`` as ``k-jupyter-poc`` (with dashes) rather than ``k_jupyter_poc`` (with underscores). 
This doesn't seem to be an issue. More on this [here](https://github.com/ros/rosdistro/issues/18116).

## Running

This assumes you have jupyter installed and that the ``jupyter-notebook`` command launches a Notebook. If not install Jupyter. Then to run, just launch ``jupyter-notebook`` and choose ``K`` as your Notebook type.
