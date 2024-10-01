from osgeo import ogr
from qgis.core import QgsProject, QgsVectorLayer

release = "2024-09-18"
# themes = ["addresses", "base", "buildings", "divisions", "transportation"]
themes = ["buildings"]

for theme in themes:
    print(f"Adding {theme} data...")

    # Define the URL for the theme
    url = f"/vsicurl/https://overturemaps-tiles-us-west-2-beta.s3.amazonaws.com/{release}/{theme}.pmtiles"

    # Open the OGR datasource
    datasource = ogr.Open(url)

    if datasource is None:
        print(f"Failed to open {theme} data.")
        continue

    # Get the number of layers in the datasource
    layer_count = datasource.GetLayerCount()

    # Loop through all the layers and add them to the project
    for i in range(layer_count):
        layer = datasource.GetLayerByIndex(i)
        layer_name = layer.GetName()

        # Create a QgsVectorLayer for each OGR layer
        vector_layer = QgsVectorLayer(
            f"{url}|layername={layer_name}", f"{theme} - {layer_name}", "ogr"
        )

        if not vector_layer.isValid():
            print(f"Layer {layer_name} is invalid.")
            continue

        # Add the layer to the QGIS project
        QgsProject.instance().addMapLayer(vector_layer)
        print(f"Added {layer_name} from {theme}.")

print("Done!")
