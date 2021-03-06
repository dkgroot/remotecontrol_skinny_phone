Simple Proof of concept
=======================
Example Phone Logger:
---------------------
phonelogger use pexpect to log into the phone via (dropbear)ssh. 
It sets the phone to produce certain debugging which we are interested in.
After that it switches to strace mode, and filters the events we want to
register a callback for

Usage: 
--------------------------------
<pre>
bin/phonelogger <hostname>
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
</pre>

Push Request to Phone:
----------------------
bin/pushphone shows how to use python to push an http/xml message to the phone.

Run Tests:
------
<pre>
py.test-3 -s -v
py.test-3 -s -v -k test_call98011_2
</pre>

Requirements:
-------------
<pre>
python3
dropbox ssh client called dbclient

pexpect >= 3.1
requests >= 2.2.1
pytest >= 2.5.1
</pre>

You can satisfy these requirements using:
<code>
sudo pip3 install -f requirements.txt
</code>

Note:
-----
Most of the cisco phones come with an older version of dropbear which is not
compatible to the openssh client.
For that reason i provided bin/dbclient which is a statically (x86_64) compiled version of dropbear ssh client
if you need a version for a different platform, you need to download the dropbear ssh package and run
<pre>
make PROGRAMS="dbclient" MULTI=1 STATIC=1
</pre>
to create a new version of dbclient as a replacement
