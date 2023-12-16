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
import os, sys, tempfile
import FreeCAD, FreeCADGui
from PySide import QtGui
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
#             'MenuText': "Extend Face" ,
#             'ToolTip' : "Extend a face along normal"}

class AlignerTools:
    "manipulator tools object"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'Center-Align.svg') , # the name of a svg file available in the resources
                     'MenuText': "Aligner Tools" ,
                     'ToolTip' : "Aligner & Mover Manipulator workbench"}
 
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
                     'MenuText': "Mover Tools" ,
                     'ToolTip' : "Mover Manipulator workbench"}
 
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
                     'MenuText': "Caliper Tools" ,
                     'ToolTip' : "Caliper Manipulator workbench"}
 
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
                    'ToolTip' : "Help files"}
        elif 'fcstd' in self.ext:
            return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'Freecad.svg') ,
                    'MenuText': str(self.exFile),
                    'ToolTip' : "Demo files"}        
        else:
            return {'MenuText': str(self.exFile),
                    'ToolTip' : "Demo files"}

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
class DatumPlane:
    "datum tools object"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'DatumPlane.svg') , # the name of a svg file available in the resources
                     'MenuText': "Datum Plane" ,
                     'ToolTip' : "Datum Plane\nManipulator workbench"}
 
    def IsActive(self):
        if FreeCAD.ActiveDocument is not None:
            import os, sys
            return True
 
    def Activated(self):
        # do something here...
        sel = FreeCADGui.Selection.getSelection()
        if len (sel) == 1:
            if 'App::Part' in sel[0].TypeId or 'PartDesign::Body' in sel[0].TypeId \
                    or 'Part::FeaturePython' in sel[0].TypeId:
                try:
                    sel[0].newObject('PartDesign::Plane','DatumPlane')
                except:
                    FreeCAD.ActiveDocument.addObject('PartDesign::Plane','DatumPlane')
            else:
                FreeCAD.ActiveDocument.addObject('PartDesign::Plane','DatumPlane')
        else:
            FreeCAD.ActiveDocument.addObject('PartDesign::Plane','DatumPlane')
        
        FreeCAD.ActiveDocument.recompute()
        #FreeCAD.Console.PrintWarning( 'Done :)\n' )
        
FreeCADGui.addCommand('DatumPlane',DatumPlane())
##
class Plane:
    "datum tools object"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'RefPlane.svg') , # the name of a svg file available in the resources
                     'MenuText': "PlaneRef" ,
                     'ToolTip' : "Plane Reference\nManipulator workbench"}
 
    def IsActive(self):
        if FreeCAD.ActiveDocument is not None:
            import os, sys
            return True
 
    def Activated(self):
        # do something here...
        def makePlane(plc):
            import FreeCAD, FreeCADGui
            from FreeCAD import Base
            import Part,PartGui
            FreeCAD.ActiveDocument.addObject("Part::Plane","RefPlane")
            plane = FreeCAD.ActiveDocument.ActiveObject
            plane.Length=10.000
            plane.Width=10.000
            l=float(plane.Length)
            w=float(plane.Width)
            px=float(plc.Base.x)
            py=float(plc.Base.y)
            x=px-l/2.0
            y=py-w/2.0
            plane.Placement=Base.Placement(Base.Vector(x,y,0.000),Base.Rotation(0.000,0.000,0.000,1.000))
            FreeCADGui.ActiveDocument.getObject(plane.Name).Transparency = 60
            FreeCADGui.ActiveDocument.getObject(plane.Name).LineColor = (1.000,0.667,0.498)
            return plane
            
        sel = FreeCADGui.Selection.getSelection()
        from FreeCAD import Base
        if len (sel) == 1:
            if 'App::Part' in sel[0].TypeId or 'PartDesign::Body' in sel[0].TypeId \
                    or 'Part::FeaturePython' in sel[0].TypeId:
                try:
                    plc = FreeCAD.Placement(Base.Vector(0.0,0.0,0.000),Base.Rotation(0.000,0.000,0.000,1.000))
                    plane = makePlane(plc)
                    sel[0].addObject(FreeCAD.ActiveDocument.ActiveObject)
                except:
                    plane.Placement = sel[0].Placement.multiply(plane.Placement)
                    print(plane.Label,'exception')
                #    FreeCAD.ActiveDocument.addObject('PartDesign::Plane','DatumPlane')
            else:
                plc = FreeCAD.Placement(Base.Vector(0.0,0.0,0.000),Base.Rotation(0.000,0.000,0.000,1.000))
                makePlane(plc)
        else:
            plc = FreeCAD.Placement(Base.Vector(0.0,0.0,0.000),Base.Rotation(0.000,0.000,0.000,1.000))
            makePlane(plc)        
        FreeCAD.ActiveDocument.recompute()
        #FreeCAD.Console.PrintWarning( 'Done :)\n' )
        
