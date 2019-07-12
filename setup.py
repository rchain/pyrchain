import setuptools
from pathlib import Path

setuptools.setup(
    name='pyrchain',
    version='0.1.5',
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
    ],
    extras_require={'dev': ['grpcio-tools', 'mypy', 'typing-extensions', 'mypy-protobuf']}
)
