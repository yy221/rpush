#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      chliu
#
# Created:     30/04/2013
# Copyright:   (c) Administrator 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from datetime import date
import feedparser
import os
import os.path
import codecs

allurl = [
"http://blogs.msmvps.com/?feed=rss2" ,
"http://www.newsmth.net/rssi.php?h=1" ,
"http://www.36kr.com/feed" ,
"http://cn.engadget.com/rss.xml" ,
"http://www.hexblog.com/?feed=rss2" ,
"http://www.nooidea.com/feed" ,
"http://syndication.thedailywtf.com/TheDailyWtf" ,
"http://shixian.net/?feed=rss2" ,
"http://www.aqee.net/feed/" ,
"http://it.oyksoft.com/feed.php" ,
"http://feed.feedsky.com/programmer" ,
"http://www.ifanr.com/feed" ,
"http://www.huxiu.com/rss/0.xml" ,
"http://www.huxiu.com/rss/1.xml" ,
"http://www.huxiu.com/rss/4.xml" ,
"http://www.huxiu.com/rss/6.xml" ,
"http://www.matrix67.com/blog/feed.asp" ,
"http://blog.k-tai-douga.com/index.rdf" ,
"http://feed.feedsky.com/2maomao" ,
"http://feed.feedsky.com/programlife" ,
"http://blog.csdn.net/v_JULY_v/rss/list" ,
"http://www.joelonsoftware.com/rss.xml" ,
"http://blog.codingnow.com/atom.xml" ,
"http://blog.jobbole.com/feed/" ,
"http://feed.feedsky.com/valleytalk" ,
"http://blog.sina.com.cn/rss/1569777711.xml" ,
"http://blog.sina.com.cn/rss/1547596314.xml" ,
"http://xieguozhong.blog.sohu.com/rss" ,
"http://coolshell.cn/feed" ,
        ]

def main():

    t = date.today()
    old_feedurl = 'd:/feed_%d%02d%02d.html' %(t.year, t.month, t.day )
    feedurl = 'd:/feeds.html'
    print feedurl

    if ( os.path.exists ( feedurl)) :
        os.rename ( feedurl, old_feedurl );

    feedfile = codecs.open (feedurl, 'w', 'utf-8' )

    feedfile.write('<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head><body>')

    for url in allurl:

        try:
            d = feedparser.parse (url)
            title = d['feed']['title']
            feedfile.write ( "<p>TITLE:<B>%s</B></p>" %(title) )
            for entry in d.entries:
                feedfile.write ( '<p><a href="%s">%s</a></p>' %(entry.link, entry.title))
        except:
            print "exception:%s" %(url)

    feedfile.write ( '</body></html>' )
    feedfile.close()


if __name__ == '__main__':
    main()
