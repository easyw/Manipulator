# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                          *
#*  Copyright (c) 2017                                                      *
#*  Maurice easyw@katamail.com                                              *
#*                                                                          *
#*   code partially based on:                                               *
#*                                                                          *
# evolution of Macro_CenterFace                                             *
# some part of Macro WorkFeature                                            *
# and assembly2                                                             *
#                                                                           *
# Move objs along obj face Normal or edge                                   *
#                                                                           *
#  (C) Maurice easyw-fc 2016                                                *
#    This program is free software; you can redistribute it and/or modify   *
#    it under the terms of the GNU Library General Public License (LGPL)    *
#    as published by the Free Software Foundation; either version 2 of      *
#    the License, or (at your option) any later version.                    *
#    for detail see the LICENCE text file.                                  *
#****************************************************************************

import FreeCAD, FreeCADGui, Part, os, sys
import mvr_locator
from ManipulatorCMD import *

ManipulatorWBpath = os.path.dirname(mvr_locator.__file__)
ManipulatorWB_icons_path =  os.path.join( ManipulatorWBpath, 'Resources', 'icons')

global main_MWB_Icon
main_MWB_Icon = os.path.join( ManipulatorWB_icons_path , 'Manipulator-icon.svg')

MWB_wb_version='v 1.1.3'
#try:
#    from FreeCADGui import Workbench
#except ImportError as e:
#    FreeCAD.Console.PrintWarning("error")
    
class ManipulatorWB ( Workbench ):
    global main_MWB_Icon, MWB_wb_version
    
    "kicad StepUp WB object"
    Icon = main_MWB_Icon
    #Icon = ":Resources/icons/kicad-StepUp-tools-WB.svg"
    MenuText = "Manipulator WB"
    ToolTip = "Aligner & Mover Manipulator workbench"
 
    def GetClassName(self):
        return "Gui::PythonWorkbench"
    
    def Initialize(self):
        #import ManipulatorCMD
        submenu = ['Manipulator-cheat-sheet.pdf']
        dirs = self.ListDemos()

        #self.appendToolbar("ksu Tools", ["ksuTools"])
        self.appendToolbar("Manipulator Tools", ["AlignerTools","MoverTools","CaliperTools"])
        
        #self.appendMenu("ksu Tools", ["ksuTools","ksuToolsEdit"])
        self.appendMenu("Manipulator Tools", ["AlignerTools"])
        self.appendMenu("Manipulator Tools", ["MoverTools"])
        self.appendMenu("Manipulator Tools", ["CaliperTools"])
        self.appendMenu(["Manipulator Tools", "Help"], submenu)
        
        Log ("Loading Manipulator Module... done\n")
 
    def Activated(self):
                # do something here if needed...
        Msg ("Manipulator WB Activated("+MWB_wb_version+")\n")
 
    def Deactivated(self):
                # do something here if needed...
        Msg ("Manipulator WB Deactivated()\n")
    
    @staticmethod
    def ListDemos():
        import os
        import mvr_locator

        dirs = []
        # List all of the example files in an order that makes sense
        module_base_path = mvr_locator.module_path()
        help_dir_path = os.path.join(module_base_path, 'help')
        dirs = os.listdir(help_dir_path)
        dirs.sort()

        return dirs

###

dirs = ManipulatorWB.ListDemos()
#FreeCADGui.addCommand('ksuWBOpenDemo', ksuOpenDemo())
#dirs = ksuWB.ListDemos()
for curFile in dirs:
    FreeCADGui.addCommand(curFile, ManpHelpFiles(curFile))

FreeCADGui.addWorkbench(ManipulatorWB)