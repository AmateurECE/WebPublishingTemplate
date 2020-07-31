###############################################################################
# NAME:             GenerateMakefile.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      Creates a makefile for the project.
#
# CREATED:          07/18/2020
#
# LAST EDITED:      07/31/2020
###

from os import walk, path
from datetime import datetime

PAGE_DATA = {}
INDEX = 'index.tex'
BOOK_MAIN = ''
BOOK_EXCLUDE = []
BOOK_OUTPUT = ''

try:
    import makefile_config
    if 'PAGE_DATA' in makefile_config.__dict__:
        PAGE_DATA = makefile_config.PAGE_DATA
    if 'INDEX' in makefile_config.__dict__:
        INDEX = makefile_config.INDEX
    if 'BOOK_MAIN' in makefile_config.__dict__:
        BOOK_MAIN = makefile_config.BOOK_MAIN
    if 'BOOK_EXCLUDE' in makefile_config.__dict__:
        BOOK_EXCLUDE = makefile_config.BOOK_EXCLUDE
    if 'BOOK_OUTPUT' in makefile_config.__dict__:
        BOOK_OUTPUT = makefile_config.BOOK_OUTPUT
except ImportError:
    pass

PREAMBLE = """
# Generated by GenerateMakefile.py (Ethan D. Twardy),
# on: {}
"""

BUILD_RULE = """
build: $(pdfFiles) $(erbFiles) {}
	python3 Navigation.py -b '{}' $(htmlFiles)
	middleman build
"""

DEPLOY_RULE = """
host=edtwardy@192.168.1.60
remotePath=/var/www/edtwardy.hopto.org/THE_LOCATION/
deploy: build
	rsync -r -e 'ssh -p 5000' --delete build/ pdf \\
		"$(host):$(remotePath)"
"""

CLEAN_RULE = """
clean:
	rm -f `find source -name '*.html.erb' | grep -v 'index'`
	rm -rf build/
	rm -rf pdf/
	git clean -fd
	rm -f Makefile
"""

PDF_RULE_FORMAT = """
{}: {}
	pdflatex --interaction=batchmode --shell-escape $< 2>&1 >/dev/null
	pdflatex --interaction=batchmode --shell-escape $< 2>&1 >/dev/null
	mkdir -p $(@D)
	-mv $(basename $(<F)).pdf $@
"""

HTML_RULE_FORMAT = """
{}: {}
	make4ht -sm draft -c tex4ht.cfg -f html5+tidy+join_colors $< >/dev/null
	-mv $(basename $(<F)).html $@
	-mv $(basename $(<F)).css $(basename $(@F)).css
"""

ERB_RULE_FORMAT = """
{}: {}
	mkdir -p $(@D)
	python3 Prepare.py -d '{}' $< $(basename $(<F)).css $@
"""

def warn(message):
    """Prints a warning to stdout"""
    warning = '\033[1;33m'
    noColor = '\033[0m'
    print(f'[GenerateMakefile.py] {warning}Warning{noColor}: {message}')

def getLatexFiles():
    """Locates LaTeX files in the subtree of the current directory"""
    latexFiles = []
    for dirpath, dirnames, filenames in walk('.'):
        for filename in filenames:
            if '.tex' in filename and filename != BOOK_MAIN:
                latexFiles.append(path.relpath(path.join(dirpath, filename)))
    return latexFiles

def getVariableDeclaration(values, name):
    """Returns a Makefile variable declaration from the provided list"""
    declaration = ''
    for value in values:
        declaration += f'{name}+={value}\n'
    return declaration

def getSimpleRules(targets, prerequisites, formatString=None, generator=None):
    """Generates rules for creating targets from the prerequisites."""
    if not len(targets) == len(prerequisites):
        raise ValueError('The lengths of the two arrays should be the same!')
    if not formatString and not generator:
        raise ValueError('Must pass either a generator or a format string!')

    rules = ''
    for index in range(0, len(targets)):
        if generator:
            rules += generator(targets[index], prerequisites[index])
        else:
            rules += formatString.format(targets[index], prerequisites[index])
    return rules

def getBookRule(bookOutput, bookMain):
    """Obtain a rule for generating the whole book file."""
    return PDF_RULE_FORMAT.format(bookOutput, bookMain)

def getPageData(filename):
    """Obtain the page data for a filename (specified in makefile_config)"""
    if filename in PAGE_DATA:
        return ','.join([f'{k}={v}' for k, v in PAGE_DATA[filename].items()])
    return ''

def verifyBookMain(bookMain, latexFiles):
    """Verifies that the bookMain file contains all other latexFiles."""
    if not bookMain:
        return []
    with open(bookMain, 'r') as bookMainFile:
        bookText = ''.join(bookMainFile.readlines())
        unincludedFilenames = []
        for latexFile in latexFiles:
            if f'\\subfile{{{latexFile.replace(".tex", "")}}}' not in bookText:
                unincludedFilenames.append(latexFile)
        return unincludedFilenames

def getVariables(latexFiles):
    """Generate the makefile's variable declarations"""
    makefile = ''
    makefile += getVariableDeclaration(latexFiles, 'latexFiles') + '\n'

    pdfFiles = [path.join('pdf', string.replace('.tex', '.pdf'))
                if string != INDEX else path.join('pdf', 'index.pdf')
                for string in latexFiles]
    makefile += getVariableDeclaration(pdfFiles, 'pdfFiles') + '\n'

    htmlFiles = [string.replace('.tex', '.html') if string != INDEX
                 else 'index.html' for string in latexFiles]
    makefile += getVariableDeclaration(htmlFiles, 'htmlFiles') + '\n'

    erbFiles = [path.join('source', name + '.erb') for name in htmlFiles]
    makefile += getVariableDeclaration(erbFiles, 'erbFiles')
    return (makefile, pdfFiles, htmlFiles, erbFiles)

def getRules(latexFiles, pdfFiles, htmlFiles, erbFiles):
    """Generate the makefile's rules"""
    makefile = ''
    if BOOK_MAIN:
        makefile += BUILD_RULE.format(BOOK_OUTPUT, '/' + BOOK_OUTPUT)
        makefile += getBookRule(BOOK_OUTPUT, BOOK_MAIN)
    else:
        makefile += BUILD_RULE.format('', '')

    # Write the PDF, HTML, ERB rules
    makefile += getSimpleRules(pdfFiles, latexFiles,
                               formatString=PDF_RULE_FORMAT)
    makefile += getSimpleRules(htmlFiles, latexFiles,
                               formatString=HTML_RULE_FORMAT)
    generator = lambda tgt, pre: ERB_RULE_FORMAT.format(
        tgt, pre, getPageData(pre))
    makefile += getSimpleRules(erbFiles, htmlFiles, generator=generator)

    makefile += DEPLOY_RULE
    makefile += CLEAN_RULE
    return makefile

def main():
    latexFiles = getLatexFiles()
    for unincludedFilename in verifyBookMain(BOOK_MAIN, latexFiles):
        if unincludedFilename not in BOOK_EXCLUDE:
            warn(f'{unincludedFilename} not in {BOOK_MAIN} and not excluded '
                 + 'in makefile_config.py')
    with open('Makefile', 'w') as makefile:
        makefile.write(PREAMBLE.format(datetime.now()) + '\n')
        variables, pdfFiles, htmlFiles, erbFiles = getVariables(latexFiles)
        makefile.write(variables)
        makefile.write(getRules(latexFiles, pdfFiles, htmlFiles, erbFiles))

if __name__ == '__main__':
    main()

###############################################################################
