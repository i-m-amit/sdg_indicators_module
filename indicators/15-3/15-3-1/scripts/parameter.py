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

######################
##      matrix      ##
######################

IPCC_matrix = [
    11, 12, 13, 14, 15, 16, 17,
    21, 22, 23, 24, 25, 26, 27,
    31, 32, 33, 34, 35, 36, 37,
    41, 42, 43, 44, 45, 46, 47,
    51, 52, 53, 54, 55, 56, 57,
    61, 62, 63, 64, 65, 66, 67,
    71, 72, 73, 74, 75, 76, 77
]

###############################
##      named parameter      ##
###############################

trajectories = ['ndvi_trend', 'p_restrend', 's_restrend', 'ue_trend']

#############################
##      kendall coeff      ##
#############################

def get_kendall_coef(n, level=95):
    """ retreive the kendalls coeffs"""
    
    # The minus 4 is because the indexing below for a sample size of 4
    assert(n >= 4)
    n = n - 4
    
    coefs = {90: [4, 6, 7, 9, 10, 12, 15, 17, 18, 22, 23, 27, 28, 32, 35, 37, 40, 42, 45, 49, 52, 56, 59, 61, 66, 68, 73, 75, 80, 84, 87, 91, 94, 98, 103, 107, 110, 114, 119, 123, 128, 132, 135, 141, 144, 150, 153, 159, 162, 168, 173, 177, 182, 186, 191, 197, 202],
             95: [4, 6, 9, 11, 14, 16, 19, 21, 24, 26, 31, 33, 36, 40, 43, 47, 50, 54, 59, 63, 66, 70, 75, 79, 84, 88, 93, 97, 102, 106, 111, 115, 120, 126, 131, 137, 142, 146, 151, 157, 162, 168, 173, 179, 186, 190, 197, 203, 208, 214, 221, 227, 232, 240, 245, 251, 258],
             99: [6, 8, 11, 18, 22, 25, 29, 34, 38, 41, 47, 50, 56, 61, 65, 70, 76, 81, 87, 92, 98, 105, 111, 116, 124, 129, 135, 142, 150, 155, 163, 170, 176, 183, 191, 198, 206, 213, 221, 228, 236, 245, 253, 260, 268, 277, 285, 294, 302, 311, 319, 328, 336, 345, 355, 364]
            }
    
    return coefs[level][n]

########################################
##      vizualization parameters      ##
########################################

viz_trajectory = {"max": 3, "min":-3,"palette":["#762a83","#af8dc3","#e7d4e8","#f7f7f7","#d9f0d3","#7fbf7b","#1b7837"]}
