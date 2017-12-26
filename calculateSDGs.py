import arcgis
URL = 'https://services1.arcgis.com/k8WRSCmxGgCwZufI/ArcGIS/rest/services/Departments/FeatureServer/1'

departmentsFL = arcgis.features.FeatureLayer(URL) # Create the feature layer object

def getSDGs():

    # Get the IDs from departments
    departmentsIDs = departmentsFL.query(return_ids_only=True)['objectIds']
    departmentsDic = {}

    for IDs in departmentsIDs:
        listSDG = []
        relatedActions = departmentsFL.query_related_records(IDs, '0', out_fields='SDG', return_geometry=False)
        for SDG in relatedActions['relatedRecordGroups'][0]['relatedRecords']:
            listSDG.append(SDG['attributes']['SDG'])
        departmentsDic[str(IDs)] = listSDG

    return departmentsDic

def update_departments(departmentsDic):

    departmentsRecordSet = departmentsFL.query(where='1=1', return_geometry=False, out_fields= 'OBJECTID,SDG_Totals,SDG1,SDG2,SDG3,SDG4,SDG5,SDG6,SDG7,SDG8,SDG9,SDG10,SDG11,SDG12,SDG13,SDG14,SDG15,SDG16,SDG17')

    for record in departmentsRecordSet:
        SDGinRecord = departmentsDic[str(record.get_value('OBJECTID'))]
        record.set_value('SDG_Totals',len(SDGinRecord))
        record.set_value('SDG1',SDGinRecord.count('01'))
        record.set_value('SDG2',SDGinRecord.count('02'))
        record.set_value('SDG3',SDGinRecord.count('03'))
        record.set_value('SDG4',SDGinRecord.count('04'))
        record.set_value('SDG5',SDGinRecord.count('05'))
        record.set_value('SDG6',SDGinRecord.count('06'))
        record.set_value('SDG7',SDGinRecord.count('07'))
        record.set_value('SDG8',SDGinRecord.count('08'))
        record.set_value('SDG9',SDGinRecord.count('09'))
        record.set_value('SDG10',SDGinRecord.count('10'))
        record.set_value('SDG11',SDGinRecord.count('11'))
        record.set_value('SDG12',SDGinRecord.count('12'))
        record.set_value('SDG13',SDGinRecord.count('13'))
        record.set_value('SDG14',SDGinRecord.count('14'))
        record.set_value('SDG15',SDGinRecord.count('15'))
        record.set_value('SDG16',SDGinRecord.count('16'))
        record.set_value('SDG17',SDGinRecord.count('17'))

    return departmentsRecordSet

SDG_data = getSDGs()
new_departments = update_departments(SDG_data)
departmentsFL.edit_features(updates=new_departments)
