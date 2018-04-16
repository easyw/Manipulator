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

MWB_wb_version='v 1.2.6'
global myurlMWB
myurlMWB='https://github.com/easyw/Manipulator'
global mycommitsMWB
mycommitsMWB=96 #v 1.2.6


import FreeCAD, FreeCADGui, Part, os, sys
import re, time

if (sys.version_info > (3, 0)):  #py3
    import urllib
    from urllib import request, error #URLError, HTTPError
else:  #py2
    import urllib2
    from urllib2 import Request, urlopen, URLError, HTTPError
    
import mvr_locator
from ManipulatorCMD import *

ManipulatorWBpath = os.path.dirname(mvr_locator.__file__)
ManipulatorWB_icons_path =  os.path.join( ManipulatorWBpath, 'Resources', 'icons')

global main_MWB_Icon
main_MWB_Icon = os.path.join( ManipulatorWB_icons_path , 'Manipulator-icon.svg')


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
        from PySide import QtGui
        import time
        
        pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Manipulator")
        tnow = int(time.time())
        oneday = 86400
        if pg.IsEmpty():
            pg.SetBool("checkUpdates",1)
            upd=True
            pg.SetInt("updateDaysInterval",1)
            pg.SetInt("lastCheck",tnow-2*oneday)
            interval=True
            FreeCAD.Console.PrintError('new \'check for updates\' feature added!!!\n')
            msg="""
            <font color=red>new \'check for updates\' feature added!!!</font>
            <br>
            <br>set \'checkUpdates\' to \'False\' to avoid this checking
            <br>in \"Tools\", \"Edit Parameters\",<br>\"Preferences\"->\"Mod\"->\"Manipulator\"
            """
            QtGui.QApplication.restoreOverrideCursor()
            reply = QtGui.QMessageBox.information(None,"Warning", msg)
        else:
            upd=pg.GetBool("checkUpdates")
        time_interval = pg.GetInt("updateDaysInterval")
        if time_interval <= 0:
            time_interval = 1
            pg.SetInt("updateDaysInterval",1)
        nowTimeCheck = int(time.time())
        lastTimeCheck = pg.GetInt("lastCheck")
        #print (nowTimeCheck - lastTimeCheck)/(oneday*time_interval)
        if time_interval <= 0 or ((nowTimeCheck - lastTimeCheck)/(oneday*time_interval) >= 1):
            interval = True
            pg.SetInt("lastCheck",tnow)
        else:
            interval = False
        def check_updates(url, commit_nbr):
            import re, sys
            resp_ok = False
            if (sys.version_info > (3, 0)):  #py3
                import urllib
                from urllib import request, error #URLError, HTTPError
                req = request.Request(url)
                try:
                    response = request.urlopen(req)
                    resp_ok = True
                    the_page = response.read().decode("utf-8") 
                except error.HTTPError as e:
                    FreeCAD.Console.PrintWarning('The server couldn\'t fulfill the request.')
                    FreeCAD.Console.PrintWarning('Error code: ' + str(e.code)+'\n')
                except error.URLError as e:
                    FreeCAD.Console.PrintWarning('We failed to reach a server.\n')
                    FreeCAD.Console.PrintWarning('Reason: '+ str(e.reason)+'\n')
                
            else:  #py2
                import urllib2
                from urllib2 import Request, urlopen, URLError, HTTPError
                req = Request(url)
                try:
                    response = urlopen(req)
                    resp_ok = True
                    the_page = response.read()
                except HTTPError as e:
                    FreeCAD.Console.PrintWarning('The server couldn\'t fulfill the request.')
                    FreeCAD.Console.PrintWarning('Error code: ' + str(e.code)+'\n')
                except URLError as e:
                    FreeCAD.Console.PrintWarning('We failed to reach a server.\n')
                    FreeCAD.Console.PrintWarning('Reason: '+ str(e.reason)+'\n')          
                
            if resp_ok:
                # everything is fine
                #the_page = response.read()
                # print the_page
                str2='<li class=\"commits\">'
                pos=the_page.find(str2)
                str_commits=(the_page[pos:pos+600])
                # print str_commits
                pos=str_commits.find('<span class=\"num text-emphasized\">')
                commits=(str_commits[pos:pos+200])
                commits=commits.replace('<span class=\"num text-emphasized\">','')
                #commits=commits.strip(" ")
                #exp = re.compile("\s-[^\S\r\n]")
                #print exp
                #nbr_commits=''
                my_commits=re.sub('[\s+]', '', commits)
                pos=my_commits.find('</span>')
                #print my_commits
                nbr_commits=my_commits[:pos]
                nbr_commits=nbr_commits.replace(',','')
                nbr_commits=nbr_commits.replace('.','')
                
                FreeCAD.Console.PrintMessage(url+'-> commits:'+str(nbr_commits)+'\n')
                delta = int(nbr_commits) - commit_nbr
                if delta > 0:
                    s = ""
                    if delta >1:
                        s="s"
                    FreeCAD.Console.PrintError('PLEASE UPDATE "Manipulator" WB.\n')
                    msg="""
                    <font color=red>PLEASE UPDATE "Manipulator" WB.</font>
                    <br>through \"Tools\" \"Addon manager\" Menu
                    <br><br><b>your release is """+str(delta)+""" commit"""+s+""" behind</b><br>
                    <br><a href=\""""+myurlMWB+"""\">Manipulator WB</a>
                    <br>
                    <br>set \'checkUpdates\' to \'False\' to avoid this checking
                    <br>in \"Tools\", \"Edit Parameters\",<br>\"Preferences\"->\"Mod\"->\"Manipulator\"
                    """
                    QtGui.QApplication.restoreOverrideCursor()
                    reply = QtGui.QMessageBox.information(None,"Warning", msg)
                else:
                    FreeCAD.Console.PrintMessage('the WB is Up to Date\n')
                #<li class="commits">
        ##
        if upd and interval:
            check_updates(myurlMWB, mycommitsMWB)
 
 
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
