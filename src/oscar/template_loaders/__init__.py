
from django.conf import settings as django_settings
from django.template.utils import get_app_template_dirs

from django.template.loaders.filesystem import Loader as FilesystemLoader


class OscarLoader(FilesystemLoader):

    def get_template_sources(self, template_name):
        if 'partials/partials' in template_name:
            template_name = template_name.replace('partials/partials', 'partials')
        return super(OscarLoader, self).get_template_sources(template_name=template_name)

    def get_dirs(self):
        return get_app_template_dirs('templates/oscar')
