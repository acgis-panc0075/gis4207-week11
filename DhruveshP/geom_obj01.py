import arcpy
import sys
import os
import time

def create_polyline_feature_class(input_file, output_shp):
    input_file = "E:\acgis\gis4207_prog\Data"
    arcpy.env.overwriteOutput = True

    arcpy.management.CreateFeatureclass(os.path.dirname(output_shp), os.path.basename(output_shp), "POLYLINE", spatial_reference=arcpy.SpatialReference(4326))

    with open(input_file, 'r') as file:
        start_time = time.perf_counter()

        with arcpy.da.InsertCursor(output_shp, ["SHAPE@"]) as cursor:
            array = arcpy.Array()
            for line in file:
                line = line.strip()
                parts = line.split()

                if parts and parts[0].isdigit():
                    if array:
                        cursor.insertRow([arcpy.Polyline(array)])
                        array.removeAll()

                else:
                    point = arcpy.Point(float(parts[0]), float(parts[1]))
                    array.add(point)

            if array:
                cursor.insertRow([arcpy.Polyline(array)])

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Process completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: geom_obj01.py in_txt out_shp")
    else:
        input_file = sys.argv[1]
        output_shp = sys.argv[2]
        create_polyline_feature_class(input_file, output_shp)
