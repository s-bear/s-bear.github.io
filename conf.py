# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SBP'
copyright = '2022, Samuel B Powell'
author = 'Samuel B Powell'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
	'myst_parser',
	'sphinx.ext.githubpages',
	'sphinx.ext.mathjax',
	'sphinx_design',
	'sphinx_togglebutton',
	]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

numfig = True #number figures

# -- Myst options ------------------------------------------------------------
# https://myst-parser.readthedocs.io/en/latest/configuration.html

myst_enable_extensions = [
	'colon_fence',
	#'dollarmath', #-- we can't use dollarmath because it interferes with custom tex macros
	'deflist',
	]
myst_title_to_header = True
myst_update_mathjax = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_title = "Your title"
#html_logo = "logo.png"
#html_favicon = "favicon.ico"
html_theme_options = {
	"home_page_in_toc": True,
	"use_sidenotes": True,
}

# -- MathJax Options ---------------------------------------------------------

mathjax3_config = {
	'options': {'processHtmlClass': 'tex2jax_process|mathjax_process|math|output_area'},
	'tex': {
		'inlineMath': [['$','$'],['\\(','\\)']],
		'macros': {
			'RR': '\\mathbb{R}', # real numbers
			'mat': ['\\mathbf{#1}',1], #matrix: bold, upright
			'trans': '\\intercal', #transpose T
			'units': ['\\ \\mathrm{\\left[#1\\right]}',1], #space, upright in []
		},
	}
}