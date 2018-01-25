import pptx_template
from setuptools import setup

setup(name='pptx-template-fork',
      version=pptx_template.__version__,
      description='The PowerPoint presentation builder using template.pptx (without support in cli)',
      long_description=open('README.rst', encoding='utf-8').read(),
      url='https://github.com/skar404/pptx-template',
      author='Reki Murakami',
      author_email='skar404@gmail.com',
      license='Apache-2.0',
      packages=['pptx_template'],
      test_suite='test',
      install_requires=['python-pptx==0.6.6', 'pandas>=0.18.0', 'openpyxl>=2.4.7'],
      keywords=['powerpoint', 'ppt', 'pptx'],
      entry_points={"console_scripts": ["pptx_template=pptx_template.cli:main"]},
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Topic :: Utilities",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: OS Independent"
      ])
