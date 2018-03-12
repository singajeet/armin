from setuptools import setup, find_packages

setup(
    name='default-script-file-driver',
    version='1.0',

    description='The default driver to access scripts on file system',

    author='Ajeet Singh',
    author_email='singajeet@gmail.com',

    url='http://githubpages.com/singajeet',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=['driver.for.script.file',
              ],

    packages=[
    'armin_ext',
    'armin_ext.drivers',
    'armin_ext.drivers.script',
    ],
    include_package_data=True,

    entry_points={
        'script.file.drivers': [
            'file = armin_ext.drivers.script.file:ScriptFileDriver',
        ],
    },

    zip_safe=False,
)
