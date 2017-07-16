atom
#!/usr/bin/python3

# M3TIOR 2017
#
#

# API imports
if __name__!="__main__":
	from .utils import Dataset
else:
	#XXX: workaround for local testing
	from utils import Dataset

# Python3 imports
import datetime
# WE DON'T NEED MEMORY PROTECTIONS!!!

# SECTION: local functions
# NOTE: _pad
#	this local function exists only because the ghcn database has some datasets
#	that depend on static fields to hold their values, instead of something like
#	CSV format. This is actually great for optimization purposes, since you
# 	can use some simple math to get your values instead of searching entire
#	database files byte by byte.
def _pad(value, space):
	return str.join([" " for x in range(value.__len__(), space)]) + str(value)

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
__daily_mask__.update({"VALUE"+str(day):(21+(day*8),21+(day*8)+5) for day in range(1,32)})
__daily_mask__.update({"MFLAG"+str(day):(21+(day*8)+5,21+(day*8)+6) for day in range(1,32)})
__daily_mask__.update({"QFLAG"+str(day):(21+(day*8)+6,21+(day*8)+7) for day in range(1,32)})
__daily_mask__.update({"SFLAG"+str(day):(21+(day*8)+7,21+(day*8)+8) for day in range(1,32)})
#
#
#########################################################################

# SECTION: API structures
class __flag__():
	def __init__(self, value=" "):
		if not isinstance(value, str):
			raise TypeError("Expected type 'str' not '%s'"%( value.__class__.__name__,))
		if value in self.values.keys():
			self.value = value
			return
		raise ValueError("%s flag '%s' does not exist"%(self.description, value))
	def	__str__(self):
		return self.value
	def description(self):
		return self.values(self.value)
	def search(self, string):
		ret = [] #Return value holder
		for flag in self.values.keys():
			if self.values(flag).find(string) or flag.find(string):
				ret.append("%s : %s"%(flag, self.values(flag)))
		return ret

###COMPLETE###
class MFLAG(__flag__):
	"""
		Measurement flag
	"""
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

###COMPLETE###
class QFLAG(__flag__):
	"""
		Quality flag
	"""
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

	def __init__(self, value="NULL"):
		if not isinstance(value, str):
			raise TypeError("Expected type 'str' not '%s'"%( value.__class__.__name__))
		if not self.values[value]:
			raise ValueError("Code '%s' does not exist!")
		self.value=value
	def __str__(self):
		return self.value # It's already a string dumb dumb...
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
			if pair[0].find(string) or pair[1][0].find(string):
				ret.append(pair)
		return ret


### COMPLETE ###
class DAY(Dataset):
	"""
		Data value of a single day
	"""
	def __init__(self, value=-9999, mflag=" ", qflag=" ", sflag=" ", raw=None):
		if raw:
			raise UnimplementedError()
			return self.decode(raw)
		if not value:
			self.value=-9999
		else not isinstance(value, int):
			self.value=int(value) #this will handle the errors by itself
		if not mflag:
			self.m=MFLAG()
		elif isinstance(mflag, str):
			self.m=MFLAG()
	 	elif isinstance(mflag, MFLAG):
			self.m=mflag
		else:
			raise TypeError("Expected type 'str' or 'MFLAG' not '%s'"%( mflag.__class__.__name__,))
		if not qflag:
			self.q=QFLAG()
		elif isinstance(qflag, str):
			self.q=QFLAG()
	 	elif isinstance(qflag, QFLAG):
			self.q=qflag
		else:
			raise TypeError("Expected type 'str' or 'QFLAG' not '%s'"%( qflag.__class__.__name__,))
		if not sflag:
			self.s=SFLAG()
		elif isinstance(sflag, str):
			self.s=SFLAG()
	 	elif isinstance(sflag, SFLAG):
			self.s=sflag
		else:
			raise TypeError("Expected type 'str' or 'SFLAG' not '%s'"%( sflag.__class__.__name__,))
	def __str__(self):
		return str(self.value)

