###############################################################################
# NAME:             makefile_config.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      Configuration file for GenerateMakefile.py script.
#                   PAGE_DATA: This can be used to add additional page data to
#                       the yaml header in the ERB template files. The keys are
#                       paths of generated html files, the values are dicts
#                       which contain key/value pairs for data to add.
#                   INDEX: The path of the latex file which generates the
#                       index.html.
#                   BOOK_MAIN: The latex file that imports all subfiles for the
#                       totality of the book.
#                   BOOK_EXCLUDE: A list of files that won't be included in the
#                       book, so don't warn if we find they're not in the book.
#
# CREATED:          07/25/2020
#
# LAST EDITED:      07/26/2020
###

import os

PAGE_DATA = {
    'Professional/Resume-Style1.html': {'stylesheet': 'resume'},
    'Professional/Resume-Style2.html': {'stylesheet': 'resume'},
}

INDEX = 'Introduction.tex'

BOOK_MAIN = 'BookMain.tex'
BOOK_OUTPUT = os.path.join('pdf', 'EthanRepository.pdf')
BOOK_EXCLUDE = [
    'Professional/Resume-Style1.tex',
    'Professional/Resume-Style2.tex',
    'Professional/InterviewQuestions.tex',
]

###############################################################################
