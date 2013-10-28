import xml.dom.minidom as dom
import math
import collections
import random
import sys
import datetime
import re

__author__ = "C. Wilhelm"
___license___ = "The MIT License (MIT)"

# Javascript Global Objects
# https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects


class Object(object):
	def __init__(self, value=None):
		self.value = value

	@property
	def length(self):
		return self.__len__() # always override __len__(), not length, in subclasses of Object

	def toString(self):
		return String(self.__str__()) # preferably override __str__(), not toString(), in subclasses of Object

	def toLocaleString(self):
		return self.toString()

	def valueOf(self):
		return self.value

	def hasOwnProperty(self, prop):
		return hasattr(self, prop)

	def isPrototypeOf(self, obj):
		return isinstance(obj, self)

	def propertyIsEnumerable(self, prop):
		return isinstance(prop, collections.Iterable)

	def __getitem__(self, key):
		return object.__getattribute__(self, key)

	def __setitem__(self, key, value):
		object.__setattr__(self, key, value)

	def __repr__(self):
		return self.__class__.__name__ + "(" + self.value.__repr__() + ")"


class Array(Object):
	# TODO: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach
	def __init__(self, *items):
		Object.__init__(self, items)
		self._list = list(items)

	def __len__(self):
		return len(self._list)

	def __repr__(self):
		return "Array(" + self._list.__repr__() + ")"

	def concat(self, *items):
		concatitems = self._list[:] + list(items)
		return Array(*concatitems)

	def join(self, seperator=""):
		return seperator.join(self._list)

	def pop(self):
		""" removes the last item from an array and returns that item """
		return self._list.pop()

	def push(self, *items):
		"""  appends the given element(s) and returns the new length of the array """
		self._list.extend(items)
		return len(self._list)

	def reverse(self):
		"""revers an array in place (first item becomes the last and vice versa); returns a reference to the array"""
		self._list.reverse()
		return self

	def shift(self):
		""" removes the first item from an array and returns that item """
		return self._list.pop(0)

	def slice(self, start, end=None):
		""" returns a shallow copy of a portion of an array """
		if end is None:
			return Array(*self._list[start:])
		return Array(*self._list[start:end])

	def sort(self, comparefunc=None):
		""" sorts the items in place and returns the array """
		if comparefunc is not None:
			self._list.sort(comparefunc)
			return self
		self._list.sort()
		return self

	def splice(self, index, howMany, *items):
		"""changes the content of an array, adding new items while removing
		old items; returns array containing the removed items """
		assert howMany == len(items)
		ret = Array()
		for i, item in enumerate(items):
			ret.push(self._list[i])
			self._list[i] = item
		return ret

	def unshift(self, *items):
		""" adds one or more items to the front of an array and returns the new length of the array """
		for item in reversed(items):
			self._list.insert(0, item)
		return len(self._list)


