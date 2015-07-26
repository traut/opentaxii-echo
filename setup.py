import os

from setuptools import setup, find_packages


CURRENT_DIR = os.path.dirname(__file__)


def get_file_contents(filename):
    with open(os.path.join(CURRENT_DIR, filename)) as fp:
        return fp.read()


install_requires = get_file_contents('requirements.txt').split()


setup(
    name='opentaxii-echo',
    version='0.0.1',
    description='Simple Echo implementation of OpenTAXII Persistence API',
    long_description=get_file_contents('README.rst'),
    url='https://github.com/traut/opentaxii-echo',
    author='Sergey Polzunov',
    author_email='sergey@polzunov.com',
    license='BSD License',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires
)
