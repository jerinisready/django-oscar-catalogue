DJANGO OSCAR CATALOGUE
======================


.. image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
   :target: https://www.python.org/
.. image:: https://img.shields.io/pypi/djversions/django-oscar-catalogue.svg?style=flat
.. image:: https://img.shields.io/pypi/pyversions/django-oscar-catalogue.svg?style=flat
.. image:: https://img.shields.io/pypi/wheel/django-oscar-catalogue.svg?style=flat
.. image:: https://img.shields.io/librariesio/github/jerinisready/django-oscar-catalogue.svg?label=Dependencies&style=flat
.. image:: https://img.shields.io/github/license/jerinisready/django-oscar-catalogue.svg?style=flat
.. image:: https://img.shields.io/badge/PyPi_Package-django_oscar_catalogue-25ABFF.svg
.. image:: https://img.shields.io/pypi/status/django-oscar-catalogue.svg?style=flat
.. image:: https://img.shields.io/pypi/format/django-oscar-catalogue.svg?style=flat
.. image:: https://img.shields.io/github/commit-activity/y/jerinisready/django-oscar-catalogue.svg?style=flat
.. image:: https://img.shields.io/github/contributors/jerinisready/django-oscar-catalogue.svg?label=Contributors&style=flat
.. image:: https://img.shields.io/pypi/implementation/django-oscar-catalogue.svg?label=Implementation&style=flat
.. image:: https://img.shields.io/pypi/v/django-oscar-catalogue.svg?colorB=orange&label=PyPi&style=flat
.. image:: https://img.shields.io/pypi/l/django-oscar-catalogue.svg?style=flat&label=License

Django Oscar Catalogue is a small packet of code extracted from Django Oscar,
to isolate the catalogue module independantly along with its dashboard.

Django Oscar Handles Products, Categories and its Attributes in one of the best approach,
which favors high amount of customization even from Dashboard. Also, it provides a basic
Dashboard to handle those products and associated things. django-oscar encapsulated all
those into a single module named 'oscar.apps.catalogue'.

Due to some Dependency with other modules inside django-oscar, Its module cannot be
isolated as it is. Django-Oscar-Catalogue filtered out these dependencies, and isolated
the module.

This retains the complete structure and interface with its parent package (Django Oscar),
so that, at any point of your project; you can simply unplug this module and install
django-oscar with minimum effort.


=================================
README - Django-Oscar-Catalogue
=================================


API Documentation for catalogue can be referred from official Documentation of django-oscar.


Packages.
`````````

Ensure these Python packages are added in your environment.

1) haystack          # Search support

2) treebeard         # Treebeard is used for categories

3) sorl_thumbnail    # Sorl is used as the default thumbnailer

4) django_tables2    # Used for automatically building larger HTML tables

5) Pillow            # PIL is required for image fields, Pillow is the "friendly" PIL fork

6) django-widget-tweaks   # Used for manipulating form field attributes in templates (eg: add a css class)


SETTINGS FOR PACKAGE
````````````````````
Almost All Oscar Settings are added in *'oscar.default.\*'*
You can override them after importing these settings in your settings.py .

``get_core_apps()`` will include the following apps with your INSTALLED_APPS.

.. code-block:: python

    OSCAR_CORE_APPS = [
        'oscar',
        'oscar.apps.catalogue',
        'oscar.apps.catalogue.reviews',
        'oscar.apps.dashboard',
        'oscar.apps.dashboard.catalogue',
        # 3rd-party apps that oscar depends on
        'haystack',
        'treebeard',
        'sorl.thumbnail',
        'django_tables2',
    ]

Django Oscar uses ``django.contrib.flatpages.middleware.FlatpageFallbackMiddleware``
to handle url fallbacks .

Oscar Guides Django to use 'OSCAR_MAIN_TEMPLATE_DIR' to search for oscar templates.

Oscar-Catalogue uses 'oscar.template_loaders.OscarLoader' as template loader.
This have nothing to do with oscar, and also django oscar do not have a package named template_loaders.

But when you switch to `django-oscar` package this line can be removed.

CONCEPT :

.. code-block:: python

    TEMPLATES[0]['OPTIONS']['context_processors'].append('oscar.core.context_processors.metadata')
    TEMPLATES[0]['OPTIONS']['loaders'].append('django.template.loaders.app_directories.Loader')
    TEMPLATES[0]['OPTIONS']['loaders'].append('oscar.template_loaders.OscarLoader')


Oscar Guides Django uses 'HAYSTACK_CONNECTIONS' To establish Haystack for search.

In your "settings.py"; append:

.. code-block:: python

    from oscar.defaults import *
    from oscar import get_core_apps

    INSTALLED_APPS = [
    ...
    ...
    ] + get_core_apps()

    SITE_ID = 1
    OSCAR_MAIN_TEMPLATE_DIR = os.path.join(os.path.join(BASE_DIR), 'oscar', 'templates', 'oscar')
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            ...
            ...
            'APP_DIRS': False,
            'OPTIONS': {
            'context_processors': [
                ...
                ...
                'oscar.core.context_processors.metadata',
            ],
            'loaders':[
                    'django.template.loaders.app_directories.Loader',
                    ...
                    'oscar.template_loaders.OscarLoader',   # only to be used with oscar_catalogue not with oscar
                ],
            },
        },
    ]

    MIDDLEWARE = (
        ...
        'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    )

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }



URLS FOR PACKAGE
`````````````````
Oscar-Catalogue uses these two urls to access catalogue of products and its dashboard.

.. code-block:: python

    urls = [
            path('', self.catalogue_app.urls),
            path('dashboard/', self.dashboard_app.urls)
    ]


in your ``urls.py``; append:

.. code-block:: python

    from...
    from oscar.app import application

    urlpatterns = [
        ...

        path('oscar/', include( application.urls[:2] )),    # NOQA, Depndancy; # only to be used with oscar_catalogue not with oscar
        ...
    ]
    """
    Note that "application.urls[:2]" will be used with django oscar catalogue and
    "application.urls" will be used with django oscar.
    """



While Switching to Django Oscar
```````````````````````````````
1) In your local, pull a new branch.

2) Keep all your code as it is.

3) pip uninstall django-oscar-catalogue

4) pip install django-oscar >


LICENSE
````````
Django - Oscar is released under the permissive New BSD license (see summary).

The basic copy of this project is forked from https://github.com/django-oscar/django-oscar/ and is liable to follow its license.

from LICENSE is added in the "LICENSE" file.


Contributors
````````````
We acknowledge and respect contributions towards django-oscar!


Contributing
`````````````
If you want to contribute to a project and make it better, your help is very welcome. Contributing is also a great way
to learn more about social coding on Github, new technologies and and their ecosystems and how to make constructive,
helpful bug reports, feature requests and the noblest of all contributions: a good, clean pull request.

django-oscar-contrib turned into a Github repository so you can, you know, contribute to it by making pull requests
We Call for contributions to make it efficient, up-to-date with django-oscar, and fixing any issue raised by others.

Pull a PR and Contributors List will be managed Soon.
If you find any bugs or issues, or anything regarding usage, feel free to use issue page.
Racing an issue is the greatest way to support us.


