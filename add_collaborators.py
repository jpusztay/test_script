from optparse import OptionParser
import csv
parser = OptionParser()

parser.add_option('--repo', action='store', type = 'string',
                  default = '',
                  dest='repo',
                  help='The repo to add collaborators to.')

parser.add_option('--un', action='store', type= 'string',
                  default = '',
                  dest='un',
                  help='Your github username')

parser.add_option('--apitoken', action='store', type = 'string',
                  default = '',
                  dest='apitoken',
                  help='GitHub API Token')

parser.add_option('--userNameList', action ='store', type = 'string',
                 default ='',
                 dest='userNameList',
                 help= "The csv containing all github usernames to add as collaborators.")
parser.add_option('--csvcoord', action = 'store', type = 'int',
                  default = 0,
                  dest = 'csvcoord',
                  help = 'The column coordinate location of the username for the git collaborator in collaborators csv file')
                 
(options, args) = parser.parse_args()

if (options.un == '' or options.apitoken == '' or options.repo == '' or options.userNameList == ''):
    print "you done goofed, check your inputs."
    quit()


import urllib2
import base64
import os
USER=options.un
API_TOKEN=options.apitoken
GIT_API_URL='https://api.github.com'

def get_api(url, added_user):
    try:
        request = urllib2.Request(GIT_API_URL + url)
        base64string = base64.encodestring('%s/token:%s' % (USER, API_TOKEN)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.get_method = lambda: 'PUT'
        result = urllib2.urlopen(request)
        print result.read()
        result.close()
    except:
        print 'Failed to add above user as collaborator'
        try:
            f = open('FAILED.txt', 'a')
            f.write(added_user+'\n')
            f.close()
        except:
            f = open('FAILED.txt', 'w')
            f.write(added_user+'\n')
            f.close()

with open(options.userNameList, 'rb') as users:
    all_users = csv.reader(users, delimiter=',')
    try:
        os.remove('FAILED.txt')
    except OSError:
        pass
    for row in all_users:
        print 'adding user: ' + row[options.csvcoord]
        get_api('/repos/'+options.un+'/'+options.repo+'/collaborators/'+row[options.csvcoord], row[options.csvcoord])

print 'finished'

