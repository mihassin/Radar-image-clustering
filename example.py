from owslib.wms import WebMapService as wms
import numpy as np
import datetime
import time
import os

def connect(api):
	domain = "http://wms.fmi.fi/"
	url = domain + "fmi-apikey/" + api + "/geoserver/wms"
	cnc = wms(url, version='1.1.1')
	if cnc.identification.type != "OGC:WMS":
		return "error"
	return cnc

def find(item, connection):
	res = np.array([])
	for a in list(connection.contents):
		if a.lower().count(item.lower()) > 0:
			res = np.append(res, a)
	return res

def create_path(path_):
	if not os.path.exists(path_):
		os.makedirs(path_)

def getmap_info(obj, cnc):
	res = [[cnc[obj].title]]
	res.append(list(cnc["Radar:kuopio_dbzh"].styles)[1:2])
	arr = ["EPSG:4326", cnc[obj].boundingBoxWGS84, (720,480), "image/jpeg", True]
	res.extend(arr)
	return res

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

def to_jpg(fname, location, obj, cnc):
	arr = getmap_info(obj, cnc)
	img = getmap(arr, cnc)
	out = open(location+"/"+fname, 'wb')
	out.write(img.read())
	out.close()

def lots_tojpg(which, cnc):
	for i in find(which, cnc):
		location  = "data/pics/"+which+"/"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
		create_path(location)
		filename = cnc[i].title+"_"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')+".jpg"
		to_jpg(filename, location, i, cnc)

def pull_all_radar_images(cnc):
	lots_tojpg("dbzh", cnc)
	lots_tojpg("etop_20",cnc)
	lots_tojpg("vrad",cnc)
	lots_tojpg("hclass", cnc)

'''

    radar reflectivity (dbz)
    radial velocity (vrad)
    rain classification (hclass)
    cloud top height (etop_20)
    
'''

