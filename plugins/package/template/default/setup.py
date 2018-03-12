from setuptools import setup, find_packages

setup(
    name='default-package-template',
    version='1.0',

    description='The default package template',

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

    provides=['driver.for.templates',
              ],

    packages=[
    'armin_ext',
    'armin_ext.template',
    ],
    include_package_data=True,

    entry_points={
        'package.templates': [
            'default_package_template = armin_ext.template.package:Package',
        ],
    },

    zip_safe=False,
)
