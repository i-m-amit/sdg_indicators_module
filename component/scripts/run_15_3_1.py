from zipfile import ZipFile

import ee
import geemap
from ipywidgets import Output
import ipyvuetify as v
import geopandas as gpd
import pandas as pd

from component import parameter as pm

from .gdrive import gdrive
from .gee import wait_for_completion
from .download import digest_tiles
from .integration import * 
from .productivity import *
from .soil_organic_carbon import *
from .land_cover import *

ee.Initialize()

def download_maps(aoi_io, io, output):
    
    # get the export scale 
    scale = 10 if 'Sentinel 2' in io.sensors else 30
        
    # create the export path
    land_cover_desc = f'{aoi_io.get_aoi_name()}_land_cover'
    soc_desc = f'{aoi_io.get_aoi_name()}_soc'
    productivity_desc = f'{aoi_io.get_aoi_name()}_productivity'
    indicator_desc = f'{aoi_io.get_aoi_name()}_indicator_15_3_1'
        
    # load the drive_handler
    drive_handler = gdrive()
    
    # clip the images if it's an administrative layer and keep the bounding box if not
    if aoi_io.feature_collection:
        geom = aoi_io.get_aoi_ee().geometry()
        land_cover = io.land_cover.clip(geom)
        soc = io.soc.clip(geom)
        productivity = io.productivity.clip(geom)
        indicator = io.indicator_15_3_1.clip(geom)
    else:
        land_cover = io.land_cover
        soc = io.soc
        productivity = io.productivity
        indicator = io.indicator_15_3_1
        
    # download all files
    downloads = drive_handler.download_to_disk(land_cover_desc, land_cover, aoi_io, output)
    downloads = drive_handler.download_to_disk(soc_desc, soc, aoi_io, output)
    downloads = drive_handler.download_to_disk(productivity_desc, productivity, aoi_io, output)
    downloads = drive_handler.download_to_disk(indicator_desc, indicator, aoi_io, output)
        
    # I assume that they are always launch at the same time 
    # If not it's going to crash
    if downloads:
        wait_for_completion([land_cover_desc, soc_desc, productivity_desc, indicator_desc], output)
    output.add_live_msg('GEE tasks completed', 'success') 
    
    # create merge names 
    land_cover_merge = pm.result_dir.joinpath(f'{land_cover_desc}_merge.tif')
    soc_merge = pm.result_dir.joinpath(f'{soc_desc}_merge.tif')
    productivity_merge = pm.result_dir.joinpath(f'{productivity_desc}_merge.tif')
    indicator_merge = pm.result_dir.joinpath(f'{indicator_desc}_merge.tif')
    
    # digest the tiles
    digest_tiles(aoi_io, land_cover_desc, pm.result_dir, output, land_cover_merge)
    digest_tiles(aoi_io, soc_desc, pm.result_dir, output, soc_merge)
    digest_tiles(aoi_io, productivity_desc, pm.result_dir, output, productivity_merge)
    digest_tiles(aoi_io, indicator_desc, pm.result_dir, output, indicator_merge)
        
    # remove the files from drive
    drive_handler.delete_files(drive_handler.get_files(land_cover_desc))
    drive_handler.delete_files(drive_handler.get_files(soc_desc))
    drive_handler.delete_files(drive_handler.get_files(productivity_desc))
    drive_handler.delete_files(drive_handler.get_files(indicator_desc))
        
    #display msg 
    output.add_live_msg('Download complete', 'success')

    return (land_cover_merge, soc_merge, productivity_merge, indicator_merge)

def display_maps(aoi_io, io, m, output):
    
    m.zoom_ee_object(aoi_io.get_aoi_ee().geometry())
    
    # get the geometry to clip on 
    geom = aoi_io.get_aoi_ee().geometry()
    # clip on the bounding box when we use a custom aoi
    if aoi_io.assetId: 
        geom = geom.bounds()
        
    # add the layers
    m.addLayer(io.productivity.clip(geom), pm.viz_prod, 'productivity')
    #m.addLayer(io.land_cover.select('degredation').clip(geom), pm.viz_lc, 'land_cover')
    #m.addLayer(io.soc.clip(geom), pm.viz_soc, 'soil_organic_carbon')
    #m.addLayer(io.indicator_15_3_1.clip(geom), pm.viz_indicator, 'indicator_15_3_1')
        
    # add the aoi on the map 
    #m.addLayer(aoi_io.get_aoi_ee(), {'color': v.theme.themes.dark.info}, 'aoi')
    
    return 

def compute_indicator_maps(aoi_io, io, output):
    
    # raise an error if the years are not in the rigth order 
    if not (io.start < io.target_start < io.end):
        raise Exception('the years are not in the right order')
    
    # compute intermediary maps 
    ndvi_int, climate_int = integrate_ndvi_climate(aoi_io, io, output)
    prod_trajectory = productivity_trajectory(io, ndvi_int, climate_int, output)
    prod_performance = productivity_performance(aoi_io, io, ndvi_int, climate_int, output)
    prod_state = productivity_state(aoi_io, io, ndvi_int, climate_int, output) 
    
    io.productivity = prod_trajectory
    # compute result maps 
    io.land_cover = land_cover(io, aoi_io, output)
    io.soc = soil_organic_carbon(io, aoi_io, output)
    #io.productivity = productivity_final(prod_trajectory, prod_performance, prod_state, output)
    
    # sump up in a map
    io.indicator_15_3_1 = indicator_15_3_1(io.productivity, io.land_cover, io.soc, output)

    return 

