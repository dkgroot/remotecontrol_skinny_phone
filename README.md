Simple Proof of concept

ssh is a statically compiled version of dropbear dbclient program (make PROGRAMS="dropbear dbclient scp" MULTI=1 STATIC=1).
Most of the cisco phones come with an older version of dropbear which is not
compatible to the openssh client.

phonelogger.py use pexpect to log into the phone via ssh. 
It sets the phone to produce certain debugging which we are interested in.
After that it switches to strace mode, and filters the events we want to
register a callback for

pushphone.py shows how to use python to push an http/xml message to the
phone.

satisfy the requirements using:
sudo pip3 install -f requirements.txt

