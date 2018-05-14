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
  # try:
  #   rmtree(OUTPUT_DIR)
  # except OSError, e:
  #   print ("Error: %s - %s." % (e.filename,e.strerror))

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

  def _gen_article_and_html_from_rst(self, rstPath):
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
    result, soup = self._gen_article_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+result.cover in selected["style"])

  def test_article_header_cover(self):
    self.settings['HEADER_COVER']='/assets/images/header_cover.jpg'
    rstPath="content/article_without_cover.rst"
    result, soup = self._gen_article_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['HEADER_COVER'] in selected["style"])

  def test_article_header_http_cover(self):
    self.settings['HEADER_COVER']='http://example.com/cover.jpg'
    rstPath="content/article_without_cover.rst"
    result, soup = self._gen_article_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COVER'] in selected["style"])

  def test_article_theme_cover(self):
    rstPath="content/article_without_cover.rst"
    result, soup = self._gen_article_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue("/theme/images/post-bg.jpg" in selected["style"])

  def test_article_header_color(self):
    self.settings['HEADER_COLOR']='blue'
    rstPath="content/article_without_cover.rst"
    result, soup = self._gen_article_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COLOR'] in selected["style"])

  def test_article_http_cover(self):
    rstPath="content/article_with_http_cover_image.rst"
    result, soup = self._gen_article_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(result.cover in selected["style"])

  def test_article_og_cover(self):
    rstPath="content/article_with_og_image.rst"
    result, soup = self._gen_article_and_html_from_rst(rstPath)
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

  def _gen_page_and_html_from_rst(self, rstPath):
    content, metadata = self.reader.read(rstPath)
    page = Page(content=content, metadata=metadata)
    generator = PagesGenerator( context=self.settings.copy(), settings=self.settings, path=CONTENT_DIR, theme=self.settings['THEME'], output_path=OUTPUT_DIR)
    generator.generate_context()
    f = lambda a: True if (a.slug == page.slug) else False
    result = filter(f, generator.context["pages"])[0]
    self.writer.write_file(
                result.save_as, generator.get_template('page'),
                generator.context, page=result)
    soup = BeautifulSoup(open("./"+self.writer.output_path+'/'+result.save_as), "html.parser")
    return (result, soup)

  def test_page_cover(self):
    self.settings['SITEURL']="http://www.example.com"
    rstPath="content/pages/page_with_cover_image.rst"
    result, soup = self._gen_page_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+result.cover in selected["style"])

  def test_page_header_cover(self):
    self.settings['HEADER_COVER']='/assets/images/header_cover.jpg'
    rstPath="content/pages/page_without_cover_image.rst"
    result, soup = self._gen_page_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['HEADER_COVER'] in selected["style"])

  def test_page_header_http_cover(self):
    self.settings['HEADER_COVER']='http://example.com/cover.jpg'
    rstPath="content/pages/page_without_cover_image.rst"
    result, soup = self._gen_page_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COVER'] in selected["style"])

  def test_page_theme_cover(self):
    rstPath="content/pages/page_without_cover_image.rst"
    result, soup = self._gen_page_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue("/theme/images/post-bg.jpg" in selected["style"])

  def test_page_header_color(self):
    self.settings['HEADER_COLOR']='blue'
    rstPath="content/pages/page_without_cover_image.rst"
    result, soup = self._gen_page_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COLOR'] in selected["style"])

  def test_page_http_cover(self):
    rstPath="content/pages/page_with_http_cover_image.rst"
    result, soup = self._gen_page_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(result.cover in selected["style"])

  def test_page_og_cover(self):
    rstPath="content/pages/page_with_og_image.rst"
    result, soup = self._gen_page_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(result.og_image in selected["style"])

