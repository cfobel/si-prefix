from paver.easy import task, needs, path, sh, cmdopts
from paver.setuputils import setup, install_distutils_tasks, find_package_data
from distutils.extension import Extension
from optparse import make_option
from Cython.Build import cythonize

import version


pyx_files = ['si_prefix/si_prefix.pyx']


ext_modules = [Extension(f[:-4].replace('/', '.'), [f],
                         extra_compile_args=['-O3'],
                         include_dirs=['cythrust'])
               for f in pyx_files]

ext_modules = cythonize(ext_modules)


setup(name='si-prefix',
      version=version.getVersion(),
      description='Functions for formatting numbers according to SI standards.',
      keywords='si prefix format number precision',
      author='Christian Fobel',
      url='https://github.com/cfobel/si_prefix',
      license='GPL',
      packages=['si_prefix'],
      package_data=find_package_data('si_prefix', package='si_prefix',
                                     only_in_packages=False),
      ext_modules=ext_modules)


@task
@needs('build_ext', 'generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass
