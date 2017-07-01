# python3-noaa

This project is implemented to provide users with more elaborate access the NOAA's vast database,
including managers for all of the different datasets comprised therein.

### Project Format:

The sections of this API are divided as such,
	1. primary database connections and workings are made available by the root package
	2. each separate interface is connected to the noaa tree via a sub-module
	3. the seperate interface sub-modules offer functions for interactions with direct data
	4. and implement classes for custom data interaction if desired

We're choosing this format because it's the most like the raw interface offered by the NOAA
meaning we don't have to re-engineer the API, we just have to re-implement it for client side interaction.

### Database Assets:
*Unmarked is incomplete, marked is finished.*
 * [] NOAA Database (Project core)
 * [] GHCN

### Afterthoughts:

We wanted to offer a custom database API. However, the NOAA is an international nonprofit dedicated to collecting real weather data and if there was a fraudulent NOAA clone somewhere hosting a bunch of madness for disproving global warming or whatever; we really don't want to take that chance. Sure, you could say we're lazy. But the reality is, we're just paranoid as hell after the 2016 election disaster...
