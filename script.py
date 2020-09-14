import geopandas as gpd


def select_by_intersect(df1, df2, unique_column):
    """
    Select features which intersect with another layer
    """
    # find the parts of features which fall within floods
    flooded_features = gpd.overlay(df1, df2, how='intersection')

    # select only one row for each unique feature
    unique_flooded_features = flooded_features.drop_duplicates(subset=unique_column)

    # get list of unique features which intersect
    unique_features = unique_flooded_features[unique_column].tolist()

    # create dataframe of the unique features
    flooded_features = df1[df1[unique_column].isin(unique_features)]

    return flooded_features


def main():
    """
    """
    # data location
    input_path = 'data/'
    output_path = 'outputs/'

    # load in data
    buildings = gpd.read_file(input_path+'buildings.shp', encoding='UTF-8')
    flooding = gpd.read_file(input_path+'flooding_example.geojson', encoding='UTF-8')

    # run select by location - find the buildings which fall in flood areas
    flooded_buildings = select_by_intersect(buildings, flooding, 'toid')

    # save flooded buildings to file
    if flooded_buildings.shape[0] > 0:
        flooded_buildings.to_file(output_path+'flooded_buildings.geojson', driver='GeoJSON')

    # load in nature reserves
    nature_reserves = gpd.read_file(input_path+'local_nature_reserves.geojson', encoding='UTF-8')

    # run select by location - find the reserves which fall in flood areas
    flooded_reserves = select_by_intersect(nature_reserves, flooding, 'OBJECTID')

    # save flooded reserves to file
    if flooded_reserves.shape[0] > 0:
        flooded_reserves.to_file(output_path+'flooded_reserves.geojson', driver='GeoJSON')

main()
