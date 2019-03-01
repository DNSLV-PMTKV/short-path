from setuptools import setup, find_packages

setup(
    name='shortPath',
    version='0.0.4',
    author='Danislav Pometkov',
    author_email='pometkov.d@gmail.com',
    description='Simple representation of BFS algorithm',
    license='MIT',
    url='https://github.com/DNSLV-PMTKV/short-path',
    packages=find_packages('src'),
    python_requires='>=3.6.0',
    required_for_install=['Pillow==5.4.1']
)
