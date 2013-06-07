from setuptools import setup, find_packages


setup(
    name='finance',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pandas',
        'nose',
        'flake8',
        'numpy',
    ],
)
