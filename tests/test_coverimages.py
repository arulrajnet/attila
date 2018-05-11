# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import locale
import os
from bs4 import BeautifulSoup
from codecs import open
from shutil import copy, rmtree
from tempfile import mkdtemp

from pelican.generators import (ArticlesGenerator, Generator, PagesGenerator,
                                PelicanTemplateNotFound, StaticGenerator,
                                TemplatePagesGenerator)
from pelican.readers import RstReader
from pelican.writers import Writer
from pelican.contents import (Article, Page)
from support import (get_my_settings, unittest)

CUR_DIR = os.path.dirname(__file__)
CONTENT_DIR = os.path.join(CUR_DIR, 'content')
OUTPUT_DIR = os.path.join(CUR_DIR, 'output')

def setUpModule():
  print("setup module")

def tearDownModule():
  print("teardown module")

class ArticleCoverImageTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    print("setUpClass")

  @classmethod
  def tearDownClass(cls):
    print("tearDownClass")

  def setUp(self):
    self.old_locale = locale.setlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, str('C'))
    self.settings = get_my_settings()
    self.settings['THEME'] = "../"
    self.settings['filenames'] = {}
    self.reader = RstReader(self.settings)
    self.writer = Writer("output", self.settings)

  def tearDown(self):
    locale.setlocale(locale.LC_ALL, self.old_locale)

  def _article_and_html(self, rstPath):
    content, metadata = self.reader.read(rstPath)
    article = Article(content=content, metadata=metadata)
    generator = ArticlesGenerator( context=self.settings.copy(), settings=self.settings, path=CONTENT_DIR, theme=self.settings['THEME'], output_path=OUTPUT_DIR)
    generator.generate_context()
    f = lambda a: True if (a.slug == article.slug) else False
    result = filter(f, generator.context["articles"])[0]
    self.writer.write_file(
                result.save_as, generator.get_template('article'),
                generator.context, article=result)
    soup = BeautifulSoup(open("./"+self.writer.output_path+'/'+result.save_as), "html.parser")
    return (result, soup)

  def test_article_cover(self):
    self.settings['SITEURL']="http://www.example.com"
    rstPath="content/article_with_cover_image.rst"
    result, soup = self._article_and_html(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+result.cover in selected["style"])

  def test_article_header_cover(self):
    self.settings['HEADER_COVER']='/assets/images/header_cover.jpg'
    rstPath="content/article_without_cover.rst"
    result, soup = self._article_and_html(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['HEADER_COVER'] in selected["style"])

  def test_article_header_color(self):
    self.settings['HEADER_COLOR']='blue'
    rstPath="content/article_without_cover.rst"
    result, soup = self._article_and_html(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COLOR'] in selected["style"])

  def test_article_http_cover(self):
    rstPath="content/article_with_http_cover_image.rst"
    result, soup = self._article_and_html(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(result.cover in selected["style"])

  def test_article_og_cover(self):
    rstPath="content/article_with_og_image.rst"
    result, soup = self._article_and_html(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(result.og_image in selected["style"])

class PageCoverImageTest(unittest.TestCase):

  def setUp(self):
    self.old_locale = locale.setlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, str('C'))
    self.settings = get_my_settings()
    self.settings['THEME'] = "../"
    self.settings['filenames'] = {}
    self.reader = RstReader(self.settings)
    self.writer = Writer("output", self.settings)

  def tearDown(self):
    locale.setlocale(locale.LC_ALL, self.old_locale)

class TagCoverImageTest(unittest.TestCase):

  def setUp(self):
    self.old_locale = locale.setlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, str('C'))
    self.settings = get_my_settings()
    self.settings['THEME'] = "../"
    self.settings['filenames'] = {}
    self.reader = RstReader(self.settings)
    self.writer = Writer("output", self.settings)

  def tearDown(self):
    locale.setlocale(locale.LC_ALL, self.old_locale)

class CategoryCoverImageTest(unittest.TestCase):

  def setUp(self):
    self.old_locale = locale.setlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, str('C'))
    self.settings = get_my_settings()
    self.settings['THEME'] = "../"
    self.settings['filenames'] = {}
    self.reader = RstReader(self.settings)
    self.writer = Writer("output", self.settings)

  def tearDown(self):
    locale.setlocale(locale.LC_ALL, self.old_locale)

class AuthorCoverImageTest(unittest.TestCase):

  def setUp(self):
    self.old_locale = locale.setlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, str('C'))
    self.settings = get_my_settings()
    self.settings['THEME'] = "../"
    self.settings['filenames'] = {}
    self.reader = RstReader(self.settings)
    self.writer = Writer("output", self.settings)

  def tearDown(self):
    locale.setlocale(locale.LC_ALL, self.old_locale)

if __name__ == '__main__':
  unittest.main()