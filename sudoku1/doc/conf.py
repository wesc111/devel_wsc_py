# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SUDOKU doc'
copyright = '2024, Werner Schoegler'
author = 'Werner Schoegler'
release = '0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# the default theme
#html_theme = 'alabaster'

# some additional basic themes (in my opinion, all of these look worse than the default)
#html_theme = 'haiku'
#html_theme = 'sphinxdoc'
#html_theme = 'agogo'
#html_theme = 'traditional'

# additional themes:
# note: for following theme, please install this additional theme by 
#     $pip install sphinx-rtd-theme
html_theme = "sphinx_rtd_theme"

html_static_path = ['_static']
