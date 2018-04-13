from setuptools import setup

PATH_REQUIREMENTS="requirements/"
KEY_COMMON="common"
KEY_DEV="dev"
KEY_TEST="test"
FILE_REQUIREMENTS={KEY_DEV : "requirements-dev.txt",
    KEY_COMMON : "requirements.txt", KEY_TEST : "requirements-test.txt",
    }

REQUIREMENTS={}
def get_requirements(key):
    with open(PATH_REQUIREMENTS + FILE_REQUIREMENTS[key]) as f:
        REQUIREMENTS[key] = f.read().splitlines()

    return REQUIREMENTS[key]

setup(
    name='td_dl',
    version='0.0.1',
    description='Api for data lineage on neo4j',
    author='bluetab',
    author_email='bluetab@bluetab.net',
    license='Apache2 License',
    keywords=['td_dl', 'api', 'neo4j'],
    packages=['api', 'api.v1', 'api.common', 'api.settings'],
    test_suite='nose2.collector.collector',
    tests_require=[get_requirements(KEY_TEST)],
    include_package_data=True,
    install_requires=get_requirements(KEY_COMMON),
    extras_require={
        'dev': [
            get_requirements(KEY_DEV)
        ]
    }
)
