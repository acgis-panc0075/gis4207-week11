stop_id_to_buffer = {}
ws = r'E:\acgis\gis4207\data\Ottawa\Stops'
stop_id_field = arcpy.AddFieldDelimiters(ws, 'stop_id')
stop_name_field = arcpy.AddFieldDelimiters(ws, 'stop_name')
where_clause = f"{stop_id_field}='CI380'"
where_clause = f"{stop_name_field} LIKE '%GLADSTONE%'"
with arcpy.da.SearchCursor('Stops_UTM', 
                           ['stop_id','SHAPE@', 'stop_name'], 
                           where_clause=where_clause) as cursor:
    for row in cursor:
        stopid = row[0]
        shape = row[1]
        stop_id_to_buffer[stopid] = shape.buffer(150)

stop_id_to_DA_data = {}
for stopid in stop_id_to_buffer:
    stop_buffer = stop_id_to_buffer[stopid]
    intersected_da_data = []
    with arcpy.da.SearchCursor('OttawaDA_UTM', ['DACODE','POP_2016','SHAPE@']) as cursor:
        for row in cursor:            
            da_code = row[0]   
            population = row[1]
            da_poly = row[2] 
            dimension = 4  # Resulting geometry is a polygon
            if stop_buffer.overlaps(da_poly) == True:
                intersect_poly = stop_buffer.intersect(da_poly, 
                                                       dimension)
                data = (da_code, 
                        population, 
                        int(intersect_poly.area),
                        int(da_poly.area))
                intersected_da_data.append(data)
    stop_id_to_DA_data[stopid] = intersected_da_data

for stop_id in stop_id_to_DA_data:
    for data in stop_id_to_DA_data[stop_id]:
        print(stop_id, data)