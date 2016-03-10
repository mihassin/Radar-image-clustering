from owslib.wms import WebMapService
from owslib.csw import CatalogueServiceWeb
import numpy as np
import datetime, time, os


#estaplishes a connection to wms.fmi.fi with an api key
def wms_connection(api):
	domain = "http://wms.fmi.fi/"
	url = domain + "fmi-apikey/" + api + "/geoserver/wms"
	cnc = WebMapService(url, version='1.1.1')
	if cnc.identification.type != "OGC:WMS":
		return "error"
	return cnc


#establishes csw connenction to fmi.fi
def csw_connection():
	cnc = CatalogueServiceWeb('http://catalog.fmi.fi/geonetwork/srv/en/csw') # open for public, not api required 
	if cnc.identification.type != "OGC:WMS":
		return "error"
	return cnc


#creates a directory to system fs
def create_path(path_):
	if not os.path.exists(path_):
		os.makedirs(path_)


#rounds up info for image query
def getmap_info(obj, size, cnc):
	res = [[cnc[obj].title]]
	style = list(cnc["Radar:kuopio_dbzh"].styles)
	style.remove('raster')
	res.append(style[0:1])
	arr = ["EPSG:4326", cnc[obj].boundingBoxWGS84, size, "image/jpeg", True]
	res.extend(arr)
	return res


#returns essential values for a image request
def getmap(arr, cnc):
	return cnc.getmap(
		layers=arr[0],
		styles=arr[1],
		srs=arr[2],
		bbox=arr[3],
		size=arr[4],
		format=arr[5],
		transparent=arr[6]
		)


#saves and image on a disk
def to_jpg(fname, location, obj, size, cnc):
	arr = getmap_info(obj, size, cnc)
	img = getmap(arr, cnc)
	out = open(location+"/"+fname, 'wb')
	out.write(img.read())
	out.close()


#returns all measure type radar stations
def find(item, connection):
	res = np.array([])
	for a in list(connection.contents):
		if a.lower().count(item.lower()) > 0:
			res = np.append(res, a)
	return res


#saves all images with a specific type and size size
def lots_tojpg(which, size, cnc):
	for i in find(which, cnc):
		location  = "data/pics/"+str(size[0])+"x"+str(size[1])+"/"+which+"/"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
		create_path(location)
		filename = cnc[i].title+"_"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')+".jpg"
		to_jpg(filename, location, i, size, cnc)


#pulls all images from all radars with every type with a specific size
def save_all_radar_images(cnc, size):
	types = np.array(["dbzh", "etop_20", "vrad", "hclass"])
	for i in types: lots_tojpg(i, size, cnc)
