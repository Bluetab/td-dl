from setuptools import setup

PATH_REQUIREMENTS="requirements/"
KEY_COMMON="common"
KEY_DEV="dev"
KEY_TEST="test"
FILE_REQUIREMENTS={KEY_DEV : "requirements-dev.txt",
    KEY_COMMON : "requirements.txt", KEY_TEST : "requirements-test.txt",
    }

REQUIREMENTS={}
for key, name_file in FILE_REQUIREMENTS.items():
    with open(PATH_REQUIREMENTS + name_file) as f:
        REQUIREMENTS[key] = f.read().splitlines()

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
    tests_require=[REQUIREMENTS[KEY_TEST]],
    include_package_data=True,
    install_requires=REQUIREMENTS[KEY_COMMON],
    extras_require={
        'dev': [
            REQUIREMENTS[KEY_DEV]
        ]
    }
)