class STATION(Dataset):
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
	class GSNFLAG(__flag__):
		values={
			" ":"non-GSN station or WMO Station number not available",
			"GSN":"this station is part of the GCOS Surface Network (GSN)",
		}
	class NETFLAG(__flag__):
		values={
			" ":"Not a member of the U.S. Historical Climatology or U.S. Climate Reference Networks",
			"HCN":"This stations is part of the U.S. Historical Climatology Network",
			"CNR":"This stations is part of the U.S. Climate Reference Network or U.S. Regional Climate Network",
		}
	# NOTE: GSNFLAG, NETFLAG
	#	I just want to make it very clear I didn't want to implemement these flags as such
	#	and the only reason they have their own classes is because I wanted to keep some
	#	level of consistency in this damn API. I keep asking myself, couldn't these be combined?
	#	but I think the reason they aren't may be because a station can be a part of both GSN
	#	and something else.
	#
	length=86 #includes whitespace
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
	def __init__(self, id="NOTDEFINED", latitude=-9999.99,
		longitude=-9999.99, elevation=-999.9, state="NA",
		name="-----------------------------", gsn_flag=" ",
		hcn_crn_flag=" ", wmo_id="", raw=None):
		if raw:
			return self.decode(raw)
		if not id:
			self.id="NOTDEFINED"
		elif not isinstance(id, str):
			self.id=str(id)
		if not latitude:
			latitude=-9999.99
		elif not isinstance(latitude, float):
			self.latitude=float(latitude)
		if not longitude:
			self.longitude=-9999.99
		elif not isinstance(longitude, float):
			self.longitude=float(longitude)
		if not elevation:
			self.elevation=-999.9
		elif not isinstance(elevation, float):
			self.elevation=float(elevation)
		if not state:
			self.state="NA"
		elif not isinstance(state, str):
			self.state=str(state)
		if not name:
			self.name="-----------------------------"
		elif not isinstance(name, str):
			self.name=str(name)
		if not gsn_flag or not gsn_flag.strip():
			self.gsn=self.GSNFLAG()
		elif isinstance(gsn_flag, self.GSNFLAG):
			self.gsn=gsn_flag
		elif isinstance(gsn_flag, str):
			self.gsn=self.GSNFLAG(gsn_flag)
		else:
			raise TypeError("Expected type 'str' or 'STATION.GSNFLAG' not '%s'"%( gsn_flag.__class__.__name__,))
		if not hcn_crn_flag or not hcn_crn_flag.strip():
			self.net=self.NETFLAG()
		elif isinstance(hcn_crn_flag, self.NETFLAG):
			self.net=hcn_crn_flag
		elif isinstance(hcn_crn_flag, str):
			self.net=self.NETFLAG(hcn_crn_flag)
		else:
			raise TypeError("Expected type 'str' or 'STATION.NETFLAG' not '%s'"%( hcn_crn_flag.__class__.__name__,))

		raise UnimplementedError()
	def __str__():
		return self.encode()
	def decode(self, string):
		"""
			Directly converts an entire station entry
		"""
		if not isinstance(string, str):
			raise TypeError("Expected type 'str' not '%s'"%( string.__class__.__name__,))
		self.id=str(string[0,11])
		self.latitude=float(string[12,20])
		self.longitude=float(string[21,30])
		self.elevation=float(string[31,37])
		self.state=str(string[38,40])
		self.name=str(string[41,71])
		self.gsn=self.GSNFLAG(str(string[72,75]))
		self.net=self.NETFLAG(str(string[76,79]))
		self.wmo=str(string[80,85])
	def encode(self):
		out=_pad(self.id, 10)
		out+="  "+_pad(self.latitude, 8)
		out+="  "+_pad(self.longitude, 8)
		out+="  "+_pad(self.elevation, 6)
		out+="  "+_pad(self.state, 2)
		out+="  "+_pad(self.name, 30)
		out+="  "+_pad(self.gsn, 3)
		out+="  "+_pad(self.net, 3)
		out+="  "+_pad(self.wmo, 5)
		return out


