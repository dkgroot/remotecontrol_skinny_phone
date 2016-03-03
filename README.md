Simple Proof of concept
=======================
ssh is a statically compiled version of dropbear dbclient program (make PROGRAMS="dropbear dbclient scp" MULTI=1 STATIC=1).
Most of the cisco phones come with an older version of dropbear which is not
compatible to the openssh client.

Example Phone Logger:
---------------------
phonelogger.py use pexpect to log into the phone via ssh. 
It sets the phone to produce certain debugging which we are interested in.
After that it switches to strace mode, and filters the events we want to
register a callback for

Usage: 
--------------------------------
phonelogger.py <hostname>
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -n USERNAME, --username=USERNAME
                        ssh username to connect to phone
  -p PASSWORD, --password=PASSWORD
                        ssh password to connect to phone
  -a SHELLUSER, --shelluser=SHELLUSER
                        shell username to login to the phone
  -b SHELLPASSWD, --shellpass=SHELLPASSWD
                        shell password to login to the phone
  -l LOGFILENAME, --logfile=LOGFILENAME
                        log ssh output to logfile

Push Request to Phone:
----------------------
pushphone.py shows how to use python to push an http/xml message to the phone.

Run Tests:
------
py.test-3 -s -v
py.test-3 -s -v -k test_call98011_2

Requirements:
-------------
python3
pexpect >= 3.1
requests >= 2.2.1
pytest >= 2.5.1  

You can satisfy these requirements using:
<code>
sudo pip3 install -f requirements.txt
</code>
