#!/usr/bin/python3

# M3TIOR 2017
#
#

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
		pass
	def decode(self, data):
		raise UnimplementedError()
	def encode(self):
		raise UnimplementedError()

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

if __name__ == "__main__":
	pass
