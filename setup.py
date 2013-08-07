# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup

install_requires = [
    'minion-backend'
]

setup(name="minion-arachni-plugin",
      version="0.1",
      description="Arachni Plugin for Minion",
      url="https://github.com/ZaiLynch/minion-arachni-plugin/",
      author="zai",
      author_email="zai@z.ai",
      packages=['minion', 'minion.plugins'],
      namespace_packages=['minion', 'minion.plugins'],
      include_package_data=True,
      install_requires = install_requires)