class TagCoverImageTest(unittest.TestCase):

  def setUp(self):
    self.old_locale = locale.setlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, str('C'))
    self.settings = get_my_settings()
    self.settings['THEME'] = "../"
    self.settings['filenames'] = {}
    self.reader = RstReader(self.settings)
    self.writer = Writer("output", self.settings)

  def _gen_tag_and_html_from_name(self, name):
    generator = ArticlesGenerator( context=self.settings.copy(), settings=self.settings, path=CONTENT_DIR, theme=self.settings['THEME'], output_path=OUTPUT_DIR)
    generator.generate_context()
    generator.generate_tags(self.writer.write_file)
    selectedTag = None

    for tag, articles in generator.tags.items():
      if tag.name == name:
        selectedTag = tag

    soup = BeautifulSoup(open("./"+self.writer.output_path+'/'+selectedTag.save_as), "html.parser")
    return (selectedTag, soup)

  def tearDown(self):
    locale.setlocale(locale.LC_ALL, self.old_locale)

  def test_footag_theme_cover(self):
    result, soup = self._gen_tag_and_html_from_name("footag")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue("/theme/images/post-bg.jpg" in selected["style"])

  def test_footag_cover(self):
    tagName = "footag"
    self.settings['HEADER_COVERS_BY_TAG'] = {
      tagName: "/assets/images/foo_tag_cover.jpg"
    }
    result, soup = self._gen_tag_and_html_from_name(tagName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['HEADER_COVERS_BY_TAG'][tagName] in selected["style"])

  def test_footag_http_cover(self):
    tagName = "footag"
    self.settings['HEADER_COVERS_BY_TAG'] = {
      tagName: "http://examble.com/cover.jpg"
    }
    result, soup = self._gen_tag_and_html_from_name(tagName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COVERS_BY_TAG'][tagName] in selected["style"])

  def test_footag_header_cover(self):
    self.settings['SITEURL'] = "http://example.com"
    self.settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
    result, soup = self._gen_tag_and_html_from_name("footag")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings["HEADER_COVER"] in selected["style"])

  def test_footag_header_http_cover(self):
    self.settings["HEADER_COVER"] = "http://example.com/cover.jpg"
    result, soup = self._gen_tag_and_html_from_name("footag")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COVER"] in selected["style"])

  def test_footag_header_color(self):
    self.settings["HEADER_COLOR"] = "red"
    result, soup = self._gen_tag_and_html_from_name("footag")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COLOR"] in selected["style"])

  def test_bartag_theme_cover(self):
    result, soup = self._gen_tag_and_html_from_name("bartag")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue("/theme/images/post-bg.jpg" in selected["style"])

  def test_bartag_cover(self):
    tagName = "bartag"
    self.settings['HEADER_COVERS_BY_TAG'] = {
      tagName: "/assets/images/bar_tag_cover.jpg"
    }
    result, soup = self._gen_tag_and_html_from_name(tagName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['HEADER_COVERS_BY_TAG'][tagName] in selected["style"])

  def test_bartag_http_cover(self):
    tagName = "bartag"
    self.settings['HEADER_COVERS_BY_TAG'] = {
      tagName: "http://examble.com/cover.jpg"
    }
    result, soup = self._gen_tag_and_html_from_name(tagName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COVERS_BY_TAG'][tagName] in selected["style"])

  def test_bartag_header_cover(self):
    self.settings['SITEURL'] = "http://example.com"
    self.settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
    result, soup = self._gen_tag_and_html_from_name("bartag")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings["HEADER_COVER"] in selected["style"])

  def test_bartag_header_http_cover(self):
    self.settings["HEADER_COVER"] = "http://example.com/cover.jpg"
    result, soup = self._gen_tag_and_html_from_name("bartag")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COVER"] in selected["style"])

  def test_bartag_header_color(self):
    self.settings["HEADER_COLOR"] = "red"
    result, soup = self._gen_tag_and_html_from_name("bartag")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COLOR"] in selected["style"])


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

  def _gen_category_and_html_from_name(self, name):
    generator = ArticlesGenerator( context=self.settings.copy(), settings=self.settings, path=CONTENT_DIR, theme=self.settings['THEME'], output_path=OUTPUT_DIR)
    generator.generate_context()
    generator.generate_categories(self.writer.write_file)
    selectedCategory = None

    for category, articles in generator.categories:
      if category.name == name:
        selectedCategory = category

    soup = BeautifulSoup(open("./"+self.writer.output_path+'/'+selectedCategory.save_as), "html.parser")
    return (selectedCategory, soup)

  def test_foo_theme_cover(self):
    result, soup = self._gen_category_and_html_from_name("foo")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue("/theme/images/post-bg.jpg" in selected["style"])

  def test_foo_cover(self):
    categoryName = "foo"
    self.settings['HEADER_COVERS_BY_CATEGORY'] = {
      categoryName: "/assets/images/foo_category_cover.jpg"
    }
    result, soup = self._gen_category_and_html_from_name(categoryName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['HEADER_COVERS_BY_CATEGORY'][categoryName] in selected["style"])

  def test_foo_http_cover(self):
    categoryName = "foo"
    self.settings['HEADER_COVERS_BY_CATEGORY'] = {
      categoryName: "http://examble.com/cover.jpg"
    }
    result, soup = self._gen_category_and_html_from_name(categoryName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COVERS_BY_CATEGORY'][categoryName] in selected["style"])

  def test_foo_header_cover(self):
    self.settings['SITEURL'] = "http://example.com"
    self.settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
    result, soup = self._gen_category_and_html_from_name("foo")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings["HEADER_COVER"] in selected["style"])

  def test_foo_header_http_cover(self):
    self.settings["HEADER_COVER"] = "http://example.com/cover.jpg"
    result, soup = self._gen_category_and_html_from_name("foo")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COVER"] in selected["style"])

  def test_foo_header_color(self):
    self.settings["HEADER_COLOR"] = "red"
    result, soup = self._gen_category_and_html_from_name("foo")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COLOR"] in selected["style"])

  def test_bar_theme_cover(self):
    result, soup = self._gen_category_and_html_from_name("bar")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue("/theme/images/post-bg.jpg" in selected["style"])

  def test_bar_cover(self):
    categoryName = "bar"
    self.settings['HEADER_COVERS_BY_CATEGORY'] = {
      categoryName: "/assets/images/bar_category_cover.jpg"
    }
    result, soup = self._gen_category_and_html_from_name(categoryName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['HEADER_COVERS_BY_CATEGORY'][categoryName] in selected["style"])

  def test_bar_http_cover(self):
    categoryName = "bar"
    self.settings['HEADER_COVERS_BY_CATEGORY'] = {
      categoryName: "http://examble.com/cover.jpg"
    }
    result, soup = self._gen_category_and_html_from_name(categoryName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COVERS_BY_CATEGORY'][categoryName] in selected["style"])

  def test_bar_header_cover(self):
    self.settings['SITEURL'] = "http://example.com"
    self.settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
    result, soup = self._gen_category_and_html_from_name("bar")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings["HEADER_COVER"] in selected["style"])

  def test_bar_header_http_cover(self):
    self.settings["HEADER_COVER"] = "http://example.com/cover.jpg"
    result, soup = self._gen_category_and_html_from_name("bar")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COVER"] in selected["style"])

  def test_bar_header_color(self):
    self.settings["HEADER_COLOR"] = "red"
    result, soup = self._gen_category_and_html_from_name("bar")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COLOR"] in selected["style"])

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

  def _gen_author_and_html_from_name(self, name):
    generator = ArticlesGenerator( context=self.settings.copy(), settings=self.settings, path=CONTENT_DIR, theme=self.settings['THEME'], output_path=OUTPUT_DIR)
    generator.generate_context()
    generator.generate_authors(self.writer.write_file)
    selectedAuthor = None

    for author, articles in generator.authors:
      if author.name == name:
        selectedAuthor = author

    soup = BeautifulSoup(open("./"+self.writer.output_path+'/'+selectedAuthor.save_as), "html.parser")
    return (selectedAuthor, soup)

  def test_arul_theme_cover(self):
    result, soup = self._gen_author_and_html_from_name("arul")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue("/theme/images/post-bg.jpg" in selected["style"])

  def test_arul_cover(self):
    authorName = "arul"
    self.settings['AUTHORS_BIO'] = {
      authorName: {
        'cover': "/assets/images/arul_author_cover.jpg"
      }
    }
    result, soup = self._gen_author_and_html_from_name(authorName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['AUTHORS_BIO'][authorName]['cover'] in selected["style"])

  def test_arul_http_cover(self):
    authorName = "arul"
    self.settings['AUTHORS_BIO'] = {
      authorName: {
        'cover': "http://examble.com/cover.jpg"
      }
    }
    result, soup = self._gen_author_and_html_from_name(authorName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['AUTHORS_BIO'][authorName]['cover'] in selected["style"])

  def test_arul_header_cover(self):
    self.settings['SITEURL'] = "http://example.com"
    self.settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
    result, soup = self._gen_author_and_html_from_name("arul")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings["HEADER_COVER"] in selected["style"])

  def test_arul_header_http_cover(self):
    self.settings["HEADER_COVER"] = "http://example.com/cover.jpg"
    result, soup = self._gen_author_and_html_from_name("arul")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COVER"] in selected["style"])

  def test_arul_header_color(self):
    self.settings["HEADER_COLOR"] = "red"
    result, soup = self._gen_author_and_html_from_name("arul")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COLOR"] in selected["style"])

  def test_raj_theme_cover(self):
    result, soup = self._gen_author_and_html_from_name("raj")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue("/theme/images/post-bg.jpg" in selected["style"])

  def test_raj_cover(self):
    authorName = "raj"
    self.settings['AUTHORS_BIO'] = {
      authorName: {
        'cover': "/assets/images/raj_author_cover.jpg"
      }
    }
    result, soup = self._gen_author_and_html_from_name(authorName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['AUTHORS_BIO'][authorName]['cover'] in selected["style"])

  def test_raj_http_cover(self):
    authorName = "raj"
    self.settings['AUTHORS_BIO'] = {
      authorName: {
        'cover': "http://examble.com/cover.jpg"
      }
    }
    result, soup = self._gen_author_and_html_from_name(authorName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['AUTHORS_BIO'][authorName]['cover'] in selected["style"])

  def test_raj_header_cover(self):
    self.settings['SITEURL'] = "http://example.com"
    self.settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
    result, soup = self._gen_author_and_html_from_name("raj")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings["HEADER_COVER"] in selected["style"])

  def test_raj_header_http_cover(self):
    self.settings["HEADER_COVER"] = "http://example.com/cover.jpg"
    result, soup = self._gen_author_and_html_from_name("raj")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COVER"] in selected["style"])

  def test_raj_header_color(self):
    self.settings["HEADER_COLOR"] = "red"
    result, soup = self._gen_author_and_html_from_name("raj")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COLOR"] in selected["style"])

if __name__ == '__main__':
  unittest.main()