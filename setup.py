import os
import sys
from setuptools import find_packages, setup
from oscar import get_version

CODE_DIR = 'oscar'
PROJECT_DIR = os.path.dirname(__file__)

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
sys.path.append(os.path.join(PROJECT_DIR, CODE_DIR))


install_requires = [
    'django>=1.11,<2.2',
    # PIL is required for image fields, Pillow is the "friendly" PIL fork
    'pillow>=4.0',
    # Search support
    'django-haystack>=2.5.0,<3.0.0',
    # Treebeard is used for categories
    'django-treebeard>=4.3.0',
    # Sorl is used as the default thumbnailer
    'sorl-thumbnail>=12.4.1,<12.5',
    # Used for automatically building larger HTML tables
    'django-tables2>=1.19,<2.0',
    # Used for manipulating form field attributes in templates (eg: add
    # a css class)
    'django-widget-tweaks>=1.4.1',
]


setup(
    name='django-oscar-catalogue',
    version=get_version().replace(' ', '-'),
    packages=find_packages(CODE_DIR),
    include_package_data=True,
    license='LICENSE ATTACHED WITH SOURCE CODE',  # example license
    description='Django Oscar Catalogue is an extracted module from Django Oscar, to isolate  the catalogue module '
                'independently along with its dashboard.',
    long_description=README,
    url='https://github.com/jerinisready/Django-Oscar-Catalogue/',
    author='jerinisready',
    author_email='jerinisready@gmail.com',
    keywords="Django Oscar Catalogue, Django Oscar Products, Oscar Products Table, ",
    install_requires=install_requires,
    platforms=['linux'],
    package_dir={'': CODE_DIR},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: LICENSE ATTACHED WITH SOURCE CODE',  
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
)


