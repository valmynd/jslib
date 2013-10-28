The goal of this project is to be able to use parts of the Javascript Standard libraries in Python.

# Why?

Python is the preferred choice for many developers, but when it comes to client side web development,
Javascript has to be used in one way or another (since Javascript is the only language Web Browsers understand).

Having to maintain seperate codebases for the frontend and the backend of a webapplication, often
doing many things in the exact same way (like validating User Input or manipulating HTML/XML/etc.), can be
a big pain in the neck and there are several approaches to avoid such redundancy:

1. Shared-Nothing Approach (not always feasible)
2. Use Javascript for everything (having to live with its flaws)
3. Use Python for everything (translating Python to Javascript)

People who like Python and dislike Javascript are likely to prefer the last approach and fortunately, there are many projects trying
to achieve this ([Here is a nice article comparing them](http://blog.pyjeon.com/?p=301)).

Some of those projects even try to bring parts of the Python Standard Libraries to Javascript, making it possible
to share even more code between client and server. The obvious flaw of this is, that more Javascript code needs to be transferred to
the client and it will cost some performance.

By doing the opposite, using the Javascript libraries in Python, this could be avoided, and you can still
use the exact same code on the client as on the server.

# Status

Currently, this is only proof-of-concept, some parts of it were not tested thoroughly.

One thing that was better tested and might come handy is the Date class.

# Requirements

For using the date class you need pytz, tzlocal and dateutil:

	pip install pytz
	pip install tzlocal
	pip install dateutil
