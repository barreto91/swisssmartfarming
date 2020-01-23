#!../venv/bin/python2

import glob
from IPython import embed
from exif import Image
from geopy.point import Point
import shapely.geometry as shg
import geopandas as gpd
import os
import argparse

# parse the arguments
parser = argparse.ArgumentParser()


imgs_path = '/home/seba/polybox/Matterhorn.Project/Fields/FiBL/Rheinau/GPS Photos/20190604Rheinau Files/'

imgs_list = glob.glob(imgs_path + '*.jpg')

points = []
for img_name in imgs_list:
    with open(img_name, 'rb') as img:
        img = Image(img)
        lon = img.gps_longitude
        lat = img.gps_latitude
        location = "{} {}m {}s N {} {}m {}s E".format(lat[0], lat[1], lat[2],
            lon[0], lon[1], lon[2])
        point = Point(location)
        point = shg.Point(point.longitude, point.latitude)
        points.append(point)

# write the points to a shapefile
gsr = gpd.GeoSeries(points)
gsr.crs = {'init': 'epsg:4326'}
gsr = gsr.to_crs({'init': 'epsg:3857'})
save_path = '/media/seba/Samsung_2TB/AgriCircle/Rheinau/Shapes'
file_name = 'samples.shp'

if not os.path.exists(save_path):
    os.mkdir(save_path)

gsr.to_file(os.path.join(save_path, file_name))