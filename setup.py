from setuptools import setup

setup(
    name='data-lineage',
    version='0.0.1',
    description='Api for data lineage on neo4j',
    author='bluetab',
    author_email='bluetab@bluetab.net',
    license='Apache2 License',
    keywords=['data-lineage', 'api', 'neo4j'],
    packages=['api', 'api.v1', 'api.common', 'api.settings'],
    include_package_data=True,
    install_requires=[
        'Fabric3==1.13.1.post1',
        'Flask==0.12.2',
        'Flask-Cors==3.0.2',
        'Flask-HTTPAuth==3.2.3',
        'gunicorn==19.7.1',
        'neo4j-driver==1.3.0',
        'nose2==0.7.3',
        'nose2==0.7.3',
        'PyJWT==1.5.3',
        'requests==2.18.4',
        'tornado==4.5.2'
    ],
)
