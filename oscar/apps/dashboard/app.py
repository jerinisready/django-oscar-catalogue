from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm

from oscar.core.application import (
    DashboardApplication as BaseDashboardApplication)
from oscar.core.loading import get_class


class DashboardApplication(BaseDashboardApplication):
    name = 'dashboard'
    # permissions_map = {
    #     'index': (['is_staff'], ['partner.dashboard_access']),
    # }

    index_view = get_class('dashboard.views', 'IndexView')
    catalogue_app = get_class('dashboard.catalogue.app', 'application')

    def get_urls(self):
        urls = [
            url(r'^$', self.index_view.as_view(), name='index'),
            url(r'^catalogue/', self.catalogue_app.urls),
        ]
        return self.post_process_urls(urls)


application = DashboardApplication()
