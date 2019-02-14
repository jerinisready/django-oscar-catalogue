import os
import sys
from setuptools import find_packages, setup


CODE_DIR = 'src'
PROJECT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(PROJECT_DIR, CODE_DIR))

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# sys.path.append(PROJECT_DIR)
# from oscar import get_version # noqa isort:skip

# # Use 'dev', 'beta', or 'final' as the 4th element to indicate release type.
VERSION = (0, 0, 1, 'beta', 1)


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    # Append 3rd digit if > 0
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    elif VERSION[3] != 'final':
        version = '%s %s' % (version, VERSION[3])
        if len(VERSION) == 5:
            version = '%s %s' % (version, VERSION[4])
    return version


install_requires = [
    'django>=1.11',

    'pillow>=4.0',    # PIL is required for image fields, Pillow is the "friendly" PIL fork

    'django-haystack>=2.5',    # Search support

    'django-treebeard>=4.3',    # Treebeard is used for categories

    'sorl-thumbnail>=12.4.1,<12.5',    # Sorl is used as the default thumbnailer

    'django-tables2>=1.19,<2.0',    # Used for automatically building larger HTML tables

    'django-widget-tweaks>=1.4',    # Used for manipulating form field attributes in templates (eg: add a css class)
]


setup(
    name='django-oscar-catalogue',
    version=get_version().replace(' ', '-'),
    packages=find_packages(CODE_DIR),
    package_dir={'': CODE_DIR},
    include_package_data=True,
    license='BSD',
    description='Django Oscar Catalogue is an extracted module from Django Oscar, to isolate  the catalogue module '
                'independently along with its dashboard.',
    long_description=README,
    url='https://github.com/jerinisready/django-oscar-catalogue',
    author='jerinisready',
    author_email='jerinisready@gmail.com',
    keywords="Django Oscar Catalogue, Django Oscar Products, Oscar Products Table, ",
    install_requires=install_requires,
    platforms=['linux'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
)


