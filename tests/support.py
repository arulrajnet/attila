# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import locale
import logging
import os
import re
import subprocess
import sys
import unittest
from contextlib import contextmanager
from functools import wraps
from logging.handlers import BufferingHandler
from os.path import abspath, dirname, join
from shutil import rmtree
from tempfile import mkdtemp

from six import StringIO

from pelican.contents import Article
from pelican.settings import (DEFAULT_CONFIG, read_settings)

__all__ = ['get_article', 'unittest', ]


@contextmanager
def temporary_folder():
    """creates a temporary folder, return it and delete it afterwards.

    This allows to do something like this in tests:

        >>> with temporary_folder() as d:
            # do whatever you want
    """
    tempdir = mkdtemp()
    try:
        yield tempdir
    finally:
        rmtree(tempdir)


def isplit(s, sep=None):
    """Behaves like str.split but returns a generator instead of a list.

    >>> list(isplit('\tUse the force\n')) == '\tUse the force\n'.split()
    True
    >>> list(isplit('\tUse the force\n')) == ['Use', 'the', 'force']
    True
    >>> (list(isplit('\tUse the force\n', "e"))
         == '\tUse the force\n'.split("e"))
    True
    >>> list(isplit('Use the force', "e")) == 'Use the force'.split("e")
    True
    >>> list(isplit('Use the force', "e")) == ['Us', ' th', ' forc', '']
    True

    """
    sep, hardsep = r'\s+' if sep is None else re.escape(sep), sep is not None
    exp, pos, length = re.compile(sep), 0, len(s)
    while True:
        m = exp.search(s, pos)
        if not m:
            if pos < length or hardsep:
                #      ^ mimic "split()": ''.split() returns []
                yield s[pos:]
            break
        start = m.start()
        if pos < start or hardsep:
            #           ^ mimic "split()": includes trailing empty string
            yield s[pos:start]
        pos = m.end()


