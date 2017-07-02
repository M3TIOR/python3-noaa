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

import tempfile
import socket
from ftplib import FTP

class NOAADatabase():
	"""
		base class for NOAA database interactions.
		Overrides basic connection information with correct
		defaults, and ensure's we're managed properly
	"""
	root   = "/pub/data"   #Master Database directory
	ftp    = None          #FTP connection

	def __init__(self, email=''):
		"""override init"""
		self.ftp = FTP()
		# Basically this everything the FTP init does,
		# but I'm doing it here to remove the magical
		# borkedness that is inheritence problems when calling
		# inherited class functions (*-*) grrrrrrrrrrrr
		self.connect()
		# for the reccord, I was having problems with the timeout var
		# in connect magically becoming the same value as the first argument
		# of this init, despite my explicitly defining it as otherwise...
		self.login(email)
		# so yea, sorry for not being able to fix that, cause I'd include
		# a variable timeout option, as extend the FTP class functionality,
		# if it were possible anyway.

	def __enter__(self):
		"""override context"""
		return self

    # Context management protocol: try to quit() if active
	def __exit__(self, *args):
		"""override exit"""
		self.ftp.__exit__(*args)

	def connect(self, timeout=socket.SO_KEEPALIVE):
		"""override connect"""
		self.ftp.connect(host='ftp.ncdc.noaa.gov', 	# Always the same host
				timeout=timeout)					# And keepalive timeout

	def login(self, email=''):
		"""override login"""
		# FTP login defaults to anonymous without args,
		# so we don't need to append any arguments here
		# besides the password requested: which is the email
		# of the user requesting access to the database
		self.ftp.login(passwd=email)
		# then move to the appropriate database directory
		self.ftp.cwd('/pub/data')
		# make absolutely sure passive mode is turned on!
		self.ftp.set_pasv(True)

	def set_blocksize(self, blocksize):
		self._block = blocksize

	def keep_alive():
		self.ftp.voidcmd("NOOP")

	#----------------------------------------------------------------#
	# BEGIN RESTFUL ACTIONS
	# I do have to admit, this is powerful, but not at all robust...
	#----------------------------------------------------------------#
	def send():
		raise UnimplementedError()
	def get():
		raise UnimplementedError()
	def relinquish(self, *files, dir=None):
		raise UnimplementedError() # because lazy atm...
	def request(self, dir=None, facts=None, callback=None, blocksize=8192):
		for f in ftp.mlsd(dir, facts):
			self.ftp.retrbinary("RETR %s"%())
