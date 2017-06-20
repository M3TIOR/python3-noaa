#!/usr/bin/python3

# M3TIOR 2017
#
#

# API imports
from .utils import NOAADataset, DatasetError

# Python3 imports
import datetime
import copy			#using this for memory protection.
import math			#optimization here

#########################################################################
# XXX: This is here to generate the sub-encoded bits of the .dly ELEMENTS
#
#	PLZ DO NOT DELETE
#
#
# NOTE:
#	This could used some optimization, if just a little.
#	Please don't forget to come back and work on it...
#

def __subencode__(*encodings, key_prefix=None, description_prefix=None, unit=None, mask=None):
	ret = {}								# our output
	retret = {}
	counter = [0 for l in encodings] 		# this holds all our counters
	c_max = [len(l) for l in encodings]		# this holds all the counter's max values
	digits = len(counter)					# the number of spaces / digits in our outputs
	while True:
		try:
			# The try here's needed to capture the out of bound reads
			# So that they can be passed onto the counter
			code = 0
			description = description_prefix
			for digit in range(0, digits):
				code += list(encodings[digits-1-digit].keys())[counter[digits-1-digit]]*(10**digit)
				description += " " + list(encodings[digits-1-digit].values())[counter[digits-1-digit]]
			if code < 10:
				ret[key_prefix+"0"+str(code)]=(description, unit, None)
			else:
				ret[key_prefix+str(code)]=(description, unit, None)
		except IndexError:
			pass

		for digit in reversed(range(0, digits)):
			if counter[digit] < c_max[digit]:
				counter[digit] += 1
				break
			elif not digit and counter[digit] >= c_max[digit]:
				if isinstance(mask, list):
					for element in mask:
						if element < 10:
							tmpelement = key_prefix+"0"+str(element)
						else:
							tmpelement = key_prefix+str(element)
						if tmpelement in ret.keys():
							retret[tmpelement]=ret[tmpelement]
				else:
					retret = ret
				return retret
			else:
				counter[digit] = 0
				continue


_soil_type = {
	0:"in unknown",
	1:"in grass",
	2:"in fallow",
	3:"in bare ground",
	4:"in brome grass",
	5:"in sod",
	6:"in straw multch",
	7:"in grass muck",
	8:"in bare muck"
}
_depth_subcode = {
	1:"down 5 centimeters",
	2:"down 10 centimeters",
	3:"down 20 centimeters",
	4:"down 50 centimeters",
	5:"down 100 centimeters",
	6:"down 150 centimeters",
	7:"down 180 centimeters"
}
_weather_type = {
	1:"Fog, ice fog, or freezing fog",
	2:"Heavy fog or heaving freezing fog", #Not always distinguished from fog
	3:"Thunder",
	4:"Ice pellets, sleet, or snow pellets",
	5:"Hail",
	6:"Glaze or rime",
	7:"Blowing obstruction, such as: Dust, volcanic ash, blowing dust, or blowing sand",
	8:"Smoke or haze",
	9:"Blowing or drifting snow",
	10:"Tornado, waterspout, or funnel cloud",
	11:"High or damaging winds",
	12:"Blowing spray",
	13:"Mist",
	14:"Drizzle",
	15:"Freezing drizzle",
	16:"Rain",
	17:"Freezing rain",
	18:"Snow, snow pellets, snow grains, or ice crystals",
	19:"Unknown source of precipitation",
	20:"Rain or snow shower",
	21:"Ground fog",
	22:"Ice fog or freezing fog"
}

