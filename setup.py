from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='armin-studio',
    version='1.0',
    description='Armin Studio for rapid app development',
    long_description=readme(),
    author='Ajeet Singh',
    author_email='singajeet@gmail.com',
    url='http://githubpages.com/singajeet',
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Editor :: Tool',
                 ],
    license='MIT',
    keywords='armin ide studio editor tool rapid development',
    packages=[
        'armin',
        'armin.api',
        'armin.api.managers',
        'armin.api.managers.source',
        'armin.api.managers.io',
        'armin.api.managers.package',
        'armin.api.managers.hook',
        'armin.api.share',
        'armin.api.config',
        'armin.api.resources',
        'armin.api.tests',

    ],
    install_requires=[
        'tinydb',
        'stevedore',
        'typing',
        'configparser',
        'constantly',
        'aiohttp',
        'asyncio',
        'six',
        'pathlib',
        'goldfinch',
    ],
    entry_points={
        'console_scripts': ['armin=armin.api.command_line:main'],
    },
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
)
