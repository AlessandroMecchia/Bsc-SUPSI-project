from setuptools import setup, find_packages

setup(
    name='client_lib',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    author='Mecchia ALessandro and Nicolet Paolo',
    description='client_lib library',
    python_requires='>=3.11',
)