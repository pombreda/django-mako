#   Copyright (c) 2008 Mikeal Rogers
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from __future__ import absolute_import, unicode_literals
import tempfile

from django.utils.module_loading import import_by_path
from mako.template import Template
from ._lookup import TemplateLookup


lookup = None


class MakoMiddleware(object):

    def __init__(self):
        """Setup mako variables and lookup object"""
        from django.conf import settings

        # Set all mako variables based on django settings
        directories = getattr(
            settings,
            'MAKO_TEMPLATE_DIRS',
            settings.TEMPLATE_DIRS
        )
        module_directory = getattr(settings, 'MAKO_MODULE_DIR', None)
        if module_directory is None:
            module_directory = tempfile.mkdtemp()

        output_encoding = getattr(settings, 'MAKO_OUTPUT_ENCODING', 'utf-8')
        encoding_errors = getattr(settings, 'MAKO_ENCODING_ERRORS', 'replace')
        template_class = getattr(settings, 'MAKO_TEMPLATE_CLASS', Template)
        if isinstance(template_class, basestring):
            template_class = import_by_path(template_class)

        global lookup
        lookup = TemplateLookup(
            directories=directories,
            module_directory=module_directory,
            output_encoding=output_encoding,
            encoding_errors=encoding_errors,
            template_class=template_class,
        )

        import djangomako
        djangomako.lookup = lookup
