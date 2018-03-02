import arcgis

def getJenksBreaks( dataList, numClass ):
    dataList.sort()
    mat1 = []
    for i in range(0,len(dataList)+1):
        temp = []
        for j in range(0,numClass+1):
            temp.append(0)
        mat1.append(temp)
    mat2 = []
    for i in range(0,len(dataList)+1):
        temp = []
        for j in range(0,numClass+1):
            temp.append(0)
        mat2.append(temp)
    for i in range(1,numClass+1):
        mat1[1][i] = 1
        mat2[1][i] = 0
        for j in range(2,len(dataList)+1):
            mat2[j][i] = float('inf')
    v = 0.0
    for l in range(2,len(dataList)+1):
        s1 = 0.0
        s2 = 0.0
        w = 0.0
        for m in range(1,l+1):
            i3 = l - m + 1
            val = float(dataList[i3-1])
            s2 += val * val
            s1 += val
            w += 1
            v = s2 - (s1 * s1) / w
            i4 = i3 - 1
            if i4 != 0:
              for j in range(2,numClass+1):
                if mat2[l][j] >= (v + mat2[i4][j - 1]):
                  mat1[l][j] = i3
                  mat2[l][j] = v + mat2[i4][j - 1]
        mat1[l][1] = 1
        mat2[l][1] = v
    k = len(dataList)
    kclass = []
    for i in range(0,numClass+1):
        kclass.append(0)
    kclass[numClass] = float(dataList[len(dataList) - 1])
    countNum = numClass
    while countNum >= 2:  #print "rank = " + str(mat1[k][countNum])
        id = int((mat1[k][countNum]) - 2)
        # print "val = " + str(dataList[id])
        kclass[countNum - 1] = dataList[id]
        k = int((mat1[k][countNum] - 1))
        countNum -= 1
    return kclass


gisuser = arcgis.gis.GIS(username="un_haiti", password="ubikgsuj1")
URL = 'https://services8.arcgis.com/iMDawfh419rT2dQQ/arcgis/rest/services/SDGs/FeatureServer/1'

departmentsFL = arcgis.features.FeatureLayer(URL, gis=gisuser) # Create the feature layer object
departmentsTotals = departmentsFL.query(return_geometry=False, out_fields='SDG_Totals')
totalsDictionary = departmentsTotals.to_dict()

dataList = []
for DepartmentRow in totalsDictionary['features']:
    dataList.append(DepartmentRow['attributes']['SDG_Totals'])

result = getJenksBreaks(dataList, 4)
resultSorted = sorted(result)
print(resultSorted)

# Create break values and labels
break0 = int(resultSorted[1])
label0 = "0 - " + str(break0)
break1 = int(resultSorted[2])
label1 = str(break0) + " - " + str(break1)
break2 = int(resultSorted[3])
label2 = str(break1) + " - " + str(break2)
break3 = int(resultSorted[4])
label3 = str(break2) + " - " + str(break3)

# bring webmap
webmapItem = "6ed1633b7839452fbd81455c411d22ab"

item = arcgis.gis.Item(gisuser, webmapItem, itemdict=None)
totalActionsMap = arcgis.mapping.WebMap(item)

# modify webmap
# breaks
totalActionsMap['operationalLayers'][0]['layerDefinition']['drawingInfo']['renderer']['classBreakInfos'][0]['classMaxValue'] = break0
totalActionsMap['operationalLayers'][0]['layerDefinition']['drawingInfo']['renderer']['classBreakInfos'][1]['classMaxValue'] = break1
totalActionsMap['operationalLayers'][0]['layerDefinition']['drawingInfo']['renderer']['classBreakInfos'][2]['classMaxValue'] = break2
totalActionsMap['operationalLayers'][0]['layerDefinition']['drawingInfo']['renderer']['classBreakInfos'][3]['classMaxValue'] = break3

# labels
totalActionsMap['operationalLayers'][0]['layerDefinition']['drawingInfo']['renderer']['classBreakInfos'][0]['label'] = label0
totalActionsMap['operationalLayers'][0]['layerDefinition']['drawingInfo']['renderer']['classBreakInfos'][1]['label'] = label1
totalActionsMap['operationalLayers'][0]['layerDefinition']['drawingInfo']['renderer']['classBreakInfos'][2]['label'] = label2
totalActionsMap['operationalLayers'][0]['layerDefinition']['drawingInfo']['renderer']['classBreakInfos'][3]['label'] = label3

# modify the webmap
totalActionsMap.update()
print("Webmap Updated")







