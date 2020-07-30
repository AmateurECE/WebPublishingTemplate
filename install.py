###############################################################################
# NAME:             install.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      Installs the template
#
# CREATED:          07/26/2020
#
# LAST EDITED:      07/29/2020
###

# Procedure for the next couple of days:
# 2. repository book copyright/publishing page
# 4. Set up the django index app (display an index page that routes the user
#    to different places on the server)
# 7. Get LDAP and the index app running with groups

def getParameter(message):
    """Obtain a parameter from the user with the message"""
    return input(f'Please enter {message}: ')

TEMPLATE_FILES = ['deployment-site.conf', 'GenerateMakefile.py']
REPLACE_KEYS = {
    'THE_LOCATION': getParameter('the location name of this publication'),
}

def main():
    for filename in TEMPLATE_FILES:
        with open(filename, 'r') as inputFile:
            inputFileContent = inputFile.readlines()

        with open(filename, 'w') as outputFile:
            for line in inputFileContent:
                for key, value in REPLACE_KEYS.items():
                    line = line.replace(key, value)
                outputFile.write(line)

if __name__ == '__main__':
    main()

###############################################################################
