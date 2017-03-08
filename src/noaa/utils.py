#!/usr/bin/python3

# M3TIOR 2017
#
#

import sys
import socket
import tempfile
from ftplib import FTP

class NOAADatabase(FTP):
	"""
		The base class for NOAA database interactions.
		Overrides basic connection information with correct
		defaults, and ensure's we're managed properly

		This class can also optimize server queries by storing
		data locally, either for an extended period or temporarily
		to reduce the amount of redundant server queries when
		doing operations on large datasets.

		(cache-ing) :: couldn't remember the term when I started ...
	"""
	devel = 0 #DEBUG LEVEL
	_ftp

	def __init__(self, email='', path='', cache=False):
		"""override init"""
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
		if cache:
			self.init_cache(directory=path)


	def __enter__(self):
		"""override context"""
		return self

    # Context management protocol: try to quit() if active
	def __exit__(self, *args):
		"""override exit
			---------------------------------
			Context exit implement, inherited
			directly from FTPlib source
		"""
		# had to copy this from the ftplib source because
		# I don't think there's a way for me to mirror *args
		# wildcard into another function without doing extra
		# unnecessary stuff. Someone should figure that out for
		# me...
		if self.sock is not None:
			try:
				self.quit()
			except (OSError, EOFError):
				pass
			finally:
				if self.sock is not None:
					self.close()
		# aaaand the rest of this is mine...
		if self.storage is not None:
			self.close_cache()


	def connect(self, timeout=30, source_address=None):
		"""override connect"""
		super().connect(host='ftp.ncdc.noaa.gov', 	# Always the same host
				timeout=timeout,					# Timeout is inherited
				source_address=source_address)		# along with this thing

	def login(self, email=''):
		"""override login"""
		# FTP login defaults to anonymous without args,
		# so we don't need to append any arguments here
		# besides the password requested: which is the email
		# of the user requesting access to the database
		super().login(passwd=email)

	def init_cache(self, directory=''):
		self.storage = tempfile.TemporaryDirectory(dir= directory if directory != '' else None)

	def close_cache(self):
		if self.storage is not None:
			self.storage.cleanup()



class NOAADatabaseError(BaseException):
	"""
		The base class for database error handling.
	"""

if __name__ == "__main__":
	test = NOAADatabase(email='jtimmerman32@gmail.com')