__elements__={
	"PRCP":("Precipitation", "tenths of millimeters", None),
	"SNOW":("Snowfall", "millimeters", None),
	"SNWD":("Snow depth", "millimeters", None),
	"TMAX":("Maximum temperature", "tenths of degrees^C", None),
	"TMIN":("Minimum temperature", "tenths of degrees^C", None),
	"ACMC":("Average cloudiness from 00:00 to 23:59", "percent", None), #Collected from 30-second ceilometer data
	"ACMH":("Average cloudiness from 00:00 to 23:59", "percent", None), #Collected from manual observations
	"ACSC":("Average cloudiness sunrise to sunset", "percent", None), #Collected from 30-second ceilometer data
	"ACSH":("Average cloudiness sunrise to sunset", "percnt", None), #Collected from manual observations
	"AWDR":("Average wind direction", "degrees", None),
	"AWND":("Average wind speed", "tenths of meters per second", None),
	"DAEV":("Number of days included in the multiday evaporation total", "days", None),
	"DAPR":("Number of days included in the multiday precipiation total", "days", None),
	"DASF":("Number of days included in the multiday snowfall total", "days", None),
	"DATN":("Number of days included in the multiday minimum temperature", "days", None),
	"DATX":("Number of days included in the multiday maximum temperature", "days", None),
	"DAWM":("Number of days included in the multiday wind movement", "days", None),
	"DWPR":("Number of days with non-zero precipitation included in multiday precipitation total", "days", None),
	"EVAP":("Evaporation of water from evaporation pan", "tenths of millimeters", None),
	"FMTM":("Time of fastest mile or fastest 1-minute wind", "hours and minutes", "HHMM"),
	"FRGB":("Base of frozen ground layer", "centimeters", None),
	"FRGT":("Top of frozen ground layer", "centimeters", None),
	"FRTH":("Thickness of frozen ground layer", "centimeters", None),
	"GAHT":("Difference between river and gauge height", "centimeters", None),
	"MDEV":("Multiday evaporation total", "tenths of millimeters", None),
	"MDPR":("Multiday precipitation total", "tenths of millimeters", None),
	"MDSF":("Multiday snowfall total", "millimeters", None),
	#NOTE: MDSF
	# Documentation did not list, the unit for this code, so I'm assuming
	# the unit here. This will be changed later if I'm wrong.
	"MDTN":("Multiday minimum temperature", "tenths of degrees^C", None),
	"MDTX":("Multiday maximum temperature", "tenths of degrees^C", None),
	"MDWM":("Multiday wind movement", "kilometers", None),
	"MNPN":("Daily minimum temperature of water in an evaporation pan", "tenths of degrees^C", None),
	"MXPN":("Daily maximum temperature of water in an evaporation pan", "tenths of degrees^C", None),
	"PGTM":("Peak gust time", "hours and minutes", "HHMM"),
	"PSUN":("Daily percent of possible sunshine", "percent", None),
	"TAVG":("Average temperature", "tenths of degrees^C", None),
	#NOTE: TAVG
	# Note that TAVG from source 'S' corresponds to an average
	# for the period ending at 2400 UTC rather than local midnight
	"THIC":("Thickness of ice on water", "tenths of millimeters", None),
	"TOBS":("Temperature at the time of observation", "tenths of degrees^C", None),
	"TSUN":("Total daily sunshine", "minutes", None),
	"WDF1":("Direction of fastest 1-minute wind", "degrees", None),
	"WDF2":("Direction of fastest 2-minute wind", "degrees", None),
	"WDF5":("Direction of fastest 5-minute wind", "degrees", None),
	"WDFG":("Direction of peak wind gust", "degrees", None),
	"WDFI":("Direction of highest instantaneous wind", "degrees", None),
	"WDFM":("Fastest mile wind direction", "degrees", None),
	"WDMV":("24-hour wind movement", "kilometers", None),
	"WESD":("Water equivalent of snow on the ground", "tenths of millimeters", None),
	"WESF":("Water equivalent of snowfall", "tenths of millimeters", None),
	"WSF1":("Fastest 1-minute wind speed", "tenths of meters per second", None),
	"WSF2":("Fastest 2-minute wind speed", "tenths of meters per second", None),
	"WSF5":("Fastest 5-minute wind speed", "tenths of meters per second", None),
	"WSFG":("Peak gust wind speed", "tenths of meters per second", None),
	"WSFI":("Highest instantaneous wind speed", "tenths of meters per second", None),
	"WSFM":("Fastest mile wind speed", "tenths of meters per second", None),
}

__elements__.update(__subencode__(_soil_type, _depth_subcode,
	key_prefix="SN",
	description_prefix="Minimum soil temperature",
	unit="tenths of degrees^C",
	mask=None))

__elements__.update(__subencode__(_soil_type, _depth_subcode,
	key_prefix="SM",
	description_prefix="Maximum soil temperature",
	unit="tenths of degrees^C",
	mask=None))

__elements__.update(__subencode__(_weather_type,
	key_prefix="WT",
	description_prefix="Weather Type",
	unit=None,
	mask=[x for x in range(1,23) if not x==20]))

__elements__.update(__subencode__(_weather_type,
	key_prefix="WV",
	description_prefix="Weather in the vicinity",
	unit=None,
	mask=[1, 3, 7, 18, 20]))
