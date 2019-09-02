# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import locale
from shutil import copy, rmtree

from support import (get_my_settings, unittest, BaseTest, CUR_DIR, CONTENT_DIR, OUTPUT_DIR)

def setUpModule():
  print("setup module")

def tearDownModule():
  print("teardown module")
  try:
    rmtree(OUTPUT_DIR)
  except OSError as e:
    print ("Error: %s - %s." % (e.filename,e.strerror))

class ArticleCoverImageTest(unittest.TestCase, BaseTest):

  @classmethod
  def setUpClass(cls):
    print("setUpClass")

  @classmethod
  def tearDownClass(cls):
    print("tearDownClass")

  def setUp(self):
    self.initSettings()

  def tearDown(self):
    locale.setlocale(locale.LC_ALL, self.old_locale)

  def test_article_cover(self):
    self.settings['SITEURL']="http://www.example.com"
    rstPath="content/article_with_cover_image.rst"
    result, soup = self.gen_article_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+result.cover in selected["style"])

  def test_article_header_cover(self):
    self.settings['HEADER_COVER']='/assets/images/header_cover.jpg'
    rstPath="content/article_without_cover.rst"
    result, soup = self.gen_article_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['HEADER_COVER'] in selected["style"])

  def test_article_header_http_cover(self):
    self.settings['HEADER_COVER']='http://example.com/cover.jpg'
    rstPath="content/article_without_cover.rst"
    result, soup = self.gen_article_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COVER'] in selected["style"])

  def test_article_theme_cover(self):
    rstPath="content/article_without_cover.rst"
    result, soup = self.gen_article_and_html_from_rst(rstPath)
    selected = soup.find(id="post-header")
    # Assertion
    self.assertTrue("class" not in selected)

  def test_article_header_color(self):
    self.settings['HEADER_COLOR']='blue'
    rstPath="content/article_without_cover.rst"
    result, soup = self.gen_article_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COLOR'] in selected["style"])

  def test_article_http_cover(self):
    rstPath="content/article_with_http_cover_image.rst"
    result, soup = self.gen_article_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(result.cover in selected["style"])

  def test_article_og_cover(self):
    rstPath="content/article_with_og_image.rst"
    result, soup = self.gen_article_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(result.og_image in selected["style"])

class PageCoverImageTest(unittest.TestCase, BaseTest):

  def setUp(self):
    self.initSettings()

  def tearDown(self):
    locale.setlocale(locale.LC_ALL, self.old_locale)

  def test_page_cover(self):
    self.settings['SITEURL']="http://www.example.com"
    rstPath="content/pages/page_with_cover_image.rst"
    result, soup = self.gen_page_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+result.cover in selected["style"])

  def test_page_header_cover(self):
    self.settings['HEADER_COVER']='/assets/images/header_cover.jpg'
    rstPath="content/pages/page_without_cover_image.rst"
    result, soup = self.gen_page_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['HEADER_COVER'] in selected["style"])

  def test_page_header_http_cover(self):
    self.settings['HEADER_COVER']='http://example.com/cover.jpg'
    rstPath="content/pages/page_without_cover_image.rst"
    result, soup = self.gen_page_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COVER'] in selected["style"])

  def test_page_theme_cover(self):
    rstPath="content/pages/page_without_cover_image.rst"
    result, soup = self.gen_page_and_html_from_rst(rstPath)
    selected = soup.find(id="post-header")
    # Assertion
    self.assertTrue("class" not in selected)

  def test_page_header_color(self):
    self.settings['HEADER_COLOR']='blue'
    rstPath="content/pages/page_without_cover_image.rst"
    result, soup = self.gen_page_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COLOR'] in selected["style"])

  def test_page_http_cover(self):
    rstPath="content/pages/page_with_http_cover_image.rst"
    result, soup = self.gen_page_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(result.cover in selected["style"])

  def test_page_og_cover(self):
    rstPath="content/pages/page_with_og_image.rst"
    result, soup = self.gen_page_and_html_from_rst(rstPath)
    selected = soup.find(name="div", attrs={"class": "post-cover cover"})
    # Assertion
    self.assertTrue(result.og_image in selected["style"])

