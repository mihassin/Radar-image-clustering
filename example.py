from owslib.wms import WebMapService as wms
import sys

def connection(api):
	domain = "http://wms.fmi.fi/"
	url = domain + "fmi-apikey/" + api + "/geoserver/wms"
	cnc = wms(url, version='1.1.1')
	if cnc.identification.type != "OGC:WMS":
		return "error"
	return cnc