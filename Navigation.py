###############################################################################
# NAME:             Navigation.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      This script generates the navigation data for the layout.
#
# CREATED:          07/18/2020
#
# LAST EDITED:      07/31/2020
###

import os
import argparse
from bs4 import BeautifulSoup

NAV_PROLOGUE = """
<nav>
  <div class="menu-wrap">
    <input class="toggler" name="" type="checkbox" value=""/>
    <div class="hamburger"><div></div></div>
    <div class="menu">
      <div>
        <ul>
"""
BOOK_LINK = """
          <li>
            <p class="nav-book-link-text">Like these articles? Download nearly
            the whole technical content of the website in PDF form
            <a class="nav-book-link" href="{}">here</a>.</p>
          </li>
"""
NAV_EPILOGUE = """
        </ul>
      </div>
    </div>
  </div>
  <div class="brand"></div>
  <ul class="button-header">
    <li><a class="button" href="/">Home</a></li>
    <li><a class="button" href="<%= current_page.data.pdfLink %>"><div>
      <div id="downloadIcon"></div></div></a></li>
  </ul>
</nav>
"""

def getTitleFromHtml(htmlFilePath):
    """Obtains the title from the LaTeX document"""
    with open(htmlFilePath, 'r') as htmlFile:
        soup = BeautifulSoup(htmlFile, 'html.parser')
        if not soup.title or not soup.title.text:
            raise RuntimeError(f'{htmlFilePath} does not specify a title!')
        return soup.title.text

def getLinkFromHtml(filename):
    """Obtain the link from the file path of the TeX file"""
    link = '/'
    if filename != 'index.html':
        link += filename.replace('.html', '/')
    return link

def getNavigationItem(link, title):
    """Obtain a navigation item"""
    attributeData = {'href': link}
    attributes = ' '.join(
        [f'{key}="{val}"' for key, val in attributeData.items()])
    return f'            <li class=""><a {attributes}>{title}</a></li>\n'

def getFolders(titles):
    """Split the pages down into folders"""
    folders = {}
    for link, title in titles.items():
        parts = os.path.split(link[:-1])
        if len(parts) > 2:
            raise RuntimeError('Too many layers of folders.')
        elif len(parts) == 1:
            if 'default' not in folders:
                folders['default'] = {}
            folders['default'][parts[0]] = {'link': link, 'title': title}
        else:
            folderName = parts[0][1:]
            if folderName not in folders:
                folders[folderName] = {}
            folders[folderName][parts[1]] = {'link': link, 'title': title}
    return folders

def getNavigation(titles, book=''):
    """Obtain the markup for the navigation"""
    navigation = NAV_PROLOGUE
    folders = getFolders(titles)
    for folder in folders:
        if folder != 'default':
            navigation += ('          <ul class="folder">\n'
                           + f'            <h5>{folder}</h5>\n')
        for entry in folders[folder]:
            data = folders[folder][entry]
            navigation += getNavigationItem(data['link'], data['title'])
        if folder != 'default':
            navigation += '          </ul>\n'

    if book:
        navigation += BOOK_LINK.format('/' + book)
    return navigation + NAV_EPILOGUE

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--book', '-b',
        help=('The path of the collected works of this repository--this file'
              ' is treated specially'), default='')
    parser.add_argument(
        '--output', '-o',
        help=('The path of the file to which to write the navigation data'),
        default=os.path.join('source', '_navigation.erb'))
    parser.add_argument(
        'htmlFiles', help=('The HTML files for which to generate navigation'),
        nargs='*')
    arguments = parser.parse_args()

    titles = dict(zip(
        [getLinkFromHtml(htmlFile) for htmlFile in arguments.htmlFiles],
        [getTitleFromHtml(htmlFile) for htmlFile in arguments.htmlFiles]))
    with open(arguments.output, 'w') as outputFile:
        outputFile.write(getNavigation(titles, arguments.book))

if __name__ == '__main__':
    main()

###############################################################################