class Date(Object):
	def __init__(self, value=None, month=None, date=1, hours=0, minutes=0, seconds=0, milliseconds=0):
		"""
		Date(value) // -> integer representing a Unix Timestamp
		Date(dateString) // -> string representing an RFC2822 or ISO 8601 date
		Date(year, month, day [, hour, minute, second, millisecond])
		"""
		import pytz # pip install pytz
		import tzlocal # pip install tzlocal
		import dateutil.parser # pip install dateutil

		Object.__init__(self)
		if value is None:
			dt = datetime.datetime.now() # maybe non-standard, works in firefox and chrome, not tested in other browsers
		elif month is not None:
			dt = datetime.datetime(value, month, date, hours, minutes, seconds, milliseconds)
		elif isinstance(value, (int, float, Number)):
			dt = datetime.datetime.fromtimestamp(value)
		else:
			dt = dateutil.parser.parse(value)
		# http://stackoverflow.com/a/4771733/852994
		# http://stackoverflow.com/a/17363006/852994
		# http://stackoverflow.com/a/13287083/852994
		self.ltz = tzlocal.get_localzone()
		self.utz = pytz.utc
		self.ldt = self.ltz.localize(dt) if dt.tzinfo is None else dt.astimezone(self.ltz)
		self.udt = self.ldt.astimezone(self.utz)
		self.value = self.ltd

	@classmethod
	def UTC(cls, year, month, date=1, hours=0, minutes=0, seconds=0, milliseconds=0):
		""" Date.UTC uses universal time instead of the local time and returns a timestamp instead of a Date object """
		Date(year, month, date, hours, minutes, seconds, milliseconds).getTime()

	@classmethod
	def parse(cls, dateString):
		""" parses a string representation of a date, and returns the number of milliseconds since 1970, 00:00:00 UTC """
		return Date(dateString).getTime()

	def getTime(self):
		"""returns the number of milliseconds (!) since 1 January 1970 00:00:00 UTC"""
		return int(self.udt.timestamp() * 1000)

	def setTime(self, value):
		"""set the Date object to the time represented by a number of milliseconds (!) since 1970, 00:00:00 UTC"""
		dt = datetime.datetime.fromtimestamp(value / 1000) # datetime expects seconds, not milliseconds
		self.udt = dt.replace(tzinfo=self.utz)
		self.ldt = self.udt.astimezone(self.ltz)

	def getTimezoneOffset(self):
		"""
		time-zone offset from UTC, in minutes, for the current locale
		the offset is positive if the local timezone is behind UTC and negative if it is ahead!
		"""
		delta = self.ldt.utcoffset()
		return 0 if delta is None else int(delta.seconds / 60)

	def getDate(self):
		""" day of the month (1-31) for the specified date according to local time """
		return self.ldt.day

	def getDay(self):
		""" day of the week (0-6) for the specified date according to local time (0:=Monday, 6:=Sunday)"""
		return self.ldt.weekday()

	def getMonth(self):
		""" month (0-11) in the specified date according to local time (0:=January, 11:=December)"""
		return self.ldt.month - 1

	def getFullYear(self):
		""" year (4 digits, e.g. '2014') of the specified date according to local time """
		return self.ldt.year

	def getHours(self):
		""" hour (0-23) in the specified date according to local time """
		return self.ldt.hour

	def getMinutes(self):
		""" minutes (0-59) in the specified date according to local time """
		return self.ldt.minute

	def getSeconds(self):
		"""seconds (0-59) in the specified date according to local time """
		return self.ldt.second

	def getMilliseconds(self):
		""" milliseconds (0-999) in the specified date according to local time """
		return self.ldt.microsecond / 1000

	def getUTCDate(self):
		""" day (date) of the month (1-31) in the specified date according to universal time """
		return self.udt.day

	def getUTCDay(self):
		""" day of the week (0-6) for the specified date according to universal time (0:=Monday, 6:=Saturday)"""
		return self.udt.weekday()

	def getUTCMonth(self):
		""" month (0-11) in the specified date according to universal time (0:=January, 11:=December)"""
		return self.udt.month + 1

	def getUTCFullYear(self):
		""" year (4 digits, e.g. '2014') of the specified date according to universal time """
		return self.udt.year

	def getUTCHours(self):
		""" hour (0-23) in the specified date according to universal time """
		return self.udt.hour

	def getUTCMinutes(self):
		""" minutes (0-59) in the specified date according to universal time """
		return self.udt.minute

	def getUTCSeconds(self):
		"""seconds (0-59) in the specified date according to universal time """
		return self.udt.second

	def getUTCMilliseconds(self):
		""" milliseconds (0-999) in the specified date according to universal time """
		return self.udt.microsecond / 1000

	def setDate(self, value):
		self.ldt = self.ldt.replace(day=value)
		self.udt = self.ldt.astimezone(self.utz)

	def setMonth(self, value):
		"""month (0-11) (0:=January, 11:=December) -> other than in python's datetime!"""
		self.ldt = self.ldt.replace(month=value - 1)
		self.udt = self.ldt.astimezone(self.utz)

	def setFullYear(self, value):
		self.ldt = self.ldt.replace(year=value)
		self.udt = self.ldt.astimezone(self.utz)

	def setHours(self, value):
		self.ldt = self.ldt.replace(hour=value)
		self.udt = self.ldt.astimezone(self.utz)

	def setMinutes(self, value):
		self.ldt = self.ldt.replace(minute=value)
		self.udt = self.ldt.astimezone(self.utz)

	def setSeconds(self, value):
		self.ldt = self.ldt.replace(second=value)
		self.udt = self.ldt.astimezone(self.utz)

	def setMilliseconds(self, value):
		self.ldt = self.ldt.replace(microsecond=value * 1000)
		self.udt = self.ldt.astimezone(self.utz)

	def setUTCDate(self, value):
		self.udt = self.udt.replace(day=value)
		self.ldt = self.udt.astimezone(self.ltz)

	def setUTCMonth(self, value):
		"""month (0-11) (0:=January, 11:=December) -> other than in python's datetime!"""
		self.udt = self.udt.replace(month=value - 1)
		self.ldt = self.udt.astimezone(self.ltz)

	def setUTCFullYear(self, value):
		self.udt = self.udt.replace(year=value)
		self.ldt = self.udt.astimezone(self.ltz)

	def setUTCHours(self, value):
		self.udt = self.udt.replace(hour=value)
		self.ldt = self.udt.astimezone(self.ltz)

	def setUTCMinutes(self, value):
		self.udt = self.udt.replace(minute=value)
		self.ldt = self.udt.astimezone(self.ltz)

	def setUTCSeconds(self, value):
		self.udt = self.udt.replace(second=value)
		self.ldt = self.udt.astimezone(self.ltz)

	def setUTCMilliseconds(self, value):
		self.udt = self.udt.replace(microsecond=value * 1000)
		self.ldt = self.udt.astimezone(self.ltz)

	def toLocaleDateString(self):
		return self.toDateString()

	def toLocaleTimeString(self):
		return self.toTimeString()

	def toLocaleString(self):
		return self.toString()

	def toString(self):
		return String(self.ldt.strftime("%a, %d %b %Y %H:%M:%S %Z"))

	def toUTCString(self):
		"""Wed, 31 Dec 2008 23:00:00 GMT"""
		return String(self.udt.strftime("%a, %d %b %Y %H:%M:%S %Z"))

	def toDateString(self):
		"""date portion of a Date object in human readable form in American English; e.g. 'Thu Jan 01 2009'"""
		return String(self.ldt.strftime("%a %b %d %Y"))

	def toTimeString(self):
		"""date portion of a Date object in human readable form in American English; e.g. '00:00:00 GMT+0100 (CET)'"""
		return String(self.ldt.strftime("%H:%M:%S %Z"))

	def toISOString(self):
		"""YYYY-MM-DDTHH:mm:ss.sssZ; e.g. '2008-12-31T23:00:00.000Z'"""
		# https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString
		return String("%04d-%02d-%02dT%02d:%02d:%02d.%sZ" % (
			self.getUTCFullYear(),
			self.getUTCMonth() + 1,
			self.getUTCDate(),
			self.getUTCHours(),
			self.getUTCMinutes(), self.getUTCSeconds(),
			String(Number(self.getUTCMilliseconds() / 1000).toFixed(3)).slice(2, 5)
		))