class DAILY(Dataset):
	"""
		The daily dataset given by ghcn daily
	"""
	length=270 #including newline whitespace
	mask=__daily_mask__

	def __init__(self, days={}, id="NOTDEFINED", year=-999, month=-1, element="NULL", raw=None):
		if raw:
			return self.decode(raw)
		if not id:
			self.id="NOTDEFINED"
		elif not isinstance(id, str):
			self.id=str(id)
		if not year:
			self.year=-999
		elif not isinstance(year, int):
			self.year=int(year)
		if not month:
			self.month=-1
		elif not isinstance(month, int):
			self.month=int(month)
		if not element:
			self.element=ELEMENT()
		elif isinstance(element, str):
			self.element=ELEMENT(element)
		elif isinstance(element, ELEMENT):
			self.element=element
		else:
			self.element=ELEMENT(value=str(element))
		if not days:
			days={}
		elif not isinstance(days, dict):
			raise TypeError("days argument expected dict not '"+days.__class__.__name__+"'")
		for key in days.keys():
			if not key.isdecimal():
				raise ValueError("days must be decimal numbers; not strings, hex, octal or binary")
			if not isinstance(days[key], DAY):
				raise TypeError("daily values must be of type DAY not '"+days[key]__class__.__name__+"'")
		if int(days.keys()[0]) < 1 or int(reversed(days,keys())[0]) > 31:
			raise ValueError("day accessed outside of the monthly range (1 - 31)")
		self.day={x:DAY() for x in range(1,32)}
		self.day.update(days)
	def __str__(self):
		return self.encode()
	def decode(self, string):
		"""
			Directly converts an entire .dly entry
		"""
		if not isinstance(string, str):
			raise TypeError("Expected type 'str' not '"+string.__class__.__name__+"'")
		self.id=str(string[0:11])
		self.year=int(string[11:15])
		self.month=int(string[15:17])
		self.element=ELEMENT(str(string[17:21]))
		self.day={}
		for day in range(1,32):
			self.day[day] = DAY(value=string[21+((day-1)*8):21+((day-1)*8)+5],
				mflag=str(string[26+(day-1)*8]), #21+5+offset
				qflag=str(string[27+(day-1)*8]), #21+6+offset
				sflag=str(string[28+(day-1)*8])) #21+7+offset
		return
	def encode(self):
		out =  _pad(self.id, 10)
		out += _pad(self.year, 4)
		out += _pad(self.month, 2)
		out += _pad(self.element, 4)
		for d in self.day.values():
			out += _pad(d, 5)
			out += str(d.m)
			out += str(d.q)
			out += str(d.s)
		return out

