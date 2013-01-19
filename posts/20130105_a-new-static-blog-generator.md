title: A New Static Blog Generator
tags: meta, python
keywords: web, blog, blag, static generator
description: a post about my static blog generator
---

I decided that a statically generated blog was the way to go
for a couple of major reasons: 

* writing in vim is much more painless than an online editor
* having git handle version control is a no brainer
* portability

At writing, the blog is around 100 lines of python, making extensive use
of the *jinja2* and *markdown* libraries. I use [LESS][] to compile
a stylesheet and [jquery.timeago][] for readable timestamps.
It was hacked together over the course of only a few hours
(including frontend) with very little python
experience. There are many established generators I could've used
but honestly I'd rather roll my own in a few lines of python
than try to  make other engines do what I want to do.

One of those things I want to do is comments - it is argued that
[static site generators are harmful][harmful to oss] to the FOSS
community as most will turn to *Disqus* to handle commenting... something
I just don't want to do, I think there has to be a better way.

I also want to make my script a nice cli "dashboard" if you will.
I'd like to be able to type something like `blog.py edit "static blog"`
and have it fire me into `vim` ready to go. I think this is something
many static blog engines lack though it would be a useful interface to have.
Right now my focus is on improving the current codebase, an example
of some the less than beautiful code written so far:

~~~.python
'time': datetime.date(int(post.date[0:4]),
                int(post.date[4:6]),
                int(post.date[6:8]))
~~~

This engine is definitely a work in progress and far from release.
If you think ruby sucks, or that javascript is ugly, 
or hyde and pelican are too much then you should probably
use [Obraz][] instead of waiting for me to pull my finger out
because it looks quite good and is honestly what I'm heading towards.

Why write yet another static site generating blog engine?
Well that's just begging for the obligatory xkcd....

[![Obligatory xkcd...](http://imgs.xkcd.com/comics/standards.png)](http://xkcd.com/927/)





[harmful to oss]: http://www.jeremyscheff.com/2011/08/jekyll-and-other-static-site-generators-are-currently-harmful-to-the-free-open-source-software-movement/
[LESS]: http://lesscss.org
[Obraz]: http://obraz.pirx.ru/
[jquery.timeago]: http://timeago.yarp.com
