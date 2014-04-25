#chliu created 2013.05.02

import urllib
import urllib2
import codecs
import logging
import feedparser
import StringIO
#import webapp2
import cmdline.py
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.api.mail import EmailMessage

url_map = {
        '/tasks/weekly': [
"http://blog.codingnow.com/atom.xml" ,
"http://coolshell.cn/feed" ,
"http://www.ruanyifeng.com/blog/atom.xml" ],

        '/tasks/weekly2': [
# "http://www.matrix67.com/blog/feed.asp" ,
"http://feed.feedsky.com/aqee-net",
"http://feed.feedsky.com/programmer" ,
"http://feed.feedsky.com/valleytalk" ,
],

        '/tasks/weekly3': [
"http://www.huxiu.com/rss/0.xml" ,
"http://www.huxiu.com/rss/1.xml" ,
"http://www.huxiu.com/rss/4.xml" ,
"http://www.huxiu.com/rss/6.xml"  ],

        '/tasks/weekly4': [
"http://blog.jobbole.com/feed/" ,
"http://www.joelonsoftware.com/rss.xml" ,
"http://syndication.thedailywtf.com/TheDailyWtf"  
# "http://shixian.net/?feed=rss2" ,
],

        '/tasks/weekly5': [
"http://www.36kr.com/feed" ,
"http://www.ifanr.com/feed" ,
"http://feeds.feedburner.com/Torrentfreak",
# "http://cn.engadget.com/rss.xml" 
]
        }

def parseFeed (f, url):
    try:
        d = feedparser.parse (url)
        title = d['feed']['title']
        f.write ( '<p>TITLE:<a href="%s"><B>%s</B></a></p>' %(url, title) )
        for entry in d.entries:
            f.write ( '<p><a href="%s">%s</a></p>' %(entry.link, entry.title))
    except:
        f.write( '<p>exception:%s</p>' %(url) )

def sendMail (ctx):
    # logging.info (ctx)

    kw = {}
    kw['sender'] = 'qsoft9@gmail.com'
    kw['to'] = 'rpush@qq.com'
    kw['subject'] = 'daily rss feeds'
    kw['body'] = ' '
    kw['html'] = ctx

    mail = EmailMessage (**kw);
    mail.send ();

    """
    mail.send_mail(sender='qsoft9@gmail.com',
              to='rpush@qq.com',
              subject='daily rss feeds',
              body=ctx
              #,html=ctx
              )
    """
class TwitterCallback(webapp.RequestHandler):
    def get(self):
        logging.info ('TwitterCallback %s' %(self) )
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write ('ok: %s' %(self.request.path) );

class TwitterPush (webapp.RequestHandler):
    def get(self):
        logging.info ('TwitterPush %s' %(self) )
        ioctx = StringIO.StringIO();

        try:
            ret = twitter_main ():
            ioctx.write ( '%s' %(ret) )
        except:
            ioctx.write( 'exception found.' )

        sendMail ( ioctx.getvalue() )
        ioctx.close()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write ('send mail ok: %s' %(self.request.path) );

#just for simple pass GFW to get one html page !
class OncePage(webapp.RequestHandler):
    def get(self):
	'''
        req = urllib2.Request ( 'http://projecteuler.net/show=all' );
        req.add_header ( 'User Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)');
        resp = urllib2.urlopen ( req )

        ioctx = StringIO.StringIO();
        ctx = resp.read ()
        ioctx.write ( ctx )
        sendMail ( ioctx.getvalue() )
        ioctx.close()
		'''

class TaskPage(webapp.RequestHandler):
    def get(self):
        ioctx = StringIO.StringIO();
        ioctx.write('<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head><body>')

        allurl = url_map[self.request.path]
        for url in allurl:
            parseFeed( ioctx, url );
        # ioctx.write ( 'test cron ok' )
        ioctx.write ( '</body></html>' )
        sendMail ( ioctx.getvalue() )
        ioctx.close()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write ('send mail ok: %s' %(self.request.path) );

class MainPage(webapp.RequestHandler):
    def get(self):

        user = users.get_current_user()
        if user and 0 == cmp( user.nickname(), "rpush@qq.com"):
            # self.response.out.write ( user.nickname() );
            self.response.headers['Content-Type'] = 'text/html'

            f = self.response.out
            #feedfile = codecs.open ('feeds.html', 'r', 'utf-8' )
            # f.write ( feedfile.read() )
            f.write ( '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head><body>push ok %s</body></html>'  %(self.request.path ) )

        else:
            self.redirect(users.create_login_url(self.request.uri))


application = webapp.WSGIApplication( [
    ('/', MainPage),
    ('/tasks/weekly', TaskPage ),
    ('/tasks/weekly2', TaskPage  ),
    ('/tasks/weekly3', TaskPage  ),
    ('/tasks/weekly4', TaskPage  ),
    ('/tasks/weekly5', TaskPage  ),
    ('/tasks/once', OncePage  ),
    ('/t_callback', TwitterCallback  ),
    ('/t', TwitterPush  ),
    ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

