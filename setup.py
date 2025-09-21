from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='blockchain_project',
    version='0.1.0',
    description='A basic blockchain project in Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Xgramm Platforms',
    author_email='bazarintechnologies@gmail.com',
    url='https://github.com/BazarinTech/BLOCKCHAIN-PROJECT.git',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'cryptography',
        'Flask',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'blockchain_cli=cli.cli:main',  # If you create a main function in cli.py
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)