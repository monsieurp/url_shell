#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cmd, sys, os
import urllib.request as urllib2
from urllib.error import URLError

class ParseHeaders(cmd.Cmd):
    def __init__(self):
        """Initialise the shell. """
        cmd.Cmd.__init__(self)

        # Shell prompt.
        self.prompt = '% '

        # Small intro about the script when starting the shell.
        self.intro = "Welcome to %s !\n\n" % os.path.basename(sys.argv[0])
        self.intro = self.intro + "Go ahead and set up an URL you'd like to query headers\n"
        self.intro = self.intro + "and/or get the raw HTTP via the `set_url' function.\n"
        self.intro = self.intro + "Once done, query the URL with the `query_url` function.\n"
        self.intro = self.intro + "Eventually, use `print_httpheaders' or `print_rawpage'.\n\n"
        self.intro = self.intro + "Looking for help? Type `help'.\n"

        # Default URL.
        self.url = 'http://apila.fr'

        # No HTTP response created (yet).
        self.httpresponse = None

        # This will be a dictionary to store info about the URL.
        self.httpinfo = {}

    def do_set_url(self, line):
        """Set URL to fetch headers from. """
        if line is '' or line is None:
            print("usage: set_url <URL>")
            return
        self.url = line
        print("OK! URL set to [%s]" % self.url)

    def do_print_url(self, line):
        """Print URL to fetch headers from. """
        if self.is_url_empty(): return
        print("URL to query: [%s]" % self.url)

    def do_query_url(self, line):
        """Query URL stored with `set_url' function and retrieve content, if possible."""
        if self.is_url_empty(): return
        try:
            sys.stdout.write("Querying ..")
            self.httpresponse =  urllib2.urlopen(self.url)
            print(". OK!")
            print("HTTP response succesfully retrieved!")
            self.create_dt_from_response()
        except (URLError, ValueError) as e:
            print(". Error!\nCouldn't query URL [%s]" % self.url)
            print("Try with 'http://'.")

    def do_print_rawpage(self, line):
        """Print raw page. """
        if self.is_url_empty(): return
        print(self.httpinfo['rawpage'])

    def do_print_headers(self, line):
        """Print HTTP headers. """
        if self.is_url_empty(): return
        title = "# HEADERS #"
        banner = "#" * len(title)
        print("\n%s\n%s\n%s\n" % (banner, title, banner))
        for k, v in self.httpresponse.headers.items():
            print("%s: %s" % (k, v))

    def do_print_httpmsg(self, line):
        """Print HTTP message. """
        if self.is_url_empty(): return
        print(self.httpinfo['msg'])

    def do_EOF(self, line):
        """End the shell session with ^D. """
        return -1

    def do_exit(self, line):
        """End the shell session. """
        return -1

    def is_url_empty(self):
        """ Check for URL. """
        check = (self.url == '')
        if check:
            print("Set an URL first with the `set_url' function")
            print("and query it with `query_url'.")
        return check

    def create_dt_from_response(self):
        """ Set up appropriate datastructures in self.httpinfo. """
        self.httpinfo['headers'] = dict(self.httpresponse.headers)
        self.httpinfo['rawpage'] = self.httpresponse.read().decode('utf-8')
        self.httpinfo['msg'] = '%s %s' % (self.httpresponse.code, self.httpresponse.msg)

if __name__ == '__main__':
    ParseHeaders().cmdloop()