#
#
#########################################################################

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

	class __flag__():
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

	class M(__flag__):
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

	class Q(__flag__):
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

	class S(__flag__):
		"""
			Source flag
		"""
		#NOTE:	When data are available for the same time from more than one source
		#		the highest priority source is chosen according to the following
		#		priority order (from highest to lowest):
		#		Z,R,0,6,C,X,W,K,7,F,B,M,r,E,z,u,b,s,a,G,Q,I,A,N,T,U,H,S
		_description="Source"
		_values={
			' ':"None",
			'0':"U.S. Cooperative Summary of the Day", #NCDC DSI-3200
			'6':"CDMP Cooperative Summary of the Day", #NCDC DSI-3206
			'7':"U.S. Cooperative Summary of the Day -- Transmitted",
			'A':"U.S. Automated Surface Observing System (ASOS)", #real-time data (since January 1, 2006)
			'a':"Australian data from the Australian Bureau of Meteorology",
			'B':"U.S. ASOS data for October 2000-December 2005", #(NCDC DSI-3211)
			'b':"Belarus update",
			'C':"Environment Canada",
			'E':"European Climate Assessment and Dataset", #(Klein Tank et al., 2002)
			'F':"U.S. Fort data",
			'G':"Official Global Climate Observing System (GCOS) or other government-supplied data",
			'H':"High Plains Regional Climate Center real-time data",
			'I':"International collection", #(non U.S. data received through personal contacts)
			'K':"U.S. Cooperative Summary of the Day data digitized from paper observer forms",
			# 'K' --> (from 2011 to present)
			'M':"Monthly METAR Extract", #(additional ASOS data)
			'N':"Community Collaborative Rain, Hail,and Snow (CoCoRaHS)",
			'Q':"Data from several African countries that had been \"quarantined\", that is, withheld from public release until permission was granted from the respective meteorological services",
			'R':"NCEI Reference Network Database (Climate Reference Network and Regional Climate Reference Network)",
			'r':"All-Russian Research Institute of Hydrometeorological Information-World Data Center",
			'S':"Global Summary of the Day", #(NCDC DSI-9618)
			#NOTE: "S" values are derived from hourly synoptic reports
            #      exchanged on the Global Telecommunications System (GTS).
            #      Daily values derived in this fashion may differ significantly
            #      from "true" daily data, particularly for precipitation
            #      (i.e., use with caution).
			's':"China Meteorological Administration/National Meteorological Information Center/Climatic Data Center", #(http://cdc.cma.gov.cn)
			'T':"Snowpack Telemtry (SNOTEL) data obtained from the U.S. Department of Agriculture's Natural Resources Conservation Service",
			'U':"Remote Automatic Weather Station (RAWS) data obtained from the Western Regional Climate Center",
			'u':"Ukraine update",
			'W':"WBAN/ASOS Summary of the Day from NCDC's Integrated Surface Data (ISD).",
			'X':"U.S. First-Order Summary of the Day", #(NCDC DSI-3210)
			'Z':"Datzilla official additions or replacements",
			'z':"Uzbekistan update",
		}

	class element():
		#NOTE: _soil_type, _depth_subcode, _weather_type
		# Ok, I just want to take a second to rant about this crap.
		# Who the hell thought it was a good idea to do this in a database?
		# Like, I understand being a maintainer and all, and having to extrapolate
		# upon what interfaces already exist for legacy support, but the amount
		# of bullshit that goes into accounting for each of these stupid codes...
		#
		_values=__elements__
		#
		# XXX: Values passed by refference for subencoding pre-load
		#

		def __init__(self, value):
			if not isinstance(value, str):
				raise TypeError("Expected type 'str' not '%s'"%( value.__class__.__name__))
			if not self._values(value):
				raise ValueError("Code '%s' does not exist!")
			self._val=value
		def __str__(self):
			return str(self._val)
		def long_name(self):
			"""
				Returns the long name/description of the current element's code.
				Throws an error if it doesn't yet have a code.
			"""
			if self._val not None:
				return copy.deepcopy(self._values(self._val)[0])
			else
				raise DatasetError("Element missing!")
		def unit(self):
			"""
				Returns the unit this element's corresponding values are
				measured in.
			"""
			if self._val not None:
				return copy.deepcopy(self._values(self._val)[1])
			else
				raise DatasetError("Element missing!")
		def format(self):
			"""
				Returns the format of this element's corresponding values
				if one exists.
			"""
			if self._val not None:
				return copy.deepcopy(self._values(self._val)[2])
			else
				raise DatasetError("Element missing!")
		def search(self, string):
			if not isinstance(string, str):
				raise TypeError("Expected type 'str' not '%s'"%( string.__class__.__name__))

	def __init__(self, ID=None, YEAR=None, MONTH=None, ELEMENT=None,
		VALUE=[], MFLAG=[], QFLAG=[], SFLAG=[]):
		if not isinstance(ID, str):
			raise TypeError("Expected type 'str' not '%s'"%( ID.__class__.__name__))
		else if ID.__len__() > 10:
			raise ValueError("ID should not exceed 10 characters in length")
		if not isinstance(YEAR, int):
			raise TypeError("Expected type 'int' not '%s'"%( YEAR.__class__.__name__))
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
		raise UnimplientedError()
	def encode(self):
		raise UnimplientedError()


def search_by_station():
	raise UnimplientedError()
def search_by_day():
	raise UnimplientedError()
def search_by_month():
	raise UnimplientedError()
def search_by_year():
	raise UnimplientedError()
def search_by_info(station=None, date_from=None, date_to=None, element=None):
	raise UnimplientedError()
def station_search():
	raise UnimplientedError()


# XXX:
#	Pass-by-refference preloader cleanup
#
del __elements__
del _soil_type
del _depth_subcode
del _weather_type
del __subencode__


# Run tests here
if __name__ == "__main__":