class TagCoverImageTest(unittest.TestCase, BaseTest):

  def setUp(self):
    self.initSettings()

  def tearDown(self):
    locale.setlocale(locale.LC_ALL, self.old_locale)

  def test_footag_theme_cover(self):
    result, soup = self.gen_tag_and_html_from_name("footag")
    selected = soup.find(id="blog-header")
    # Assertion
    self.assertTrue("class" not in selected)

  def test_footag_cover(self):
    tagName = "footag"
    self.settings['HEADER_COVERS_BY_TAG'] = {
      tagName: "/assets/images/foo_tag_cover.jpg"
    }
    result, soup = self.gen_tag_and_html_from_name(tagName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['HEADER_COVERS_BY_TAG'][tagName] in selected["style"])

  def test_footag_http_cover(self):
    tagName = "footag"
    self.settings['HEADER_COVERS_BY_TAG'] = {
      tagName: "http://examble.com/cover.jpg"
    }
    result, soup = self.gen_tag_and_html_from_name(tagName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COVERS_BY_TAG'][tagName] in selected["style"])

  def test_footag_header_cover(self):
    self.settings['SITEURL'] = "http://example.com"
    self.settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
    result, soup = self.gen_tag_and_html_from_name("footag")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings["HEADER_COVER"] in selected["style"])

  def test_footag_header_http_cover(self):
    self.settings["HEADER_COVER"] = "http://example.com/cover.jpg"
    result, soup = self.gen_tag_and_html_from_name("footag")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COVER"] in selected["style"])

  def test_footag_header_color(self):
    self.settings["HEADER_COLOR"] = "red"
    result, soup = self.gen_tag_and_html_from_name("footag")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COLOR"] in selected["style"])

  def test_bartag_theme_cover(self):
    result, soup = self.gen_tag_and_html_from_name("bartag")
    selected = soup.find(id="blog-header")
    # Assertion
    self.assertTrue("class" not in selected)

  def test_bartag_cover(self):
    tagName = "bartag"
    self.settings['HEADER_COVERS_BY_TAG'] = {
      tagName: "/assets/images/bar_tag_cover.jpg"
    }
    result, soup = self.gen_tag_and_html_from_name(tagName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['HEADER_COVERS_BY_TAG'][tagName] in selected["style"])

  def test_bartag_http_cover(self):
    tagName = "bartag"
    self.settings['HEADER_COVERS_BY_TAG'] = {
      tagName: "http://examble.com/cover.jpg"
    }
    result, soup = self.gen_tag_and_html_from_name(tagName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COVERS_BY_TAG'][tagName] in selected["style"])

  def test_bartag_header_cover(self):
    self.settings['SITEURL'] = "http://example.com"
    self.settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
    result, soup = self.gen_tag_and_html_from_name("bartag")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings["HEADER_COVER"] in selected["style"])

  def test_bartag_header_http_cover(self):
    self.settings["HEADER_COVER"] = "http://example.com/cover.jpg"
    result, soup = self.gen_tag_and_html_from_name("bartag")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COVER"] in selected["style"])

  def test_bartag_header_color(self):
    self.settings["HEADER_COLOR"] = "red"
    result, soup = self.gen_tag_and_html_from_name("bartag")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COLOR"] in selected["style"])


class CategoryCoverImageTest(unittest.TestCase, BaseTest):

  def setUp(self):
    self.initSettings()

  def tearDown(self):
    locale.setlocale(locale.LC_ALL, self.old_locale)

  def test_foo_theme_cover(self):
    result, soup = self.gen_category_and_html_from_name("foo")
    selected = soup.find(id="blog-header")
    # Assertion
    self.assertTrue("class" not in selected)

  def test_foo_cover(self):
    categoryName = "foo"
    self.settings['HEADER_COVERS_BY_CATEGORY'] = {
      categoryName: "/assets/images/foo_category_cover.jpg"
    }
    result, soup = self.gen_category_and_html_from_name(categoryName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['HEADER_COVERS_BY_CATEGORY'][categoryName] in selected["style"])

  def test_foo_http_cover(self):
    categoryName = "foo"
    self.settings['HEADER_COVERS_BY_CATEGORY'] = {
      categoryName: "http://examble.com/cover.jpg"
    }
    result, soup = self.gen_category_and_html_from_name(categoryName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COVERS_BY_CATEGORY'][categoryName] in selected["style"])

  def test_foo_header_cover(self):
    self.settings['SITEURL'] = "http://example.com"
    self.settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
    result, soup = self.gen_category_and_html_from_name("foo")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings["HEADER_COVER"] in selected["style"])

  def test_foo_header_http_cover(self):
    self.settings["HEADER_COVER"] = "http://example.com/cover.jpg"
    result, soup = self.gen_category_and_html_from_name("foo")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COVER"] in selected["style"])

  def test_foo_header_color(self):
    self.settings["HEADER_COLOR"] = "red"
    result, soup = self.gen_category_and_html_from_name("foo")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COLOR"] in selected["style"])

  def test_bar_theme_cover(self):
    result, soup = self.gen_category_and_html_from_name("bar")
    selected = soup.find(id="blog-header")
    # Assertion
    self.assertTrue("class" not in selected)

  def test_bar_cover(self):
    categoryName = "bar"
    self.settings['HEADER_COVERS_BY_CATEGORY'] = {
      categoryName: "/assets/images/bar_category_cover.jpg"
    }
    result, soup = self.gen_category_and_html_from_name(categoryName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings['HEADER_COVERS_BY_CATEGORY'][categoryName] in selected["style"])

  def test_bar_http_cover(self):
    categoryName = "bar"
    self.settings['HEADER_COVERS_BY_CATEGORY'] = {
      categoryName: "http://examble.com/cover.jpg"
    }
    result, soup = self.gen_category_and_html_from_name(categoryName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['HEADER_COVERS_BY_CATEGORY'][categoryName] in selected["style"])

  def test_bar_header_cover(self):
    self.settings['SITEURL'] = "http://example.com"
    self.settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
    result, soup = self.gen_category_and_html_from_name("bar")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings["HEADER_COVER"] in selected["style"])

  def test_bar_header_http_cover(self):
    self.settings["HEADER_COVER"] = "http://example.com/cover.jpg"
    result, soup = self.gen_category_and_html_from_name("bar")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COVER"] in selected["style"])

  def test_bar_header_color(self):
    self.settings["HEADER_COLOR"] = "red"
    result, soup = self.gen_category_and_html_from_name("bar")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COLOR"] in selected["style"])