def mute(returns_output=False):
    """Decorate a function that prints to stdout, intercepting the output.
    If "returns_output" is True, the function will return a generator
    yielding the printed lines instead of the return values.

    The decorator literally hijack sys.stdout during each function
    execution, so be careful with what you apply it to.

    >>> def numbers():
        print "42"
        print "1984"
    ...
    >>> numbers()
    42
    1984
    >>> mute()(numbers)()
    >>> list(mute(True)(numbers)())
    ['42', '1984']

    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            saved_stdout = sys.stdout
            sys.stdout = StringIO()

            try:
                out = func(*args, **kwargs)
                if returns_output:
                    out = isplit(sys.stdout.getvalue().strip())
            finally:
                sys.stdout = saved_stdout

            return out

        return wrapper

    return decorator


def get_article(title, slug, content, lang, extra_metadata=None):
    metadata = {'slug': slug, 'title': title, 'lang': lang}
    if extra_metadata is not None:
        metadata.update(extra_metadata)
    return Article(content, metadata=metadata)


def skipIfNoExecutable(executable):
    """Skip test if `executable` is not found

    Tries to run `executable` with subprocess to make sure it's in the path,
    and skips the tests if not found (if subprocess raises a `OSError`).
    """

    with open(os.devnull, 'w') as fnull:
        try:
            res = subprocess.call(executable, stdout=fnull, stderr=fnull)
        except OSError:
            res = None

    if res is None:
        return unittest.skip('{0} executable not found'.format(executable))

    return lambda func: func


def module_exists(module_name):
    """Test if a module is importable."""

    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True


def locale_available(locale_):
    old_locale = locale.setlocale(locale.LC_TIME)

    try:
        locale.setlocale(locale.LC_TIME, str(locale_))
    except locale.Error:
        return False
    else:
        locale.setlocale(locale.LC_TIME, old_locale)
        return True


def get_settings(**kwargs):
    """Provide tweaked setting dictionaries for testing

    Set keyword arguments to override specific settings.
    """
    settings = DEFAULT_CONFIG.copy()
    for key, value in kwargs.items():
        settings[key] = value
    return settings

def get_my_settings(**kwargs):
  PATH = abspath(dirname(__file__))
  default_conf = join(PATH, 'default_conf.py')
  settings = read_settings(default_conf)
  for key, value in kwargs.items():
    settings[key] = value
  return settings


class LogCountHandler(BufferingHandler):
    """Capturing and counting logged messages."""

    def __init__(self, capacity=1000):
        logging.handlers.BufferingHandler.__init__(self, capacity)

    def count_logs(self, msg=None, level=None):
        return len([
            l
            for l
            in self.buffer
            if (msg is None or re.match(msg, l.getMessage())) and
               (level is None or l.levelno == level)
        ])


class LoggedTestCase(unittest.TestCase):
    """A test case that captures log messages."""

    def setUp(self):
        super(LoggedTestCase, self).setUp()
        self._logcount_handler = LogCountHandler()
        logging.getLogger().addHandler(self._logcount_handler)

    def tearDown(self):
        logging.getLogger().removeHandler(self._logcount_handler)
        super(LoggedTestCase, self).tearDown()

    def assertLogCountEqual(self, count=None, msg=None, **kwargs):
        actual = self._logcount_handler.count_logs(msg=msg, **kwargs)
        self.assertEqual(
            actual, count,
            msg='expected {} occurrences of {!r}, but found {}'.format(
                count, msg, actual))

from bs4 import BeautifulSoup
from pelican.generators import (ArticlesGenerator, Generator, PagesGenerator,
                                PelicanTemplateNotFound, StaticGenerator,
                                TemplatePagesGenerator)
from pelican.readers import RstReader
from pelican.writers import Writer
from pelican.contents import (Article, Page)

CUR_DIR = os.path.dirname(__file__)
CONTENT_DIR = os.path.join(CUR_DIR, 'content')
OUTPUT_DIR = os.path.join(CUR_DIR, 'output')

class BaseTest(object):

  def __init__(self):
    self.initSettings()

  def initSettings(self):
    self.old_locale = locale.setlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, str('C'))
    self.settings = get_my_settings()
    self.settings['THEME'] = "../"
    self.settings['filenames'] = {}
    self.reader = RstReader(self.settings)
    self.writer = Writer("output", self.settings)

  def gen_article_and_html_from_rst(self, rstPath):
    content, metadata = self.reader.read(rstPath)
    article = Article(content=content, metadata=metadata)
    context = self.settings.copy()
    context['generated_content'] = {}
    context['static_links'] = set()
    context['static_content'] = {}
    context['localsiteurl'] = self.settings['SITEURL']
    generator = ArticlesGenerator( context=context, settings=self.settings, path=CONTENT_DIR, theme=self.settings['THEME'], output_path=OUTPUT_DIR)
    generator.generate_context()
    f = lambda a: True if (a.slug == article.slug) else False
    result = list(filter(f, generator.context["articles"]))[0]
    self.writer.write_file(
                result.save_as, generator.get_template('article'),
                generator.context, article=result)
    soup = BeautifulSoup(open("./"+self.writer.output_path+'/'+result.save_as), "html.parser")
    return (result, soup)

  def gen_page_and_html_from_rst(self, rstPath):
    content, metadata = self.reader.read(rstPath)
    page = Page(content=content, metadata=metadata)
    context = self.settings.copy()
    context['generated_content'] = {}
    context['static_links'] = set()
    context['static_content'] = {}
    context['localsiteurl'] = self.settings['SITEURL']
    generator = PagesGenerator( context=context, settings=self.settings, path=CONTENT_DIR, theme=self.settings['THEME'], output_path=OUTPUT_DIR)
    generator.generate_context()
    f = lambda a: True if (a.slug == page.slug) else False
    result = list(filter(f, generator.context["pages"]))[0]
    self.writer.write_file(
                result.save_as, generator.get_template('page'),
                generator.context, page=result)
    soup = BeautifulSoup(open("./"+self.writer.output_path+'/'+result.save_as), "html.parser")
    return (result, soup)

  def gen_tag_and_html_from_name(self, name):
    context = self.settings.copy()
    context['generated_content'] = {}
    context['static_links'] = set()
    context['static_content'] = {}
    context['localsiteurl'] = self.settings['SITEURL']
    generator = ArticlesGenerator( context=context, settings=self.settings, path=CONTENT_DIR, theme=self.settings['THEME'], output_path=OUTPUT_DIR)
    generator.generate_context()
    generator.generate_tags(self.writer.write_file)
    selectedTag = None

    for tag, articles in generator.tags.items():
      if tag.name == name:
        selectedTag = tag

    soup = BeautifulSoup(open("./"+self.writer.output_path+'/'+selectedTag.save_as), "html.parser")
    return (selectedTag, soup)

  def gen_category_and_html_from_name(self, name):
    context = self.settings.copy()
    context['generated_content'] = {}
    context['static_links'] = set()
    context['static_content'] = {}
    context['localsiteurl'] = self.settings['SITEURL']
    generator = ArticlesGenerator( context=context, settings=self.settings, path=CONTENT_DIR, theme=self.settings['THEME'], output_path=OUTPUT_DIR)
    generator.generate_context()
    generator.generate_categories(self.writer.write_file)
    selectedCategory = None

    for category, articles in generator.categories:
      if category.name == name:
        selectedCategory = category

    soup = BeautifulSoup(open("./"+self.writer.output_path+'/'+selectedCategory.save_as), "html.parser")
    return (selectedCategory, soup)

  def gen_author_and_html_from_name(self, name):
    context = self.settings.copy()
    context['generated_content'] = {}
    context['static_links'] = set()
    context['static_content'] = {}
    context['localsiteurl'] = self.settings['SITEURL']
    generator = ArticlesGenerator( context=context, settings=self.settings, path=CONTENT_DIR, theme=self.settings['THEME'], output_path=OUTPUT_DIR)
    generator.generate_context()
    generator.generate_authors(self.writer.write_file)
    selectedAuthor = None

    for author, articles in generator.authors:
      if author.name == name:
        selectedAuthor = author

    soup = BeautifulSoup(open("./"+self.writer.output_path+'/'+selectedAuthor.save_as), "html.parser")
    return (selectedAuthor, soup)