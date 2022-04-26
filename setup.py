from setuptools import setup

setup(name='k_jupyter_poc',
      version='0.0.0',
      description='POC K kernel for Jupyter',
      author='Colm Bhandal',
      author_email='bhandalc@gmail.com',
      license='MIT',
      classifiers=[
          'License :: OSI Approved :: MIT License',
      ],
      url='https://github.com/ColmBhandal/k-jupyter-poc',
      packages=['k_jupyter_poc'],
      keywords=['jupyter', 'notebook', 'kernel', 'k'],
      include_package_data=True
      )