class AuthorCoverImageTest(unittest.TestCase, BaseTest):

  def setUp(self):
    self.initSettings()

  def tearDown(self):
    locale.setlocale(locale.LC_ALL, self.old_locale)

  def test_arul_theme_cover(self):
    result, soup = self.gen_author_and_html_from_name("arul")
    selected = soup.find(id="blog-header")
    # Assertion
    self.assertTrue("class" not in selected)

  def test_arul_cover(self):
    authorName = "arul"
    self.settings['AUTHORS_BIO'] = {
      authorName: {
        'cover': "/assets/images/arul_author_cover.jpg"
      }
    }
    result, soup = self.gen_author_and_html_from_name(authorName)
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
    result, soup = self.gen_author_and_html_from_name(authorName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['AUTHORS_BIO'][authorName]['cover'] in selected["style"])

  def test_arul_header_cover(self):
    self.settings['SITEURL'] = "http://example.com"
    self.settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
    result, soup = self.gen_author_and_html_from_name("arul")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings["HEADER_COVER"] in selected["style"])

  def test_arul_header_http_cover(self):
    self.settings["HEADER_COVER"] = "http://example.com/cover.jpg"
    result, soup = self.gen_author_and_html_from_name("arul")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COVER"] in selected["style"])

  def test_arul_header_color(self):
    self.settings["HEADER_COLOR"] = "red"
    result, soup = self.gen_author_and_html_from_name("arul")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COLOR"] in selected["style"])

  def test_raj_theme_cover(self):
    result, soup = self.gen_author_and_html_from_name("raj")
    selected = soup.find(id="blog-header")
    # Assertion
    self.assertTrue("class" not in selected)

  def test_raj_cover(self):
    authorName = "raj"
    self.settings['AUTHORS_BIO'] = {
      authorName: {
        'cover': "/assets/images/raj_author_cover.jpg"
      }
    }
    result, soup = self.gen_author_and_html_from_name(authorName)
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
    result, soup = self.gen_author_and_html_from_name(authorName)
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['AUTHORS_BIO'][authorName]['cover'] in selected["style"])

  def test_raj_header_cover(self):
    self.settings['SITEURL'] = "http://example.com"
    self.settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
    result, soup = self.gen_author_and_html_from_name("raj")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings['SITEURL']+'/'+self.settings["HEADER_COVER"] in selected["style"])

  def test_raj_header_http_cover(self):
    self.settings["HEADER_COVER"] = "http://example.com/cover.jpg"
    result, soup = self.gen_author_and_html_from_name("raj")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COVER"] in selected["style"])

  def test_raj_header_color(self):
    self.settings["HEADER_COLOR"] = "red"
    result, soup = self.gen_author_and_html_from_name("raj")
    selected = soup.find(name="div", attrs={"class": "blog-cover cover"})
    # Assertion
    self.assertTrue(self.settings["HEADER_COLOR"] in selected["style"])

if __name__ == '__main__':
  unittest.main()