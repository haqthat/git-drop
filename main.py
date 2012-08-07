import feedparser  # Used to read my dropbox feed
import envoy # run git commands
import argparse, os, logging

from HTMLParser import HTMLParser


class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


# Function to strip the html out of each "event" in the RSS feed.


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# Parse the feed, store in d

def parseFeed():
    d = feedparser.parse('https://www.dropbox.com/666641/13750534/1858cad/events.xml')
    for i in d.entries:
        print "On", i.published, strip_tags(i.summary),
        # Outputs lines similar to below:
        # On Wed, 25 Jul 2012 18:13:35 GMT In DROPBOXFOLDERTEST, You edited the file thisisatestfile.txt.

logger = logging.getLogger('git-drop')
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(Mainessage)s',
        datefmt='%m-%d %H:%M',
        filename='/var/log/git-drop.log',
        filemode='a')

def main(infiles, indir):
    """Main method takes list of input files and creates a git commit, getting the username from dropbox."""
    os.chdir(indir)
    cmd = "git add {0}".format(infiles)
    r = envoy.run(cmd)
    if r.status_code > 0:
        logger.error("Problem with cmd: {0}".format(cmd))
        logger.error("Status code: {0}\nStdErr: {1}\nStdOut: {2}".format(r.status_code, r.std_err, r.std_out))

    # function call here to return the username
    # user = getUser()
    user = "me <me@example.com>" # author syntax may be incorrect
    cmd = 'git commit --author={0} -m "these files were changed by some user"'.format(user)
    r = envoy.run(cmd)
    if r.status_code > 0:
        logger.error("Problem with cmd: {0}".format(cmd))
        logger.error("Status code: {0}\nStdErr: {1}\nStdOut: {2}".format(r.status_code, r.std_err, r.std_out))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='git-drop script to commit changes from dropbox', version='%(prog)s 1.0')
    parser.add_argument('infiles', nargs='+', type=str, help='input files')
    parser.add_argument('--dir', type=str, default='', help='directory of git project')
    args = parser.parse_args()
    main(args.infiles, args.dir)
