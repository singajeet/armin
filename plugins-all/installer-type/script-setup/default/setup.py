from setuptools import setup, find_packages

setup(
    name='default-installer-script-driver',
    version='1.0',

    description='The default driver to work as installer running as shell-script',

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

    provides=['driver.for.imstallers',
              ],

    packages=[
    'armin_ext',
    'armin_ext.script',
    ],
    include_package_data=True,

    entry_points={
        'installer.drivers': [
            'default_installer_driver = armin_ext.script.installer:ScriptFileDriver',
        ],
    },

    zip_safe=False,
)
