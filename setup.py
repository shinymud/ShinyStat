from setuptools import find_packages, setup

# name can be any name.  This name will be used to create .egg file.
# name that is used in packages is the one that is used in the trac.ini file.
# use package name as entry_points
setup(
    name='TracShinyStat',
    version='1.0',
    author='Jess "Surrey" Coulter',
    author_email="jess@IncendiarySoftware.com",
    description= "A Trac plug-in that displays data retrieved from a ShinyMUD game.",
    license= "GPLv3",
    url="http://shiny.game-host.org",
    packages=find_packages(exclude=['*.tests*']),
    entry_points = """
        [trac.plugins]
        shinystat = shinystat
    """,
    package_data={'shinystat': ['templates/*.html', 
                                 'htdocs/css/*.css', 
                                 'htdocs/images/*']},
)
