#!/usr/bin/python3

# M3TIOR 2017
#
#

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
	def relinquish(self, **files, dir=None):
		raise UnimplementedError # because lazy atm...

	def request(self, dir=None, facts=None, callback=None, blocksize=8192):
		if self._ftp.sock is not None:
			for f in _ftp.mlsd(dir, facts):
				self._ftp.retrbinary("RETR %s"%())
		else
			raise NOAADatabaseError()

class NOAACache():
	"""
		This class optimizes server queries by storing
		data locally, either for an extended period or temporarily
		to reduce the amount of redundant server queries when
		doing operations on large datasets.

		(cache-ing) :: couldn't remember the term when I started ...
	"""


class NOAADataset():
	"""
		Basic dataset class for controling root data interactions

		***CONSTRUCTOR***
	"""

	# NOTE:
	# Each folder in the NOAA's public dataset and each is refferenced
	# individually as a seperate interface, this localdata header exists
	# for the purpose of isolating where in a master archive this interface
	# exists.
	#_directory  = None
	#
	# DEPRICATED

	# NOTE: _raw
	# Data structure, dictionary w/ file name's as key and data as raw ascii
	#_raw        = None  #Ram storage
	#_cache      = None  #Cache storage

	def __init__(self):

	def decode(self, data):
		raise UnimplementedError
	def encode(self):
		raise UnimplementedError

class NOAAError(Exception):
	"""
		The base class for error handling in this module.
	"""
	pass

class DatasetError(NOAAError):
	"""
		Any error happening within an noaa dataset
	"""
	def __init__(self, message):
		self.message = message

class ParserError(NOAAError):
	"""

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


if __name__ == "__main__":
