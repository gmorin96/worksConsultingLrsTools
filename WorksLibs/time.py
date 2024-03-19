import arcpy
import sys
from datetime import datetime, timedelta

info = "Module that contains time classes and functions."
metadata = {
  "owner": "Works Consulting LLC",
  "creationDate": "3/15/2024",
  "creator": "Gabriel Morin",
  "lastEditDate": "3/18/2024",
  "lastEditor": "Gabriel Morin"}

class tracking:
    """--------------------
Contains start(), live() and end() functions to assist in runtime logging and tracking attributes.
--------------------
"""

    info = "Class that helps with recording process runtimes."
    showMetrics = True
    ProcessNumber = 0
    startList = []
    timeTuple = []
    iterationTuple = []
    openSession = False
    currentLabel = None
    
    def __init__(self):
        self.showMetrics = showMetrics
        self.info = "Class that helps with recording process runtimes."
    
    def start(ProcessLabel):
        """--------------------
Intakes a process label and updates the tracking class for process runtimes and live tracking. Opens a session.
--------------------
"""
        
        assert type(ProcessLabel) == str, "ArgumentDataTypeError - expected a {0} got a {1}".format(str,type(ProcessLabel))
        assert tracking.openSession == False, "A tracking session is already open. Reconfigure and close tracking sessions before starting another one."
        arcpy.SetProgressorLabel(ProcessLabel)
        tracking.currentLabel = ProcessLabel
        ProcessNumber = tracking.ProcessNumber
        tracking.startList.append(datetime.now())
        tracking.timeTuple.append([])
        tracking.iterationTuple.append(0)
        tracking.openSession = True

    
    def live(iterCount):
        """--------------------
Intakes the total number of iterations for process and updates the Progressor Label with ETA's and ETR's.
--------------------
"""
        
        assert type(iterCount) == int, "ArgumentDataTypeError - expected a {0} got a {1}".format(int,type(iterCount))
        assert tracking.openSession == True, "No tracking session is open. Reconfigure and open a tracking session before."
        ProcessLabel = tracking.currentLabel
        ProcessNumber = tracking.ProcessNumber
        start = tracking.startList[ProcessNumber]
        time = tracking.timeTuple[ProcessNumber]
        iteration = tracking.iterationTuple[ProcessNumber]
        now = datetime.now()
        time.append(now)
        diff = time[iteration] - start
        rate = (diff.total_seconds())/len(time)
        eta = rate*iterCount/60
        etr = eta - (diff.total_seconds())/60
        units = "sec(s)" if etr < 1 else "min(s)"
        etr = etr*60 if etr < 1 else etr
        newProgressorLabel = "{0}\nEstimated total time in min(s): {1} | Estimate remaining time in {2}: {3}".format(ProcessLabel,round(eta,1),units,round(etr,1))
        arcpy.SetProgressor("step",newProgressorLabel,0,iterCount,iteration)
        arcpy.SetProgressorPosition(iteration)
        tracking.iterationTuple[ProcessNumber] += 1

    
    def end():
        """--------------------
Displays process runtimes through arcpy's AddMessage function. Closes a session.
--------------------
"""
        assert tracking.openSession == True, "No tracking session is open. Reconfigure and open a tracking session before."
        showMetrics = tracking.showMetrics
        ProcessLabel = tracking.currentLabel
        ProcessNumber = tracking.ProcessNumber
        start = tracking.startList[ProcessNumber]
        end = datetime.now()
        date_str = end.strftime("%H:%M:%S")
        diff = end - start
        diff2 = diff.total_seconds() if diff.total_seconds() < 60 else diff.total_seconds()/60
        diff_str = str(round(diff2,2)) + " seconds" if diff.total_seconds() < 60 else str(round(diff2,2)) + " minutes"
        if showMetrics:
            arcpy.AddMessage("[{0}] {1} took {2} and finished at {3}.".format(ProcessNumber+1,ProcessLabel,diff_str,date_str))
        tracking.ProcessNumber +=1
        tracking.openSession = False