def compute_zonal_analysis(aoi_io, io, output):
    
    indicator_stats = pm.result_dir.joinpath(f'{aoi_io.get_aoi_name()}_indicator_15_3_1')
        
    output_widget = Output()
    output.add_msg(output_widget)
        
    indicator_csv = indicator_stats.with_suffix('.csv') # to be removed when moving to shp
    with output_widget:
        geemap.zonal_statistics_by_group(
            in_value_raster = io.indicator_15_3_1,
            in_zone_vector = aoi_io.get_aoi_ee(),
            out_file_path = indicator_csv,
            statistics_type = "PERCENTAGE",
            decimal_places=2,
            tile_scale=1.0
        )
    # this should be removed once geemap is repaired
    #########################################################################
    aoi_json = geemap.ee_to_geojson(aoi_io.get_aoi_ee())
    aoi_gdf = gpd.GeoDataFrame.from_features(aoi_json).set_crs('EPSG:4326')
    indicator_df = pd.read_csv(indicator_csv)
    aoi_gdf['Class_sum'] = indicator_df.Class_sum
    aoi_gdf.to_file(indicator_stats.with_suffix('.shp'))
    #########################################################################
    
    # get all the shp extentions
    suffixes = ['.dbf', '.prj', '.shp', '.cpg', '.shx'] # , '.fix']
    
    # write the zip file
    indicator_zip = indicator_stats.with_suffix('.zip')
    with ZipFile(indicator_zip, 'w') as myzip:
        for suffix in suffixes:
            file = indicator_stats.with_suffix(suffix)
            myzip.write(file, file.name)
        
    return indicator_zip
    

def indicator_15_3_1(productivity, landcover, soc, output):
    
    landcover = landcover.select('degredation')

    indicator = ee.Image(0) \
        .where(productivity.eq(3).And(landcover.eq(3)).And(soc.eq(3)),3) \
        .where(productivity.eq(3).And(landcover.eq(3)).And(soc.eq(2)),3) \
        .where(productivity.eq(3).And(landcover.eq(3)).And(soc.eq(1)),1) \
        .where(productivity.eq(3).And(landcover.eq(2)).And(soc.eq(3)),3) \
        .where(productivity.eq(3).And(landcover.eq(2)).And(soc.eq(2)),3) \
        .where(productivity.eq(3).And(landcover.eq(2)).And(soc.eq(1)),1) \
        .where(productivity.eq(3).And(landcover.eq(1)).And(soc.eq(3)),1) \
        .where(productivity.eq(3).And(landcover.eq(1)).And(soc.eq(2)),1) \
        .where(productivity.eq(3).And(landcover.eq(1)).And(soc.eq(1)),1) \
        .where(productivity.eq(2).And(landcover.eq(3)).And(soc.eq(3)),3) \
        .where(productivity.eq(2).And(landcover.eq(3)).And(soc.eq(2)),3) \
        .where(productivity.eq(2).And(landcover.eq(3)).And(soc.eq(1)),1) \
        .where(productivity.eq(2).And(landcover.eq(2)).And(soc.eq(3)),3) \
        .where(productivity.eq(2).And(landcover.eq(2)).And(soc.eq(2)),2) \
        .where(productivity.eq(2).And(landcover.eq(2)).And(soc.eq(1)),1) \
        .where(productivity.eq(2).And(landcover.eq(1)).And(soc.eq(3)),1) \
        .where(productivity.eq(2).And(landcover.eq(1)).And(soc.eq(2)),1) \
        .where(productivity.eq(2).And(landcover.eq(1)).And(soc.eq(1)),1) \
        .where(productivity.eq(1).And(landcover.eq(3)).And(soc.eq(3)),1) \
        .where(productivity.eq(1).And(landcover.eq(3)).And(soc.eq(2)),1) \
        .where(productivity.eq(1).And(landcover.eq(3)).And(soc.eq(1)),1) \
        .where(productivity.eq(1).And(landcover.eq(2)).And(soc.eq(3)),1) \
        .where(productivity.eq(1).And(landcover.eq(2)).And(soc.eq(2)),1) \
        .where(productivity.eq(1).And(landcover.eq(2)).And(soc.eq(1)),1) \
        .where(productivity.eq(1).And(landcover.eq(1)).And(soc.eq(3)),1) \
        .where(productivity.eq(1).And(landcover.eq(1)).And(soc.eq(2)),1) \
        .where(productivity.eq(1).And(landcover.eq(1)).And(soc.eq(1)),1) \
        .where(productivity.eq(1).And(landcover.lt(1)).And(soc.lt(1)),1) \
        .where(productivity.lt(1).And(landcover.eq(1)).And(soc.lt(1)),1) \
        .where(productivity.lt(1).And(landcover.lt(1)).And(soc.eq(1)),1) \
        .where(productivity.eq(2).And(landcover.lt(1)).And(soc.lt(1)),2) \
        .where(productivity.lt(0).And(landcover.eq(2)).And(soc.lt(1)),2) \
        .where(productivity.lt(0).And(landcover.lt(1)).And(soc.eq(2)),2) \
        .where(productivity.eq(3).And(landcover.lt(1)).And(soc.lt(1)),3) \
        .where(productivity.lt(1).And(landcover.eq(3)).And(soc.lt(1)),3) \
        .where(productivity.lt(1).And(landcover.lt(1)).And(soc.eq(3)),3)
    
    return indicator.uint8()
