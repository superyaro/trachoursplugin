from setuptools import find_packages, setup

version='0.3.1'

setup(name='TracHoursPlugin',
      version=version,
      description="keep trac of the hours spent on bugs and whether these live up to estimates",
      author='David Turner and Jeff Hammel',
      author_email='jhammel@openplans.org',
      url='http://trac-hacks.org/wiki/TracHoursPlugin',
      keywords='trac plugin',
      license="GPL",
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests*']),
      include_package_data=True,
      package_data={'trachours': ['templates/*']},
      zip_safe=False,
      install_requires=['python-dateutil', 'FeedParser'],
      extras_require=dict(lxml=['lxml']),
      entry_points = """
      [trac.plugins]
      trachours.trachours = trachours.hours
      trachours.setup = trachours.setup
      trachours.multiproject = trachours.multiproject
      """,
      )