class Math(Object):
	# all properties and methods of Math are static!
	E = math.e
	LN2 = math.log(2)
	LN10 = math.log(10)
	LOG2E = math.log(math.e, 2)
	LOG10E = math.log(math.e, 10)
	PI = math.pi
	SQRT1_2 = math.sqrt(1 / 2)
	SQRT2 = math.sqrt(2)
	abs = abs
	acos = math.acos
	asin = math.asin
	atan = math.atan
	atan2 = math.atan2
	ceil = math.ceil
	cos = math.cos
	exp = math.exp
	floor = math.floor
	log = math.log
	pow = math.pow
	random = random.random
	sin = math.sin
	sqrt = math.sqrt
	tan = math.tan

	@classmethod
	def max(cls, *numbers):
		return max(numbers)

	@classmethod
	def min(cls, *numbers):
		return min(numbers)

	@classmethod
	def round(cls, number):
		return round(number)


class Number(Object):
	MAX_VALUE = sys.float_info.max
	MIN_VALUE = sys.float_info.min
	NaN = float('nan')
	NEGATIVE_INFINITY = float("inf")
	POSITIVE_INFINITY = float("-inf")

	def __init__(self, value=0):
		Object.__init__(self, float(value))

	def isNaN(self):
		return math.isnan(self.value)

	def isFinite(self):
		return math.isfinite(self.value)

	def isInteger(self):
		return self.value.is_integer()

	def toExponential(self, fractionalDigits=None):
		if fractionalDigits is not None:
			s = ("%0." + str(fractionalDigits - 1) + "e") % self.value
		else: # no need to specify precision, then
			s = "%e" % self.value
		return String(s.replace("+0", "+"))

	def toFixed(self, fractionalDigits=0):
		""" returns a string representing the number in fixed-point notation """
		s = ("%0." + str(fractionalDigits) + "f") % round(self.value, fractionalDigits)
		return String(s.replace("+0", "+"))

	def toPrecision(self, digits=None):
		if digits is None:
			return self.toString()
		s = ("%0." + str(digits) + "g") % self.value # does pretty much what the js-documentation says
		return String(s.replace("+0", "+").ljust(digits, "0"))


