import os
import setuptools

here = os.path.abspath(os.path.dirname(__file__))

setuptools.setup(
    name='ecard',
    version='0.1',
    author='52funny',
    url='https://github.com/52funny/ecard_python',
    author_email='wwq9977@gmail.com',
    description='Python Ecard',
    long_description='',
    packages=setuptools.find_packages(here)
)
