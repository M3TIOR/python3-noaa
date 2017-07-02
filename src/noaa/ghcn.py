#!/usr/bin/python3

# M3TIOR 2017
#
#

# API imports
if __name__!="__main__":
	from .utils import NOAADataset
else:
	#XXX: workaround for local testing
	import utils as NOAA_utils
	NOAADataset = NOAA_utils.NOAADataset


# Python3 imports
import datetime
# WE DON'T NEED MEMORY PROTECTIONS!!!

# DATABASE PREFIX
dir="ghcn"

#########################################################################
# XXX: This is here to generate the sub-encoded bits of the .dly ELEMENTS
#
#	PLZ DO NOT DELETE
#
# Keep in mind this is only here so I don't have to type in a bunch of shit
# manually lol.
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
	"NULL":("empty value placeholder", None, None),
	#NOTE: NULL
	# This is a custom value I'm adding in so I don't have to code in
	# an extra exception for it. It may also aid in debugging I hope.
	# It holds no value within the NOAA database standards.
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

__daily_mask__={
	"ID":(0,11),
	"YEAR":(11,15),
	"MONTH":(15,17),
	"ELEMENT":(17,21),
}
#__daily_mask__.update({"VALUE"+str(day):(21+day*8,29+day*8) for day in range(1,32)})
__daily_mask__.update({"VALUE"+str(day):(21+(day*8),21+(day*8)+5) for day in range(0,31)})
__daily_mask__.update({"MFLAG"+str(day):(21+(day*8)+5,21+(day*8)+6) for day in range(0,31)})
__daily_mask__.update({"QFLAG"+str(day):(21+(day*8)+6,21+(day*8)+7) for day in range(0,31)})
__daily_mask__.update({"SFLAG"+str(day):(21+(day*8)+7,21+(day*8)+8) for day in range(0,31)})
#
#
#########################################################################


class __flag__():
	def __init__(self, value):
		if not isinstance(value, str):
			raise TypeError("Expected type 'str' not '%s'"%( value.__class__.__name__,))
		if value in self.values.keys():
			self.value = value
			return
		raise ValueError("%s flag '%s' does not exist"%(self.description, value))
	def	__str__(self):
		return str(self.value)
	def description(self):
		return self.values(self.value)
	def search(self, string):
		ret = [] #Return value holder
		for flag in self.values.keys():
			if self.values(flag).find(string) or flag.find(string):
				ret.append("%s : %s"%(flag, self.values(flag)))
		return ret

