from pathlib import Path

import numpy as np

result_dir = Path('~', 'downloads', 'sdg_indicators').expanduser()

##########################
##      staellites      ##
##########################

# first images year
L4_start = 1982

# max year for land use 
land_use_max_year = 2018

lc_first_year = 1992
lc_last_year = 2015

# name of the sensor, GEE asset
sensors = {
        'Landsat 4': 'LANDSAT/LT04/C01/T1_SR',
        'Landsat 5': 'LANDSAT/LT05/C01/T1_SR',
        'Landsat 7': 'LANDSAT/LE07/C01/T1_SR', 
        'Landsat 8': 'LANDSAT/LC08/C01/T1_SR', 
        'Sentinel 2': 'COPERNICUS/S2'
}

precipitation = 'NOAA/PERSIANN-CDR'

land_cover = "users/geflanddegradation/toolbox_datasets/lcov_esacc_1992_2018"
soil_tax = "users/geflanddegradation/toolbox_datasets/soil_tax_usda_sgrid"
soc = "users/geflanddegradation/toolbox_datasets/soc_sgrid_30cm"
ipcc_climate_zones = "users/geflanddegradation/toolbox_datasets/ipcc_climate_zones"

######################
##      matrix      ##
######################

default_trans_matrix = [
    [0, -1, -1, -1, -1, -1, 0], # Tree-covered
    [1, 0, 1, -1, -1, -1, 0], # grassland
    [1, -1, 0, -1, -1, -1, 0], # cropland
    [-1, -1, -1, 0, -1, -1, 0], # wetland
    [1, 1, 1, 1, 0, 1, 0], # artificial
    [1, 1, 1, 1, -1, 0, 0,], # Other land
    [0, 0, 0, 0, 0, 0, 0] # water body 
]

IPCC_lc_change_matrix = [
    11, 12, 13, 14, 15, 16, 17,
    21, 22, 23, 24, 25, 26, 27,
    31, 32, 33, 34, 35, 36, 37,
    41, 42, 43, 44, 45, 46, 47,
    51, 52, 53, 54, 55, 56, 57,
    61, 62, 63, 64, 65, 66, 67,
    71, 72, 73, 74, 75, 76, 77
]

ESA_lc_classes = [
    10, 11, 12, 20 , 30, 40, 50, 60, 61, 62, 70, 
    71, 72, 80, 81, 82, 90, 100, 160, 170, 110, 
    130, 180, 190, 120, 121, 122, 140, 150, 151,     
    152, 153, 200, 201, 202, 210
]

reclassification_matrix = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 
    16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 
    29, 30, 31, 32, 33, 34, 35, 36
]

translation_matrix = [
    [10, 11, 12, 20, 30, 40, 50, 60, 61, 62, 70, 
    71, 72, 80, 81, 82, 90, 100, 110, 120, 121, 
    122, 130, 140, 150, 151, 152, 153, 160, 170, 
    180, 190, 200, 201, 202, 210, 220],
    [3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 
    1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 
    2, 2, 2, 2, 4, 4, 4, 5, 6, 6, 6, 7, 6]
]
sequential_matrix = [
    1, 12, 13, 14, 15, 16, 17,
    21, 2, 23, 24, 25, 26, 27,
    31, 32, 3, 34, 35, 36, 37,
    41, 42, 43, 4, 45, 46, 47,
    51, 52, 53, 54, 5, 56, 57,
    61, 62, 63, 64, 65, 6, 67,
    71, 72, 73, 74, 75, 76, 7
]



climate_conversion_matrix = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    [0, 0.69, 0.8, 0.69, 0.8, 0.69, 0.8, 0.69, 0.8, 0.64, 0.48, 0.48, 0.58]
]
        
c_conversion_factor = [
    1, 1, 333, 1, 0.1, 0.1, 1,
    1, 1, 333, 1, 0.1, 0.1, 1,
    -333, -333, 1, 1 / 0.71, 0.1, 
    0.1, 1, 1, 1, 0.71, 1, 0.1, 
    0.1, 1, 2, 2, 2, 2, 1, 1,
    1, 2, 2, 2, 2, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1
]

management_factor = [
    1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1
]


input_factor = [
    1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1
]


###############################
##      named parameter      ##
###############################

trajectories = ['ndvi_trend', 'p_restrend', 's_restrend', 'ue_trend']

climate_regimes = [
    {'text': 'Temperate dry (coef = 0.8)',    'value': 0.80},
    {'text': 'Temperate moist (coef = 0.69)', 'value': 0.69},
    {'text': 'Tropical dry (coef = 0.58)',    'value': 0.58},
    {'text': 'Tropical moist (coef = 0.48)',  'value': 0.48},
    {'text': 'Tropical montane (coef = 0.64)','value': 0.64}
]

#############################
##      kendall coeff      ##
#############################

def get_kendall_coef(n, level=95):
    """ retreive the kendalls coeffs"""
    
    # The minus 4 is because the indexing below for a sample size of 4
    assert(n >= 4)
    n = n - 4
    
    coefs = {
        90: [4, 6, 7, 9, 10, 12, 15, 17, 18, 22, 23, 27, 28, 32, 35, 37, 40, 42, 45, 49, 52, 56, 59, 61, 66, 68, 73, 75, 80, 84, 87, 91, 94, 98, 103, 107, 110, 114, 119, 123, 128, 132, 135, 141, 144, 150, 153, 159, 162, 168, 173, 177, 182, 186, 191, 197, 202],
        95: [4, 6, 9, 11, 14, 16, 19, 21, 24, 26, 31, 33, 36, 40, 43, 47, 50, 54, 59, 63, 66, 70, 75, 79, 84, 88, 93, 97, 102, 106, 111, 115, 120, 126, 131, 137, 142, 146, 151, 157, 162, 168, 173, 179, 186, 190, 197, 203, 208, 214, 221, 227, 232, 240, 245, 251, 258],
        99: [6, 8, 11, 18, 22, 25, 29, 34, 38, 41, 47, 50, 56, 61, 65, 70, 76, 81, 87, 92, 98, 105, 111, 116, 124, 129, 135, 142, 150, 155, 163, 170, 176, 183, 191, 198, 206, 213, 221, 228, 236, 245, 253, 260, 268, 277, 285, 294, 302, 311, 319, 328, 336, 345, 355, 364]
    }
    
    return coefs[level][n]

########################################
##      vizualization parameters      ##
########################################

viz = {"max": 1, "min":-1,"palette":["#F99B72","#F9F372","#12C341"]}

##############################
##      useful numbers      ##
##############################

int_16_min = np.iinfo(np.int16).min
