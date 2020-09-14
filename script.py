import geopandas as gpd


def main():
    """
    """

    # load in data
    buildings = gpd.read_file('buildings_E08000021/buildings.geojson', encoding='UTF-8')
    flooding = gpd.read_file('flooding_example.geojson', encoding='UTF-8')

    # find the parts of buildings which fall within floods
    flooded_buildings = gpd.overlay(buildings, flooding, how='intersection')

    # select only one row for each toid
    unique_flooded_buildings = flooded_buildings.drop_duplicates(subset='toid')

    # get list of unique toids (buildings)
    affected_buildings_toid = unique_flooded_buildings['toid'].tolist()

    # create dataframe of the unique flooded buildings
    unique_flooded_buildings = buildings[buildings['toid'].isin(affected_buildings_toid)]

    # save flooded buildings to file
    unique_flooded_buildings.to_file('flooded_buildings.geojson', driver='GeoJSON')

main()