class MFLAG(__flag__):
	"""
		Measurement flag
	"""
	description="Measurement"
	values={
		' ':"No measurement information applicable",
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

class QFLAG(__flag__):
	"""
		Quality flag
	"""
	description="Quality"
	values={
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

class SFLAG(__flag__):
	"""
		Source flag
	"""
	#NOTE:	When data are available for the same time from more than one source
	#		the highest priority source is chosen according to the following
	#		priority order (from highest to lowest):
	#		Z,R,0,6,C,X,W,K,7,F,B,M,r,E,z,u,b,s,a,G,Q,I,A,N,T,U,H,S
	description="Source"
	values={
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

class ELEMENT():
	"""

	"""
	#NOTE: _soil_type, _depth_subcode, _weather_type
	# Ok, I just want to take a second to rant about this crap.
	# Who the hell thought it was a good idea to do this in a database?
	# Like, I understand being a maintainer and all, and having to extrapolat`e
	# upon what interfaces already exist for legacy support, but the amount
	# of bullshit that goes into accounting for each of these stupid codes...
	#
	values=__elements__
	#
	# XXX: Values passed by refference for subencoding pre-load
	#
	#NOTE: I think I may end up copying the fromat of the element class from the
	# other file stuff since it would make things uniform

	def __init__(self, value):
		if not isinstance(value, str):
			raise TypeError("Expected type 'str' not '%s'"%( value.__class__.__name__))
		if not self.values[value]:
			raise ValueError("Code '%s' does not exist!")
		self.value=value
	def __str__(self):
		return str(self.value)
	def long_name(self):
		"""
			Returns the long name/description of the current element's code.
			Throws an error if it doesn't yet have a code.
		"""
		if self.value != None:
			return self.values[self.value][0]
	def unit(self):
		"""
			Returns the unit this element's corresponding values are
			measured in.
		"""
		if self.value != None:
			return self.values[self.value][1]
	def format(self):
		"""
			Returns the format of this element's corresponding values
			if one exists.
		"""
		if self.value != None:
			return self.values[self.value][2]
	def search(self, string):
		"""
			Fetches all codes that contain string
		"""
		ret = []
		if not isinstance(string, str):
			raise TypeError("Expected type 'str' not '%s'"%( string.__class__.__name__))
		for pair in self.values.items():
			if pair[0].find(string) or pair[1].find(string):
				ret.append(pair)
		return ret

class DAY():
	"""
		Data value of a single day
	"""
	def __init__(self, raw=None, value=-9999, mflag=" ", qflag=" ", sflag=" "):
		if raw:
			self.value=int(raw[0:4])
			self.m=MFLAG(raw[5])
			self.q=QFLAG(raw[6])
			self.s=SFLAG(raw[7])
		if isinstance(value, int):
			self.value=value
		elif isinstance(value, str):
			self.value=int(value)
		if isinstance(mflag, str):
			self.m=MFLAG(mflag)
		elif isinstance(mflag, MFLAG):
			self.m=mflag
		if isinstance(qflag, str):
			self.q=QFLAG(qflag)
		elif isinstance(qflag, QFLAG):
			self.q=qflag
		if isinstance(SFLAG, str):
			self.s=SFLAG(sflag)
		elif isinstance(sflag, SFLAG):
			self.s=sflag
	def __str__(self):
		return str(self.value)

class STATION(NOAADataset):
	#------------------------------
	#Variable   Columns   Type
	#------------------------------
	#ID            1-11   Character
	#LATITUDE     13-20   Real
	#LONGITUDE    22-30   Real
	#ELEVATION    32-37   Real
	#STATE        39-40   Character
	#NAME         42-71   Character
	#GSN FLAG     73-75   Character
	#HCN/CRN FLAG 77-79   Character
	#WMO ID       81-85   Character
	#------------------------------
	length=85
	mask={
		"ID":(0,11),
		"LATITUDE":(12,20),
		"LONGITUDE":(21,30),
		"ELEVATION":(31,37),
		"STATE":(38,40),
		"NAME":(41,71),
		"GSN_FLAG":(72,75),
		"HCN_CNR_FLAG":(76,79),
		"WMO_ID":(80,85)
	}
	def __init__(self, ID="NOTDEFINED", LATITUDE=-9999.99,
		LONGITUDE=-9999.99, ELEVATION=-99.99, STATE="NA",
		NAME="-----------------------------", GSN_FLAG="  ",
		HCN_CRN_FLAG="", WMO_ID=""):

	def __str__():
		return self.encode()
	def decode(self, string):
		"""
			Directly converts an entire station entry
		"""
		if not isinstance(string, str):
			raise TypeError("Expected type 'str' not '%s'"%( string.__class__.__name__,))

	def encode(self, string):
		pass


class DAILY(NOAADataset):
	"""
		The daily dataset given by ghcn daily
	"""
	#ID      =        None # The station identification code.
	#YEAR    =        None # Year of the reccord
	#MONTH   =        None # Month of the reccord
	#ELEMENT =        None # COMPLICATED DX DX DX 4 Characters
	# DAY = {
	#	VALUE   =     []   # Five Characters ~ interger / index = day
	#	MFLAG   =     []   # Single Character Flag / index = day
	#	QFLAG   =     []   # Single Character Flag / index = day
	#	SFLAG   =     []   # Single Character Flag / index = day
	# }
	length=269
	mask=__daily_mask__

	def __init__(self, days={}, id="NOTDEFINED", year=-999, month=-1, element="NULL", raw=None):
		if raw:
			return self.decode(raw)
		self.id=id
		self.year=year
		self.month=month
		self.element=ELEMENT(element)
		self.day={x:DAY() for x in range(1,32)}
		self.day.update(days)
		#self._integrity_check()
	def __str__(self):
		return self.encode()
	def decode(self, string):
		"""
			Directly converts an entire .dly entry
		"""
		if not isinstance(string, str):
			raise TypeError("Expected type 'str' not '%s'"%( string.__class__.__name__,))
		self.id=string[0:11]
		self.year=string[11:15]
		self.month=string[15:17]
		self.element=ELEMENT(string[17:21])
		self.day={}
		for day in range(1,32):
			self.day[day] = DAY(value=string[21+((day-1)*8):21+((day-1)*8)+5], #Value
				mflag=string[26+(day-1)*8], #21+5+offset
				qflag=string[27+(day-1)*8], #21+6+offset
				sflag=string[28+(day-1)*8]) #21+7+offset
		return
	def encode(self):
		#NOTE:
		#	check variable's stability here
		#self._integrity_check()
		def pad(value, space):
			return "".join([" " for x in range(value.__len__(), space)]) + str(value)
		out = ""
		out += self.id
		out += str(self.year)
		out += str(self.month)
		out += str(self.element)
		for d in self.day.values():
			out += pad(str(d), 5)
			out += str(d.m)
			out += str(d.q)
			out += str(d.s)
		return out

class YEARLY():
	"""
		the ghcn by_year dataset offered by the noaa
	"""
	delimiter=","
	fields=[
		"ID",
		"DATE",
		"ELEMENT",
		"VALUE",
		"MFLAG",
		"QFLAG",
		"SFLAG",
		"TIME"
	]
	def __init__():
		raise UnimplementedError()

def search_by_mask(data, field, type):
	"""
		search for field in data by mask of "type"
	"""
	if not type.mask:
		raise DatasetError("'%s' not maskable!"%(type.__class__.__name__,))
	ret=[]
	l = type.length+1 # add one for delimiter
	d = data.__len__() # done assuming __len__ scans variable for lenght
	#remainder = d%l
	if d%l:
		raise ValueError("incomplete data entry: data unnexpectedly ends or wrong type")
	for entry in range(1,int(d/l)+1):
		ret.append(data[entry*type.mask[field][0]:entry*type.mask[field][1]])
	return ret
def search_by_masks(data, fields, type):
	raise UnimplementedError()
def search_file_by_mask():
	raise UnimplimentedError()
def search_file_set_by_mask():
	raise UnimplementedError()
def database_get_year(db, year):
	raise UnimplementedError()


# XXX:
#	Pass-by-refference preloader cleanup
#
del(__elements__, _soil_type, _depth_subcode, _weather_type, __subencode__)
del(__daily_mask__)

# Run tests here
if __name__ == "__main__":
	# NOTE: Open test Resources
	import inspect
	import os
	daily_dataset_test_case = open(os.path.dirname(os.path.abspath(
		inspect.stack()[0][1]))[0:40]+"res/ghcn_daily_gsn_test.dly")
	stations_file_test_case = open(os.path.dirname(os.path.abspath(
		inspect.stack()[0][1]))[0:40]+"res/ghcnd-stations.dat")

	# NOTE: Begin DAILY test cases
	#
