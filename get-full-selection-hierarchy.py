#FreeCADGui.Selection.getSelectionEx('', 0)

## Use getSelectionEx('', 0) to obtained the full hierarchy information. The first argument is the document name, 
## empty string means current document, '*' means all document. 
## The second argument 1 means resolve sub-object, which is the default value. 0 means full hierarchy.

Code: Select all

for sel in FreeCADGui.Selection.getSelectionEx('', 0):
    print('sel object: ' + sel.Object.Name)
    for sub in sel.SubElementNames:
        print('sub: ' + sub)