FreeCADGui.addCommand('Plane',Plane())
##
class DatumLine:
    "datum tools object"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'DatumLine.svg') , # the name of a svg file available in the resources
                     'MenuText': "Datum Line" ,
                     'ToolTip' : "Datum Line\nManipulator workbench"}
 
    def IsActive(self):
        if FreeCAD.ActiveDocument is not None:
            import os, sys
            return True
 
    def Activated(self):
        # do something here...
        sel = FreeCADGui.Selection.getSelection()
        if len (sel) == 1:
            if 'App::Part' in sel[0].TypeId or 'PartDesign::Body' in sel[0].TypeId \
                    or 'Part::FeaturePython' in sel[0].TypeId:
                try:
                    sel[0].newObject('PartDesign::Line','DatumLine')
                except:
                    FreeCAD.ActiveDocument.addObject('PartDesign::Line','DatumLine')
            else:
                FreeCAD.ActiveDocument.addObject('PartDesign::Line','DatumLine')
        else:
            FreeCAD.ActiveDocument.addObject('PartDesign::Line','DatumLine')
        
        FreeCAD.ActiveDocument.recompute()
        #FreeCAD.Console.PrintWarning( 'Done :)\n' )
        
FreeCADGui.addCommand('DatumLine',DatumLine())
##
class DatumPoint:
    "defeaturing tools object"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'DatumPoint.svg') , # the name of a svg file available in the resources
                     'MenuText': "Datum Point" ,
                     'ToolTip' : "Datum Point\nManipulator workbench"}
 
    def IsActive(self):
        if FreeCAD.ActiveDocument is not None:
            import os, sys
            return True
 
    def Activated(self):
        # do something here...
        sel = FreeCADGui.Selection.getSelection()
        if len (sel) == 1:
            if 'App::Part' in sel[0].TypeId or 'PartDesign::Body' in sel[0].TypeId \
                    or 'Part::FeaturePython' in sel[0].TypeId:
                try:
                    sel[0].newObject('PartDesign::Point','DatumPoint')
                except:
                    FreeCAD.ActiveDocument.addObject('PartDesign::Point','DatumPoint')
            else:
                FreeCAD.ActiveDocument.addObject('PartDesign::Point','DatumPoint')
        else:
            FreeCAD.ActiveDocument.addObject('PartDesign::Point','DatumPoint')
        
        FreeCAD.ActiveDocument.recompute()
        #FreeCAD.Console.PrintWarning( 'Done :)\n' )
        
FreeCADGui.addCommand('DatumPoint',DatumPoint())
##
class DatumLCS:
    "datum tools object"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'DatumLCS.svg') , # the name of a svg file available in the resources
                     'MenuText': "Datum LCS" ,
                     'ToolTip' : "Datum LCS\nManipulator workbench"}
 
    def IsActive(self):
        if FreeCAD.ActiveDocument is not None:
            import os, sys
            return True
 
    def Activated(self):
        # do something here...
        sel = FreeCADGui.Selection.getSelection()
        if len (sel) == 1:
            if 'App::Part' in sel[0].TypeId or 'PartDesign::Body' in sel[0].TypeId \
                    or 'Part::FeaturePython' in sel[0].TypeId:
                try:
                    sel[0].newObject('PartDesign::CoordinateSystem','Local_CS')
                except:
                    FreeCAD.ActiveDocument.addObject('PartDesign::CoordinateSystem','Local_CS')
            else:
                FreeCAD.ActiveDocument.addObject('PartDesign::CoordinateSystem','Local_CS')
        else:
            FreeCAD.ActiveDocument.addObject('PartDesign::CoordinateSystem','Local_CS')
        
        FreeCAD.ActiveDocument.recompute()
        #FreeCAD.Console.PrintWarning( 'Done :)\n' )
        
