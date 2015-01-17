#! /usr/bin/env python

from download.coursera.coursera.coursera_dl import *

args = parseArgs()


session = requests.Session()

if args.preview:
    # Todo, remove this.
    session.cookie_values = 'dummy=dummy'
else:
    get_cookies_for_class(
        session,
        args.class_names[0],
        cookies_file=args.cookies_file,
        username=args.username, password=args.password
    )
    session.cookie_values = make_cookie_values(session.cookies, args.class_names[0])

# get the syllabus listing
page = get_syllabus(session, args.class_names[0], args.local_page, args.preview)


sections = parse_syllabus(session, page, args.reverse,
                              args.intact_fnames)
