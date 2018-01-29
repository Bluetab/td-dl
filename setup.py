from pip.req import parse_requirements
from setuptools import setup

install_reqs = parse_requirements('./requirements.txt', session='hack')
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='data-lineage',
    version='0.0.1',
    description='Api for data lineage on neo4j',
    author='bluetab',
    author_email='bluetab@bluetab.net',
    license = 'Apache2 License',
    keywords = ['data-lineage', 'api', 'neo4j'],
    packages=['api', 'api.v1', 'api.common', 'api.settings', 'api.models'],
    include_package_data=True,
    install_requires=[reqs],
)
