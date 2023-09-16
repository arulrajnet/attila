# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import locale
from shutil import copy, rmtree

from support import (get_my_settings, unittest, BaseTest, CUR_DIR, CONTENT_DIR, OUTPUT_DIR)

def tearDownModule():
  print("teardown module")
  try:
    rmtree(OUTPUT_DIR)
  except OSError as e:
    print ("Error: %s - %s." % (e.filename,e.strerror))

class AuthorSocialLinksTest(unittest.TestCase, BaseTest):

  def setUp(self):
    self.initSettings()

  def tearDown(self):
    locale.setlocale(locale.LC_ALL, self.old_locale)

  def test_linkedin_link(self):
    authorName = "raj"
    self.settings['AUTHOR_META'] = {
      authorName: {
        'cover': "http://examble.com/cover.jpg",
        'linkedin': "mylinkedinname"
      }
    }
    self.settings['SHOW_AUTHOR_BIO_IN_ARTICLE'] = True
    rstPath="content/article_with_og_image.rst"
    result, soup = self.gen_article_and_html_from_rst(rstPath)
    selected = soup.find(name="span", attrs={"class": "post-author-linkedin"})
    selectedAnchor = selected.find(name="a")
    # Assertion
    self.assertTrue("https://www.linkedin.com/in/mylinkedinname" in selectedAnchor["href"])

    result, soup = self.gen_author_and_html_from_name(authorName)
    selected = soup.find(name="span", attrs={"class": "archive-links"})
    # Assertion
    self.assertTrue("https://www.linkedin.com/in/mylinkedinname" in str(selected))

if __name__ == '__main__':
  unittest.main()