class YEARLY(Dataset):
	"""
		the ghcn by_year dataset offered by the noaa
	"""
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
	def __init__(id="NOTDEFINED",
			date=datetime.datetime.utcnow().date(),
			element="NULL",
			value=0,
			mflag="",
			qflag="",
			sflag="",
			obstime=datetime.datetime.utcnow().time(),
			raw=None):
		if raw:
			return self.decode(raw)
		if not id:
			self.id=str()
		elif not isinstance(id, str):
			self.id=str(id)
		if not date:
			self.date=datetime.datetime.utcnow().date()
		elif isinstance(date, str):
			self.date=datetime.date(int(date[0,4]),int(date[4,6]),int(date[6,8]))
		elif isinstance(date, datetime.date):
			self.date=date
		else:
			raise TypeError("date argument expected str or datetime.date not '"+date.__class__.__name__+"'")
		if not element:
			self.element=ELEMENT()
		elif isinstance(element, str):
			self.element=ELEMENT(element)
		elif isinstance(element, ELEMENT):
			self.element=element
		else:
			self.element=ELEMENT(value=str(element))
		if not value:
			self.value=-9999
		elif not isinstance(value, int):
			self.value=int(value)
		if not mflag:
			self.m=MFLAG()
		elif isinstance(mflag, str):
			self.m=MFLAG()
	 	elif isinstance(mflag, MFLAG):
			self.m=mflag
		else:
			raise TypeError("Expected type 'str' or 'MFLAG' not '%s'"%( mflag.__class__.__name__,))
		if not qflag:
			self.q=QFLAG()
		elif isinstance(qflag, str):
			self.q=QFLAG()
	 	elif isinstance(qflag, QFLAG):
			self.q=qflag
		else:
			raise TypeError("Expected type 'str' or 'QFLAG' not '%s'"%( qflag.__class__.__name__,))
		if not sflag:
			self.s=SFLAG()
		elif isinstance(sflag, str):
			self.s=SFLAG()
	 	elif isinstance(sflag, SFLAG):
			self.s=sflag
		else:
			raise TypeError("Expected type 'str' or 'SFLAG' not '%s'"%( sflag.__class__.__name__,))
		if not obstime:
			self.obstime=datetime.datetime.utcnow().time()
		elif isinstance(obstime, str):
			self.obstime=datetime.time(int(obstime[0,2]), int(obstime[2,4]))
		elif isinstance(obstime, datetime.time):
			self.obstime=obstime
		else:
			raise TypeError("time argument expected str or datetime.time not '"+obstime.__class__.__name__+"'")
	def __str__(self):
		return self.encode()
	def encode(self):
		out=str(self.id)+","
		out+=self.date.strftime("%Y%m%d")+","
		out+=str(self.element)+","
		out+=str(self.value)+","
		out+=str(self.m)+","
		out+=str(self.q)+","
		out+=str(self.s)+","
		out+=self.obstime.strftime("%H%M")+","
		return out
	def decode(self, string):
		if not isinstance(string, str):
			raise TypeError("Expected type 'str' not '"+string.__class__.__name__+"'")
		f = string.split(",")
		if f.__len__() < self.fields.__len__():
			raise DatasetError("Chunk contains too many fields")
		self.id=f[0]
		self.date=datetime.date(f[1][0,4],f[1][4,6],f[1][6,8])
		self.element=ELEMENT(f[2])
		self.value=f[3]
		self.m=MFLAG(f[4])
		self.q=QFLAG(f[5])
		self.s=SFLAG(f[6])
		self.obstime=datetime.time(int(f[7][0,2]), int(f[7][2,4]))
		return

# SECTION: API functions
def search_by_mask(data, field, type):
	"""
		search for field in data by mask of "type"
	"""
	# Don't error check dummy, the bindings are already present because you
	# added them to the utils.Dataset constructor :P
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
def search_archive_by_mask():
	raise UnimplimentedError()
def search_archives_by_mask():
	raise UnimplementedError()
def daily_get_month():
	raise UnimplementedError()
def daily_get_year():
	raise UnimplementedError()
def daily_get_complete():
	raise UnimplementedError()
# SECTION: Database requests
def database_get_month(db, month):
	raise UnimplementedError
def database_get_year(db, year):
	raise UnimplementedError()
def database_init_ghcnd(db):
	"""
		GHCN-Daily explicit init
	"""
	db.get("ghcn/daily", "ghcnd-stations.txt")
	db.get("ghcn/daily", "ghcnd-countries.txt")
	db.get("ghcn/daily", "ghcnd-states.txt")
	db.get("ghcn/daily", "status.txt")
def database_init_ghcnm(db):
	"""
		GHCN-Monthly explicit init
	"""
	raise UnimplementedError()
def database_init_ghcn(db):
	"""
		GCHN complete init
	"""
	if not isinstance(db, core.Database)
	db.get("ghcn/daily", "ghcnd-stations.txt")
	db.get("ghcn/daily", "ghcnd-countries.txt")
	db.get("ghcn/daily", "ghcnd-states.txt")
	db.get("ghcn/daily", "status.txt")


# XXX:
#	Pass-by-refference preloader cleanup
#
del(__elements__, _soil_type, _depth_subcode, _weather_type, __subencode__)
del(__daily_mask__)

# SECTION: API tests
if __name__ == "__main__":
	# NOTE: Open test Resources
	import inspect
	import os
	import __init__ as core
	daily_dataset_test_case = open(os.path.dirname(os.path.abspath(
		inspect.stack()[0][1]))[0:40]+"res/ghcn_daily_gsn_test.dly")
	stations_file_test_case = open(os.path.dirname(os.path.abspath(
		inspect.stack()[0][1]))[0:40]+"res/ghcnd-stations.dat")

	# NOTE: Begin DAILY test cases
	#
