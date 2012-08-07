import feedparser  # Used to read my dropbox feed

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

d = feedparser.parse('https://www.dropbox.com/666641/13750534/1858cad/events.xml')
for i in d.entries:
    print "On", i.published, strip_tags(i.summary),
    # Outputs lines similar to below:
    # On Wed, 25 Jul 2012 18:13:35 GMT In DROPBOXFOLDERTEST, You edited the file thisisatestfile.txt.


