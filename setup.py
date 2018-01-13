from setuptools import setup, find_packages

setup(
    name='banktop',
    version='1.0',
    license='MIT',
    long_description=open('README.txt').read(),
    zip_safe = False,
    #packages = find_packages(),
    packages=['banktop', 'banktop.prettytable' ],
   # package_date={'banktop': ['table.py']},
    entry_points= {
    	'console_scripts': ['banktop = banktop.main:main'],
    }
)