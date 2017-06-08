#!/usr/bin/python3

# M3TIOR 2017
#
#

# API imports
from .utils import NOAADataset, DatasetError

# Python3 imports
import datetime
import copy			#using this for memory protection.

class dly(NOAADataset):
	"""
		The .dly Dataset given by ghcn daily interface
	"""
	#------------------------------
	#Variable   Columns   Type
	#------------------------------
	#ID            1-11   Character
	#YEAR         12-15   Integer
	#MONTH        16-17   Integer
	#ELEMENT      18-21   Character
	#VALUE1       22-26   Integer
	#MFLAG1       27-27   Character
	#QFLAG1       28-28   Character
	#SFLAG1       29-29   Character
	#VALUE2       30-34   Integer
	#MFLAG2       35-35   Character
	#QFLAG2       36-36   Character
	#SFLAG2       37-37   Character
	#  .           .          .
	#  .           .          .
	#  .           .          .
	#VALUE31    262-266   Integer
	#MFLAG31    267-267   Character
	#QFLAG31    268-268   Character
	#SFLAG31    269-269   Character
	#------------------------------

	#ID      =        None # The station identification code.
	#YEAR    =        None # Year of the reccord
	#MONTH   =        None # Month of the reccord
	#ELEMENT =        None # COMPLICATED DX DX DX 4 Characters
	#VALUE   =        []   # Five Characters ~ 4 byte interger / index = day
	#MFLAG   =        []   # Single Character Flag / index = day
	#QFLAG   =        []   # Single Character Flag / index = day
	#SFLAG   =        []   # Single Character Flag / index = day

	class flag():
		def __init__(self, value):
			if not isinstance(value, str):
				raise TypeError("Expected type 'str' not '%s'"%( ID.__class__.__name__,))
			for key in self._values.keys():
				if key == value
					self._val = value
					return
			raise ValueError("%s flag '%s' does not exist"%(self._description, value))
		def	__str__(self):
			return self._val
		def description(self):
			return self._values(self._val)
		def search(self, string):
			ret = [] #Return value holder
			for flag in self._values.keys():
				if self._values(flag).find(string) or flag.find(string):
					ret.append("%s : %s"%(flag, self._values(flag)))
			return copy.deepcopy(ret)

	class M(flag):
		"""
			Measurement flag
		"""
		_description="Measurement"
		_values={
			' ':"No measurement information applicable"
			'B':"precipitation total formed from two 12-hour totals",
			'D':"precipitation total formed from four six-hour totals",
			'H':"represents highest or lowest hourly temperature or the average of hourly values",
			'K':"converted from knots",
			'L':"temperature appears to be lagged with respect to reported hour of observation",
			'O':"converted from oktas",
			'P':"missing presumed zero", #DSI 3200 and 3206
			'T':"trace of precipitation, snowfall, or snow depth",
			'W':"converted from 16-point WBAN code"
		}

	class Q(flag):
		"""
			Quality flag
		"""
		_description="Quality"
		_values={
			' ':"Did not fail any quality assurance check",
			'D':"failed duplicate check",
			'G':"failed gap check",
			'I':"failed internal consistency check",
			'K':"failed streak/frequent-value check",
			'L':"failed check on length of multiday period",
			'M':"failed megaconsistency check",
			'N':"failed naught check",
			'O':"failed climatological outlier check",
			'R':"failed lagged range check",
			'S':"failed spatial consistency check",
			'T':"failed temporal consistency check",
			'W':"temperature too warm for snow",
			'X':"failed bounds check",
			'Z':"flagged as a result of an official Datzilla investigation" # weird flag
		}

	class S(flag):
		"""
			Source flag
		"""
		_description="Source"
		_values={
			'':"",
			'':"",
			'':"",
			'':"",
			'':"",
			'':"",
			'':"",
			'':"",
			'':"",
		}

	class element():
		#NOTE: _soil_type, _depth_subcode, _weather_type
		# Ok, I just want to take a second to rant about this crap.
		# Who the hell thought it was a good idea to do this in a database?
		# Like, I understand being a maintainer and all, and having to extrapolate
		# upon what interfaces already exist for legacy support, but the amount
		# of bullshit that goes into accounting for each of these stupid codes...
		#
		_soil_type = {
			0:"unknown",
			1:"grass",
			2:"fallow",
			3:"bare ground",
			4:"brome grass",
			5:"sod",
			6:"straw multch",
			7:"grass muck",
			8:"bare muck"
		}
		_depth_subcode = {
			1:"5 centimeters",
			2:"10 centimeters",
			3:"20 centimeters",
			4:"50 centimeters",
			5:"100 centimeters",
			6:"150 centimeters",
			7:"180 centimeters"
		}
		_weather_type = [
			"Fog, ice fog, or freezing fog",
			"Heavy fog or heaving freezing fog", #Not always distinguished from fog
			"Thunder",
			"Ice pellets, sleet, or snow pellets",
			"Hail",
			"Glaze or rime"
			"Blowing obstruction, such as: Dust, volcanic ash, blowing dust, or blowing sand",
			"Smoke or haze",
			"Blowing or drifting snow",
			"Tornado, waterspout, or funnel cloud",
			"High or damaging winds",
			"Blowing spray",
			"Mist",
			"Drizzle",
			"Freezing drizzle",
			"Rain",
			"Freezing rain",
			"Snow, snow pellets, snow grains, or ice crystals",
			"Unknown source of precipitation",
			"Rain or snow shower",
			"Ground fog",
			"Ice fog or freezing fog"
		]
		_values={
			"PRCP":("Precipitation", "tenths of millimeters", None, None),
			"SNOW":("Snowfall", "millimeters", None, None),
			"SNWD":("Snow depth", "millimeters", None, None),
			"TMAX":("Maximum temperature", "tenths of degrees^C", None, None),
			"TMIN":("Minimum temperature", "tenths of degrees^C", None, None),
			"ACMC":("Average cloudiness from 00:00 to 23:59", "percent", None, None), #Collected from 30-second ceilometer data
			"ACMH":("Average cloudiness from 00:00 to 23:59", "percent", None, None), #Collected from manual observations
			"ACSC":("Average cloudiness sunrise to sunset", "percent", None, None), #Collected from 30-second ceilometer data
			"ACSH":("Average cloudiness sunrise to sunset", "percent", None, None), #Collected from manual observations
			"AWDR":("Average wind direction", "degrees", None, None),
			"AWND":("Average wind speed", "tenths of meters per second", None, None),
			"DAEV":("Number of days included in the multiday evaporation total", "days", None, None),
			"DAPR":("Number of days included in the multiday precipiation total", "days", None, None),
			"DASF":("Number of days included in the multiday snowfall total", "days", None, None),
			"DATN":("Number of days included in the multiday minimum temperature", "days", None, None),
			"DATX":("Number of days included in the multiday maximum temperature", "days", None, None),
			"DAWM":("Number of days included in the multiday wind movement", "days", None, None),
			"DWPR":("Number of days with non-zero precipitation included in multiday precipitation total", "days", None, None),
			"EVAP":("Evaporation of water from evaporation pan", "tenths of millimeters", None, None),
			"FMTM":("Time of fastest mile or fastest 1-minute wind", "hours and minutes", "HHMM", None),
			"FRGB":("Base of frozen ground layer", "centimeters", None, None),
			"FRGT":("Top of frozen ground layer", "centimeters", None, None),
			"FRTH":("Thickness of frozen ground layer", "centimeters", None, None),
			"GAHT":("Difference between river and gauge height", "centimeters", None, None),
			"MDEV":("Multiday evaporation total", "tenths of millimeters", None, None),
			"MDPR":("Multiday precipitation total", "tenths of millimeters", None, None),
			"MDSF":("Multiday snowfall total", "millimeters", None, None),
			#NOTE: MDSF
			# Documentation did not list, the unit for this code, so I'm assuming
			# the unit here. This will be changed later if I'm wrong.
			"MDTN":("Multiday minimum temperature", "tenths of degrees^C", None, None),
			"MDTX":("Multiday maximum temperature", "tenths of degrees^C", None, None),
			"MDWM":("Multiday wind movement", "kilometers", None),
			"MNPN":("Daily minimum temperature of water in an evaporation pan", "tenths of degrees^C", None, None),
			"MXPN":("Daily maximum temperature of water in an evaporation pan", "tenths of degrees^C", None, None),
			"PGTM":("Peak gust time", "hours and minutes", "HHMM", None),
			"PSUN":("Daily percent of possible sunshine", "percent", None, None),
			"SN*#":("Minimum soil temperature", "tenths of degrees^C", None, [(self._soil_type, None),(self._depth_subcode, None)]),
			"SX*#":("Maximum soil temperature", "tenths of degrees^C", None, [(self._soil_type, None),(self._depth_subcode, None)]),
			"TAVG":("Average temperature", "tenths of degrees^C", None, None),
			#NOTE: TAVG
			# Note that TAVG from source 'S' corresponds to an average
			# for the period ending at 2400 UTC rather than local midnight
			"THIC":("Thickness of ice on water", "tenths of millimeters", None, None),
			"TOBS":("Temperature at the time of observation", "tenths of degrees^C", None, None),
			"TSUN":("Total daily sunshine", "minutes", None, None),
			"WDF1":("Direction of fastest 1-minute wind", "degrees", None, None),
			"WDF2":("Direction of fastest 2-minute wind", "degrees", None, None),
			"WDF5":("Direction of fastest 5-minute wind", "degrees", None, None),
			"WDFG":("Direction of peak wind gust", "degrees", None, None),
			"WDFI":("Direction of highest instantaneous wind", "degrees", None, None),
			"WDFM":("Fastest mile wind direction", "degrees", None, None),
			"WDMV":("24-hour wind movement", "kilometers", None, None),
			"WESD":("Water equivalent of snow on the ground", "tenths of millimeters", None, None),
			"WESF":("Water equivalent of snowfall", "tenths of millimeters", None, None),
			"WSF1":("Fastest 1-minute wind speed", "tenths of meters per second", None, None),
			"WSF2":("Fastest 2-minute wind speed", "tenths of meters per second", None, None),
			"WSF5":("Fastest 5-minute wind speed", "tenths of meters per second", None, None),
			"WSFG":("Peak gust wind speed", "tenths of meters per second", None, None),
			"WSFI":("Highest instantaneous wind speed", "tenths of meters per second", None, None),
			"WSFM":("Fastest mile wind speed", "tenths of meters per second", None, None),
			"WT**":("Weather type", None, None, [(self._weather_type, [x for x in range(1,23) if not x==20])]),
			"WV**":("Weather in the vicinity", None, None, [(self._weather_type, [01, 03, 07, 18, 20])])
		}
		def __init__(self, value):
			if not isinstance()
			self._val=value
		def __str__(self):
			return str(self._val)
		def long_name(self):
			"""
				Returns the long name/description of the current element's code.
				Throws an error if it doesn't yet have a code.
			"""
			if self._val not None:
				return self._values(self._val)[0]
			else
				raise DatasetError("")
		def unit(self):
			"""
				Returns the unit this element's corresponding values are
				measured in.
			"""
			return self._values(self._val)[1]
		def format(self):
			"""
				Returns the format of this element's corresponding values
				if one exists.
			"""
			return self._values(self._val)[2]
		def search(self, string):
			if not isinstance(string, str):
				raise TypeError()

	def __init__(self, ID=None, YEAR=None, MONTH=None, ELEMENT=None,
		VALUE=[], MFLAG=[], QFLAG=[], SFLAG=[]):
		if not isinstance(ID, str):
			raise TypeError("Expected type 'str' not '%s'"%( ID.__class__.__name__,))
		else if ID.__len__() > 10:
			raise ValueError("ID should not exceed 10 characters in length")
		if not isinstance(YEAR, int):
			raise TypeError("Expected type 'int' not '%s'"%( YEAR.__class__.__name__,))
		else if YEAR > 9999:
			raise ValueError("YEAR should not exceed 9999")
		else if YEAR < 0:
			raise ValueError("YEAR cannot be a negative number")
		if not isinstance(MONTH, int):
			raise TypeError("Expected type 'int' not '%s'"%( MONTH.__class__.__name__,))
		else if MONTH < 0:
			raise ValueError("MONTH cannot be a negative number")
		else if MONTH > 12:
			raise ValueError("MONTH should not exceed 9999")
		if not isinstance(ELEMENT, self.element):
			if not isinstance(ELEMENT, str):
				raise TypeError("Expected type 'str' not '%s'"%( ELEMENT.__class__.__name__,))
		else:




	def __str__(self):
		return self.encode()
	def decode(self, data):
	def encode(self):


def search_by_station():
def search_by_day():
def search_by_month():
def search_by_year():
def search_by_info(station=None, date_from=None, date_to=None, element=None):

def station_search():
