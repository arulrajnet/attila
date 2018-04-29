# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import locale
import os
from codecs import open
from shutil import copy, rmtree
from tempfile import mkdtemp

from pelican.generators import (ArticlesGenerator, Generator, PagesGenerator,
                                PelicanTemplateNotFound, StaticGenerator,
                                TemplatePagesGenerator)
from support import (get_my_settings, unittest)

CUR_DIR = os.path.dirname(__file__)
CONTENT_DIR = os.path.join(CUR_DIR, 'content')


class TestGenerator(unittest.TestCase):
  def setUp(self):
    self.old_locale = locale.setlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, str('C'))
    self.settings = get_my_settings()
    print(self.settings)
    self.settings['THEME'] = "../"

  def test_article_cover(self):
    generator = ArticlesGenerator( context=self.settings.copy(), settings=self.settings, path=CONTENT_DIR, theme=self.settings['THEME'], output_path=None)

    generator.generate_context()
    print(generator)

  def test_tags_cover(self):
    pass

  def test_category_cover(self):
    pass

  def test_author_cover(self):
    pass

  def test_page_cover(self):
    pass

  def tearDown(self):
    locale.setlocale(locale.LC_ALL, self.old_locale)

if __name__ == '__main__':
  unittest.main()