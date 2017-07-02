#!/usr/bin/python3

# M3TIOR 2017
#
#

class NOAADataset():
	"""
		Basic dataset class for controling root data interactions

		***CONSTRUCTOR***
	"""
	length    = False
	mask      = False #used to optimize data queries of sets with fixed size
	delimiter = False #denote this name for csv
	field     = False #used as alternative to mask in csv files
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


if __name__ == "__main__":
	pass