FreeCADGui.addCommand('DatumLCS',DatumLCS())
##


#temp_placement_object = App.ActiveDocument.addObject("App::Placement","temporary_placement")
class AltLCS:
    "datum tools object"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'AlternativeLCS.svg') , # the name of a svg file available in the resources
                     'MenuText': "Alternative Datum LCS" ,
                     'ToolTip' : "Alternative Datum LCS\nManipulator workbench"}
 
    def IsActive(self):
        if FreeCAD.ActiveDocument is not None:
            import os, sys
            return True
 
    def Activated(self):
        # do something here...
        sel = FreeCADGui.Selection.getSelection()
        if len (sel) == 1:
            if 'App::Part' in sel[0].TypeId or 'PartDesign::Body' in sel[0].TypeId \
                    or 'Part::FeaturePython' in sel[0].TypeId:
                try:
                    sel[0].newObject("App::Placement",'Local_CSa')
                except:
                    FreeCAD.ActiveDocument.addObject("App::Placement",'Local_CSa')
            else:
                FreeCAD.ActiveDocument.addObject("App::Placement",'Local_CSa')
        else:
            FreeCAD.ActiveDocument.addObject("App::Placement",'Local_CSa')
        
        FreeCAD.ActiveDocument.recompute()
        #FreeCAD.Console.PrintWarning( 'Done :)\n' )
        
FreeCADGui.addCommand('AltLCS',AltLCS())
##

class AnnoLbl:
    "datum tools object"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'Annotation.svg') , # the name of a svg file available in the resources
                     'MenuText': "Annotation Label" ,
                     'ToolTip' : "Annotation Label\nManipulator workbench"}
 
    def IsActive(self):
        if FreeCAD.ActiveDocument is not None:
            import os, sys
            return True
 
    def Activated(self):
        # do something here...
        sel = FreeCADGui.Selection.getSelection()
        if len (sel) == 1:
            if 'App::Part' in sel[0].TypeId or 'PartDesign::Body' in sel[0].TypeId \
                    or 'Part::FeaturePython' in sel[0].TypeId:
                try:
                    sel[0].newObject("App::AnnotationLabel","AnnoLbl")
                    anno = FreeCAD.ActiveDocument.ActiveObject
                    anno.LabelText = "AnnoLbl"
                except:
                    FreeCAD.ActiveDocument.addObject("App::AnnotationLabel","AnnoLbl")
                    anno = FreeCAD.ActiveDocument.ActiveObject
                    anno.LabelText = "AnnoLbl"
            else:
                FreeCAD.ActiveDocument.addObject("App::AnnotationLabel","AnnoLbl")
                anno = FreeCAD.ActiveDocument.ActiveObject
                anno.LabelText = "AnnoLbl"
        else:
            FreeCAD.ActiveDocument.addObject("App::AnnotationLabel","AnnoLbl")
            anno = FreeCAD.ActiveDocument.ActiveObject
            anno.LabelText = "AnnoLbl"
        
        FreeCAD.ActiveDocument.recompute()
        #FreeCAD.Console.PrintWarning( 'Done :)\n' )
        
FreeCADGui.addCommand('AnnoLbl',AnnoLbl())
##
class ResetPositions:
    "manipulator reset positions tool"

    def GetResources(self):
        return {'Pixmap'  : os.path.join( ManipulatorWB_icons_path , 'centering-w.svg') , # the name of a svg file available in the resources
                     'MenuText': "Centering Widgets" ,
                     'ToolTip' : "Centering Widgets\nManipulator workbench"}
 
    def IsActive(self):
        import os, sys
        return True #False #True

    def Activated(self):
        # do something here...
        #import kicadStepUptools
        #reload_lib( kicadStepUptools )
        import Caliper
        reload_lib(Caliper)
        Caliper.Cp_undock()
        Caliper.Cp_centerOnScreen(Caliper.CPDockWidget)
        import Mover
        reload_lib(Mover)
        Mover.Mv_undock()
        Mover.Mv_centerOnScreen(Mover.MVDockWidget)
        import Aligner
        reload_lib(Aligner)
        Aligner.Alg_undock()
        Aligner.Alg_centerOnScreen (Aligner.ALGDockWidget)
FreeCADGui.addCommand('ResetPositions',ResetPositions())
##
