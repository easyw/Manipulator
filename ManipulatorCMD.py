# -*- coding: utf-8 -*-
#****************************************************************************
#*                                                                          *
#*  Kicad STEPUP (TM) (3D kicad board and models to STEP) for FreeCAD       *
#*  3D exporter for FreeCAD                                                 *
#*  Kicad STEPUP TOOLS (TM) (3D kicad board and models to STEP) for FreeCAD *
#*  Copyright (c) 2015                                                      *
#*  Maurice easyw@katamail.com                                              *
#*                                                                          *
#*  Kicad STEPUP (TM) is a TradeMark and cannot be freely usable            *
#*                                                                          *

import FreeCAD,FreeCADGui
import FreeCAD, FreeCADGui, Part, os
import imp, os, sys, tempfile
import FreeCAD, FreeCADGui
from PySide import QtGui
from PySide.QtCore import QT_TRANSLATE_NOOP

import mvr_locator
# from kicadStepUptools import onLoadBoard, onLoadFootprint

reload_Gui=False#True

def reload_lib(lib):
    if (sys.version_info > (3, 0)):
        import importlib
        importlib.reload(lib)
    else:
        reload (lib)

ManipulatorWBpath = os.path.dirname(mvr_locator.__file__)
#sys.path.append(ksuWB + '/Gui')
ManipulatorWB_icons_path =  os.path.join( ManipulatorWBpath, 'Resources', 'icons')

#__dir__ = os.path.dirname(__file__)
#iconPath = os.path.join( __dir__, 'Resources', 'icons' )


# class SMExtrudeCommandClass():
#   """Extrude face"""
#
#   def GetResources(self):
#     return {'Pixmap'  : os.path.join( iconPath , 'SMExtrude.svg') , # the name of a svg file available in the resources
#             'MenuText': QtCore.QT_TRANSLATE_NOOP("Manipulator", "Extend Face"),
#             'ToolTip' : QtCore.QT_TRANSLATE_NOOP("Manipulator", "Extend a face along normal")}

class AlignerTools:
    "manipulator tools object"

    def GetResources(self):
        return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'Center-Align.svg') , # the name of a svg file available in the resources
                     'MenuText': QtCore.QT_TRANSLATE_NOOP("Manipulator", "Aligner Tools"),
                     'ToolTip' : QtCore.QT_TRANSLATE_NOOP("Manipulator", "Aligner & Mover Manipulator workbench")}

    def IsActive(self):
        #if FreeCAD.ActiveDocument == None:
        #    return False
        #else:
        #    return True
        #import kicadStepUptools
        import os, sys
        return True

    def Activated(self):
        # do something here...
        import Aligner
        reload_lib(Aligner)
        FreeCAD.Console.PrintWarning( 'Aligner active :)\n' )
        #import kicadStepUptools

FreeCADGui.addCommand('AlignerTools',AlignerTools())
##
class MoverTools:
    "manipulator Mover tools object"

    def GetResources(self):
        return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'Manipulator-cmd.svg') , # the name of a svg file available in the resources
                     'MenuText': QtCore.QT_TRANSLATE_NOOP("Manipulator", "Mover Tools"),
                     'ToolTip' : QtCore.QT_TRANSLATE_NOOP("Manipulator", "Mover Manipulator workbench")}

    def IsActive(self):
        #if FreeCAD.ActiveDocument == None:
        #    return False
        #else:
        #    return True
        #import Mover
        import os, sys
        return True

    def Activated(self):
        # do something here...
        #import kicadStepUptools
        #reload_lib( kicadStepUptools )
        import Mover
        reload_lib(Mover)
        FreeCAD.Console.PrintWarning( 'Mover active :)\n' )
        #import kicadStepUptools

FreeCADGui.addCommand('MoverTools',MoverTools())
##

class CaliperTools:
    "manipulator Caliper tools object"

    def GetResources(self):
        return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'Caliper.svg') , # the name of a svg file available in the resources
                     'MenuText': QtCore.QT_TRANSLATE_NOOP("Manipulator", "Caliper Tools"),
                     'ToolTip' : QtCore.QT_TRANSLATE_NOOP("Manipulator", "Caliper Manipulator workbench")}

    def IsActive(self):
        #if FreeCAD.ActiveDocument == None:
        #    return False
        #else:
        #    return True
        #import Mover
        import os, sys
        return True #False #True

    def Activated(self):
        # do something here...
        #import kicadStepUptools
        #reload_lib( kicadStepUptools )
        import Caliper
        reload_lib(Caliper)
        FreeCAD.Console.PrintWarning( 'Caliper active :)\n' )
        #import kicadStepUptools

FreeCADGui.addCommand('CaliperTools',CaliperTools())
##

#####
class ManpHelpFiles:
    exFile = None

    def __init__(self, exFile):
        self.exFile = str(exFile)
        self.ext    = self.exFile[self.exFile.rfind('.'):].lower()
        #print self.ext

    # 'hierarchy_nav.svg' for Demo
    #'Pixmap'  : os.path.join( ksuWB_icons_path , 'hierarchy_nav.svg') ,

    def GetResources(self):
        if 'pdf' in self.ext:
            return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'datasheet.svg') ,
                    'MenuText': str(self.exFile),
                    'ToolTip' : QtCore.QT_TRANSLATE_NOOP("Manipulator", "Help files")}
        elif 'fcstd' in self.ext:
            return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'Freecad.svg') ,
                    'MenuText': str(self.exFile),
                    'ToolTip' : QtCore.QT_TRANSLATE_NOOP("Manipulator", "Demo files")}
        else:
            return {'MenuText': str(self.exFile),
                    'ToolTip' : QtCore.QT_TRANSLATE_NOOP("Manipulator", "Demo files")}

    def Activated(self):
        FreeCAD.Console.PrintWarning('opening ' + self.exFile + "\r\n")
        import os, sys
        # So we can open the "Open File" dialog
        mw = FreeCADGui.getMainWindow()

        # Start off defaulting to the Examples directory
        manp_base_path = mvr_locator.module_path()
        exs_dir_path = os.path.join(manp_base_path, 'help')
        abs_manp_path = mvr_locator.abs_module_path()
        # Append this script's directory to sys.path
        sys.path.append(os.path.dirname(exs_dir_path))

        fnameDemo=(os.path.join(exs_dir_path, self.exFile))
        ext = os.path.splitext(os.path.basename(fnameDemo))[1]
        nme = os.path.splitext(os.path.basename(fnameDemo))[0]        # We've created a library that FreeCAD can use as well to open CQ files
        FC_majorV=int(float(FreeCAD.Version()[0]))
        FC_minorV=int(float(FreeCAD.Version()[1]))

        if ext.lower()==".pdf":
            import subprocess, sys
            if sys.platform == "linux" or sys.platform == "linux2":
                # linux
                subprocess.call(["xdg-open", fnameDemo])
            if sys.platform == "darwin":
                # osx
                cmd_open = 'open '+fnameDemo
                os.system(cmd_open) #win, osx
            else:
                # win
                subprocess.Popen([fnameDemo],shell=True)
        #elif ext.lower()==".fcstd":
        #    if FC_majorV==0 and FC_minorV <17:
        #        fnameDemo=fnameDemo.rstrip(ext)+'-fc16'+ ext
        #        FreeCAD.Console.PrintWarning('opening ' + fnameDemo + "\r\n")
        #    FreeCAD.open(fnameDemo)
        #    FreeCADGui.activeDocument().activeView().viewAxonometric()

##
