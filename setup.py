import glob
import os

from setuptools import setup, find_packages

data_files = []


def append_files(path):
    directories = glob.glob(path)
    for directory in directories:
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                data_files.append((directory, [directory + r"/" + file]))


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

append_files('support')
append_files('servir_template/support/SERVIR_AppTemplate')
append_files('servir_template/support/templates/socialaccount')
append_files('servir_template/support/templates/WebApp')
append_files('servir_template/support/WebApp')
append_files('servir_template/support/WebApp/static')
append_files('servir_template/support/WebApp/static/css')
append_files('servir_template/support/WebApp/static/images')
append_files('servir_template/support/WebApp/static/images/basemaps')
append_files('servir_template/support/WebApp/static/images/cards')
append_files('servir_template/support/WebApp/static/images/logos')
append_files('servir_template/support/WebApp/static/images/readme')
append_files('servir_template/support/WebApp/static/images/teammembers')
append_files('servir_template/support/WebApp/static/js')
append_files('servir_template/support/WebApp/static/webfonts')

setup(
    name='SERVIR_Template_CLI',
    version='0.0.25',
    author='Billy Ashmall',
    author_email='billy.ashmall@nasa.gov',
    license='MIT License',
    description='Installer for the SERVIR App Template',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/SERVIR/SERVIR_Template_CLI',
    py_modules=['servir_template', 'app', 'default_files'],
    data_files=data_files,
    packages=find_packages(),
    install_requires=['click>=7.1.2',
                      'django>=4.1',
                      'GitPython',
                      'click'],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        servir_template=servir_template.servir_template:cli
    ''',
    include_package_data=True,
)
