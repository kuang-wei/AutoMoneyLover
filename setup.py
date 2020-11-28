from distutils.core import setup

setup(name='automoneylover',
      version='0.0.1',
      description='Automate Money Lover transaction logging',
      author='Kuang Wei',
      author_email='kuangwei0824@gmail.com',
      packages=['automoneylover'],
      install_requires=['mintapi',
                        'keyring',
                        'tabulate',
                        ],
      entry_points={
          'console_scripts': [
              'automoneylover:log = automoneylover.main:main',
          ]
      }
 )
