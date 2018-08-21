from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='banktop',
    version='1.1',
    license='MIT',
    long_description=open('README.md').read(),
    zip_safe = False,
    packages=['banktop'],
    install_requires=reqs,
    entry_points= {
    	'console_scripts': ['banktop = banktop.main:main'],
    }
)
