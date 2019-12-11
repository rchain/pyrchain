from pathlib import Path

import setuptools

setuptools.setup(
    name='pyrchain',
    version='0.2.0',
    author='RChain Cooperative',
    author_email='rchain-makers@rchain.coop',
    description='Interface to RChain RNode RPC',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/rchain/pyrchain',
    packages=setuptools.find_namespace_packages(include=['rchain', 'rchain.*']),
    package_data={'rchain.vault': ['*.rho.tpl']},
    install_requires=[
        'grpcio',
        'protobuf',
        'ecdsa',
        'python-bitcoinlib',
        'cryptography',
        'eth_hash',
        'pycryptodome'
    ],
    extras_require={'dev': ['grpcio-tools', 'mypy', 'typing-extensions', 'mypy-protobuf', 'isort', 'pytest', 'typeshed']}
)
