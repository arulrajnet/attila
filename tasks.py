# -*- coding: utf-8 -*-

import os
import shutil
import sys
import datetime

from invoke import task
from invoke.main import program
from invoke.util import cd
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer

'''
To use this

virtualenv .venv
source .venv/bin/activate
pip3 install invoke pelican ghp-import
invoke build
invoke serve
invoke gh-pages
'''

OPEN_BROWSER_ON_SERVE = False

CONFIG = {
  # Output path. Can be absolute or relative to tasks.py. Default: 'output'
  'deploy_path': 'output',
  # Github Pages configuration
  'github_pages_branch': 'gh-pages',
  'commit_message': "'Publish site on {}'".format(datetime.date.today().isoformat()),
  # Host and port for `serve`
  'host': 'localhost',
  'port': 8000,
}

@task
def clean(c):
  """Remove generated files"""
  if os.path.isdir(CONFIG['deploy_path']):
      shutil.rmtree(CONFIG['deploy_path'])
      os.makedirs(CONFIG['deploy_path'])

@task
def build(c):
  """Build local version of site"""
  c.run('asciidoctor -D {deploy_path} *.adoc'.format(**CONFIG))
  c.run('cp *.png {deploy_path}'.format(**CONFIG))
  c.run('mv {deploy_path}/README.html {deploy_path}/index.html'.format(**CONFIG))

@task
def serve(c):
  """Serve site at http://$HOST:$PORT/ (default is localhost:8000)"""

  class AddressReuseTCPServer(RootedHTTPServer):
      allow_reuse_address = True

  server = AddressReuseTCPServer(
      CONFIG['deploy_path'],
      (CONFIG['host'], CONFIG['port']),
      ComplexHTTPRequestHandler)

  if OPEN_BROWSER_ON_SERVE:
      # Open site in default browser
      import webbrowser
      webbrowser.open("http://{host}:{port}".format(**CONFIG))

  sys.stderr.write('Serving at {host}:{port} ...\n'.format(**CONFIG))
  server.serve_forever()

@task
def reserve(c):
  """`build`, then `serve`"""
  build(c)
  serve(c)

@task
def gh_pages(c):
  """Publish to GitHub Pages"""
  build(c)
  c.run('ghp-import -b {github_pages_branch} '
        '-m "{commit_message}" '
        '{deploy_path} -p'.format(**CONFIG))