class RegExp(Object):
	def __init__(self, pattern, flags=""):
		Object.__init__(self, pattern)
		self.global_ = 0 # can't use the keyword "global" in python
		self.ignoreCase = False
		self.lastIndex = 0
		self.multiline = False
		self.source = pattern
		re_flags = 0
		if "i" in flags:
			self.ignoreCase = False
			re_flags |= re.IGNORECASE
		if "g" in flags:
			self.global_ = True
		if "m" in flags:
			self.multiline = True
			re_flags |= re.MULTILINE
		self._r = re.compile(pattern, re_flags)

	def exec(self, string):
		if self.global_:
			return Array(*self._r.findall(string))
		return Array(self._r.search(string).group())

	def test(self, string):
		return not self._r.search(string) is None


class String(Object):
	def __init__(self, value=""):
		Object.__init__(self, str(value))

	def __str__(self):
		return self.value

	def __len__(self):
		return len(self.value)

	@classmethod
	def fromCharCode(cls, *chars):
		return String("".join(chr(i) for i in chars))

	def charAt(self, pos):
		""" If pos is out of range, JavaScript returns an empty string """
		if pos >= len(str):
			return ""
		return self.value[pos]

	def charCodeAt(self, pos):
		return ord(self.value[pos])

	def concat(self, *strings):
		return String(self.value + "".join(strings))

	def contains(self, needle, position=0):
		return needle in self.value[position:]

	def endsWith(self, needle, position=None):
		""" position (optional): search within this string as if this string were only this long """
		if position is not None:
			return self.value[:position].endswith(needle)
		return self.value.endswith(needle)

	def indexOf(self, sub, start=0):
		return self.value.find(sub, start)

	def lastIndexOf(self, sub, start=None):
		if start is None:
			return self.value.rfind(sub)
		return self.value.rfind(sub, start)

	def localeCompare(self, compareString, locales, options):
		return 0

	def match(self, regexp):
		return Array(*list(String(value) for value in re.findall(regexp, self.value)))

	def search(self, regexp):
		""" if successful, search returns the index of the regular
		expression inside the string; otherwise, it returns -1 """
		match = re.search(regexp, self.value)
		return -1 if match is None else match.start()

	def replace(self, old, new):
		return self.value.replace(old, new)

	def slice(self, start, end):
		return String(self.value[start:end])

	def split(self, sep=None, maxsplit=-1):
		return Array(*list(String(value) for value in self.value.split(sep, maxsplit)))

	def substr(self, start, length):
		return String(self.value[start:start + length])

	def substring(self, start, end):
		return String(self.value[start:end])

	def toLowerCase(self):
		return String(self.value.lower())

	def toLocaleLowerCase(self):
		return String(self.value.lower())

	def toLocaleUpperCase(self):
		return String(self.value.upper())

	def toUpperCase(self):
		return String(self.value.upper())


class Error(Exception, Object):
	def __init__(self, message, fileName, lineNumber):
		Exception.__init__(self, message)
		Object.__init__(self, message)


class EvalError(Error):
	pass


class RangeError(Error):
	pass


undefined = None
Infinity = Number.POSITIVE_INFINITY
NaN = Number.NaN
Boolean = bool
parseInt = int
parseFloat = float
isNaN = math.isnan
isFinite = math.isfinite


# Document Object Model (DOM) Document
# https://developer.mozilla.org/en-US/docs/Web/API/Document

class Document(dom.Document):
	def querySelector(self, selectors):
		pass

	def querySelectorAll(self, selectors):
		pass

# Document Object Model (DOM) Document
# https://developer.mozilla.org/en-US/docs/Web/API/Element

class Element(dom.Element):
	def querySelector(self, selectors):
		pass

	def querySelectorAll(self, selectors):
		pass
