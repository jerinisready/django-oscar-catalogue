# flake8: noqa, because URL syntax is more readable with long lines
from django.urls import path

from oscar.core.application import Application
from oscar.core.loading import get_class


class Shop(Application):
    name = None

    catalogue_app = get_class('catalogue.app', 'application')
    dashboard_app = get_class('dashboard.app', 'application')

    def get_urls(self):
        urls = [
                path('', self.catalogue_app.urls),
                path('dashboard/', self.dashboard_app.urls)
        ]

        return self.post_process_urls(urls)


application = Shop()
