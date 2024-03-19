import arcpy
import sys
import os
from datetime import datetime, timedelta

info = "Module that contains data check classes and functions."
metadata = {
  "owner": "Works Consulting LLC",
  "creationDate": "3/18/2024",
  "creator": "Gabriel Morin",
  "lastEditDate": "3/18/2024",
  "lastEditor": "Gabriel Morin"}

class inputs:
    """--------------------
Contains initialChecks() functions to assist in data checks and attributes.
--------------------
"""

    info = "Class that helps with checking input feature classes"
    showMessages= True
    inputCount = 0
    allowedTypesAttr =  {'Table':False,'TableView':False,'FeatureClass':True,'FeatureLayer':True}
    inputDataDict = {}
    
    def __init__(self):
        self.showMessages = showMessages
        self.info = info
        
    def initialChecks(inputData,requireShape=False):
        """--------------------
Intakes a input data and runs checks on them and spits out describe object attributes. Second parameter defines whether to check for shape or not.
--------------------
"""

        assert arcpy.Exists(inputData), "The input data {0} cannot be found.".format(inputData)
        showMessages = inputs.showMessages
        allowedTypesAttr = inputs.allowedTypesAttr
        allowedTypes = [dataType for dataType,shape in allowedTypesAttr.items()]
        shape_types = [dataType for dataType,shape in allowedTypesAttr.items() if shape]
        
        fc_desc,fc_desc_type = arcpy.Describe(inputData),arcpy.Describe(inputData).dataType
        if requireShape:
            assert fc_desc_type in shape_types, "Expected shape got {0}.".format(fc_desc_type)
        
        assert fc_desc_type in allowedTypes, "The Input Features type of {0} is not supported. Please contact Gabe to add in compatability.".format(fc_desc_type)
            
        fc_desc_sr,fc_desc_path,fc_desc_baseName = fc_desc.spatialreference,fc_desc.path,fc_desc.baseName
        fullpath = os.path.join(fc_desc_path,fc_desc_baseName)
        fc_count_path = int(float((arcpy.GetCount_management(fullpath)).getOutput(0)))
        fc_count = int(float((arcpy.GetCount_management(inputData)).getOutput(0)))
        if showMessages:
            fc_sel_count = 0
            try:
                fidSet = fc_desc.fidSet
                if len(fidSet) > 0:
                    fc_sel_count = len(fidSet.split(";")) if ";" in fidSet else 1
            except:
                raise
            if fc_count < fc_count_path:
                fc_sel_count = fc_count
            if inputs.inputCount == 0:
                arcpy.AddMessage("Record Count (Selection)   | Layer/FC Name")
                arcpy.AddMessage("-----------------------------------------------------------")
            arcpy.AddMessage("{0} ({1})                 | {2}".format(fc_count_path,fc_sel_count,fc_desc_baseName))
            
        inputDataDict = inputs.inputDataDict
        inputDataDict[fc_desc_baseName] = {"descObj": fc_desc,
                         "dataType": fc_desc_type,
                         "baseName": fc_desc_baseName,
                         "path": fc_desc_path,
                         "spatialReference": fc_desc_sr,
                         "recordCount": fc_count_path,
                         "selectionCount": fc_sel_count}
        inputs.inputDataDict = inputDataDict
        inputs.inputCount += 1
        return inputDataDict[fc_desc_baseName]
        
