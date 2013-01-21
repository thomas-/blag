#!/usr/bin/env python

#
# tuomas.co.uk
# 

import sys
import os
import time
import markdown
import argparse
import datetime
import glob
from distutils import dir_util
from subprocess import call
from jinja2 import Template, Environment, FileSystemLoader

TIME_START = datetime.datetime.now()

EDITOR = os.environ.get('EDITOR', 'vim')

root = os.path.dirname(os.path.realpath(__file__))
output = os.path.join("public")
loc_posts = "posts"
theme = "default"
env = Environment(loader=FileSystemLoader(
        os.path.join(root,"themes",theme)))
 

def get_path(x):
    return os.path.dirname(os.path.realpath(x))

def scan_posts(dir):
    scan = os.path.join(root,dir)
    paths = []
    for item in os.listdir(scan):
        try:
            paths.append(os.path.join(root,dir,item))
        except StandardError, e:
            log(e)
    return paths

def md(text):
    return markdown.markdown(text,['fenced_code', 'codehilite'])

def parse_post(str):
    post = {}
    str = str.split('---',1)
    header = filter(None, str[0].split('\n'))
    post['content'] = md(str[1])
    for h in header:
        h = h.split(': ',1)
        if 'tags' in h[0] or 'description' in h[0]:
            h[1] = [x.strip() for x in h[1].split(',')]
        post[h[0]] = h[1]
    return post

        

def get_post_data(paths):
    content = "content.md"
    posts = []
    for path in paths:
        p = os.path.basename(path).split("_")
        try:
            posts.append({'slug': p[1],
                'path': path,
                'date': p[0]})
        except StandardError:
            log("ERROR: something wrong with post: "
                + os.path.basename(path))
    for i, post in enumerate(posts):
        with open(posts[i]['path']) as f:
            
            posts[i].update(parse_post(f.read()))
            date = posts[i]['date']
            posts[i]['time'] = datetime.date(int(date[0:4]),
                int(date[4:6]),
                int(date[6:8]))


    return posts

def generate_posts(posts,out):
    template = env.get_template('post.htm')
    for i, p in enumerate(posts):
        data = posts[i]
        data['title'] = p['title']
        path = os.path.join(out,p['slug']+".htm")
        f = open(path, 'w')
        f.write(template.render(data))
        f.close()

def generate_index(posts,out):
    data = {}
    data['posts'] = posts
    template = env.get_template('list.htm')
    path = os.path.join(out,"index.htm")
    f = open(path, 'w')
    f.write(template.render(data))
    f.close()
#   print template.render(data)

def generate_tags(posts,out):
    tags = {}
    for i, p in enumerate(posts):
        for tag in posts[i]['tags']:
            tags.setdefault(tag, []).append(i)
    template = env.get_template('list.htm')
    for tag in tags:
        data = {}
        data['posts'] = []
        for x in tags[tag]:
            data['posts'].append(posts[x])
            
        path = (os.path.join(out,"tag-"+tag.replace(" ","-")+".htm"))
        f = open(path, 'w')
        f.write(template.render(data))
        f.close()

        

def design(theme,out):
    call(['lessc', os.path.join('themes',theme,'style.less'), 
       os.path.join(out,'style.css')])
    dir_util.copy_tree(
            os.path.join('themes',theme,'assets'),
            os.path.join(out,'assets'))

def new_post(slug,path):
    if glob.glob(os.path.join(root,path,"*_"+slug+".md")):
        log("Post with slug "+slug+" already exists.")
    else:
        filepath = os.path.join(root,path,
                time.strftime("%Y%m%d")+"_"+slug+".md")
        with open(filepath,"w") as f:
            f.write("title: \ntags: \nkeywords: \ndescription: \n--- \n\nContent \n")
            f.close()
            call([EDITOR, filepath])
            log("New Post: "+filepath)

def delete_post(slug,path):
    matches = glob.glob(os.path.join(root,path,"*"+slug+"*.md"))
    if len(matches) is 0:
        log("No posts found matching string")
        return
    for p in matches:
        print "Are you sure you want to delete "+p+"? [y/N]"
        x = raw_input()
        if x is 'Y' or x is 'y':
            try: os.remove(p)
            except IOError, e: 
                log(e)
                continue
            print "Deleted "+p

def edit_post(slug,path):
    matches = glob.glob(os.path.join(root,path,"*"+slug+"*.md"))
    if len(matches) is 1:
        call([EDITOR, matches[0]])
    elif len(matches) > 1:
        log("Too many matches, be more specific:")
        print matches
    elif len(matches) is 0:
        log("No post found matching that string")

def log(s):
    print s

def log_time(s):
    TIME_NOW = (datetime.datetime.now() - TIME_START).microseconds/1000
    print "[" + str(TIME_NOW)+"ms] - " + s

def what_do():
    parser = argparse.ArgumentParser(description='static blog generator')
    parser.add_argument('command', type=str)
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = vars(parser.parse_args())
    cmd = args['command']

    if 'build' in cmd:
        build()
    elif 'new' in cmd:
        new_post(args['args'][0],loc_posts)
    elif 'edit' in cmd:
        edit_post(args['args'][0],loc_posts)
    elif 'delete' in cmd:
        delete_post(args['args'][0],loc_posts)
    elif 'help' in cmd:
        log("help!")
    else:
        log("ERROR: unknown command "+cmd)

class COLOR:
    CLEAR = '\033[2J'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'

def path_from_slug(slug):
    return glob.glob(os.path.join(root,loc_posts,"*_"+slug))[0]
    
def build():
    if not os.path.exists(output):
        os.makedirs(output)

    posts = get_post_data(scan_posts(loc_posts))
    log_time("scanned posts")

    generate_posts(posts,output)
    log_time("generated posts")

    generate_index(posts,output)
    log_time("generated index")

    generate_tags(posts,output)
    log_time("generated tags")

    design(theme,output)
    log_time("done!")

def main():
    what_do()

if __name__ == "__main__":
    main()


