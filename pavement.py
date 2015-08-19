from paver.easy import task, needs
from paver.setuputils import setup, install_distutils_tasks, find_package_data

import version


setup(name='si-prefix',
      version=version.getVersion(),
      description='Functions for formatting numbers according to SI standards.',
      keywords='si prefix format number precision',
      author='Christian Fobel',
      author_email='christian@fobel.net',
      url='https://github.com/cfobel/si-prefix',
      license='GPL',
      packages=['si_prefix', 'si_prefix.tests'])


@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass
