import arcgis

gisuser = arcgis.gis.GIS(username="un_haiti", password="ubikgsuj1")

# URL = 'https://services1.arcgis.com/k8WRSCmxGgCwZufI/ArcGIS/rest/services/Departments/FeatureServer/1'
URLactions = 'https://services8.arcgis.com/iMDawfh419rT2dQQ/arcgis/rest/services/SDGs/FeatureServer/0'
URLcomments = 'https://services8.arcgis.com/iMDawfh419rT2dQQ/arcgis/rest/services/SDGs/FeatureServer/3'

actionsFL = arcgis.features.FeatureLayer(URLactions, gis=gisuser)  # Create the feature layer object
commentsFL = arcgis.features.FeatureLayer(URLcomments, gis=gisuser)  # Create the feature layer object
# newCommentsQuery = commentsFL.query(where='created_date BETWEEN CURRENT_TIMESTAMP - 0.041666666666666664 AND CURRENT_TIMESTAMP', out_fields='RelatedAction')
querycomments = "IsPublic = 'No'"
newCommentsQuery = commentsFL.query(where=querycomments, out_fields='RelatedAction')
newComments = []

for relatedAction in newCommentsQuery:
    newComments.append(relatedAction.attributes['OBJECTID'])

newIDs = []

for relatedID in newComments:
    actionWithNewCommentsQuery = commentsFL.query_related_records(relatedID, 0, out_fields='*', return_geometry=False)
    newIDs.append(actionWithNewCommentsQuery['relatedRecordGroups'][0]['relatedRecords'][0]['attributes']['OBJECTID'])

if len(newIDs) == 0:
    print('no new comments found')

else:

    print('found ' + str(len(newIDs)) + ' new comments.  processing...')
    noDuplicatesIDs = []

    for i in newIDs:
        if i not in noDuplicatesIDs:
            noDuplicatesIDs.append(i)

    noDuplicatesIDs.sort()

    idsForQuery = ''.join(str(e) + ', ' for e in noDuplicatesIDs)
    query = 'OBJECTID in (' + idsForQuery[:-2] + ')'

    actionsRecordSet = actionsFL.query(where=query, out_fields='NewComment', return_geometry=False)

    for record in actionsRecordSet:
        record.set_value('NewComment', 'Yes')

    actionsFL.edit_features(updates=actionsRecordSet)

    print('update completed. ' + str(len(newIDs)) + ' processed')
