# MIT License
#
# Copyright (c) 2017 Onyx
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#version = "v0.0.1"

import sys
import socket
import tempfile
from ftplib import FTP

class NOAADatabase():
	"""
		base class for NOAA database interactions.
		Overrides basic connection information with correct
		defaults, and ensure's we're managed properly
	"""
	_block       = 1024          #default block size
	_devel       = 0             #DEBUG LEVEL
	_directory   = "/pub/data"   #Master Database directory
	_ftp         = None          #FTP connection

	def __init__(self, email='', devel=0):
		"""override init"""
		self.set_devel(devel)
		self._ftp = FTP()
		# Basically this everything the FTP init does,
		# but I'm doing it here to remove the magical
		# borkedness that is inheritence problems when calling
		# inherited class functions (*-*) grrrrrrrrrrrr
		self._ftp.connect()
		# for the reccord, I was having problems with the timeout var
		# in connect magically becoming the same value as the first argument
		# of this init, despite my explicitly defining it as otherwise...
		self._ftp.login(email)
		# so yea, sorry for not being able to fix that, cause I'd include
		# a variable timeout option, as extend the FTP class functionality,
		# if it were possible anyway.

	def __enter__(self):
		"""override context"""
		return self

    # Context management protocol: try to quit() if active
	def __exit__(self, *args):
		"""override exit"""
		self._ftp.__exit__(*args)


	def connect(self, timeout=30, source_address=None):
		"""override connect"""
		self._ftp.connect(host='ftp.ncdc.noaa.gov', 	# Always the same host
				timeout=timeout,					# Timeout is inherited
				source_address=source_address)		# along with this thing

	def login(self, email=''):
		"""override login"""
		# FTP login defaults to anonymous without args,
		# so we don't need to append any arguments here
		# besides the password requested: which is the email
		# of the user requesting access to the database
		self._ftp.login(passwd=email)

	def set_devel(self, devel=0):
		self._devel = devel;

	def set_blocksize(self, blocksize):
		self._block = blocksize

	#----------------------------------------------------------------#
	# BEGIN RESTFUL ACTIONS
	# I do have to admit, this is powerful, but not at all robust...
	#----------------------------------------------------------------#
	def relinquish(self, *files, dir=None):                                #SEND
		raise UnimplementedError() # because lazy atm...

	def request(self, dir=None, facts=None, callback=None, blocksize=8192): #GET
		if self._ftp.sock is not None:
			for f in _ftp.mlsd(dir, facts):
				self._ftp.retrbinary("RETR %s"%())
		else:
			raise NOAADatabaseError()

class NOAACache():
	"""
		This class optimizes server queries by storing
		data locally, either for an extended period or temporarily
		to reduce the amount of redundant server queries when
		doing operations on large datasets.

		(cache-ing) :: couldn't remember the term when I started ...
	"""

def QUICKCONNECT(email=None):
	"""
		Quick connect to NOAA master DB

		Returns an ftp connection for queries and data handling
		the working directory is preset to the /pub/data folder
	"""
	ftp = FTP('ftp.ncdc.noaa.gov')
	ftp.login()
	ftp.cwd('/pub/data')
	return ftp
