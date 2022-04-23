"""
STL Viewer
Uses Wx Python and VTK

#Features:
Load an STL file.
Rotate, pan, zoom the model.

See it in wireframe, surface.
Take a screenshot.
"""

#import python modules
import wx, vtk, sys, os, copy
import numpy as np
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
from PARA_FIT_UTILITIES_FFD import PARA
tool=PARA()



class EventsHandler(object):

	def __init__(self, parent):
		self.parent = parent

	def onExit(self, event):
		"""
		close entire window	
		"""
		self.parent.Destroy()

	def onBackgroundColor(self, event):
		"""Change Background"""
		print("onBackgroundColor")
		dlg = wx.ColourDialog(self.parent)
		dlg.GetColourData().SetChooseFull(True)
		if dlg.ShowModal() == wx.ID_OK:
			data = dlg.GetColourData()
			dlg.Destroy()
			self.SetColor(data.GetColour().Get())
			return
		dlg.Destroy()

	def SetColor(self, bkgColor):
		print("setColor")
		"""
		@warning if the model is not loaded and the color is not "clicked"
		on, then rend will return None
		"""
		rend = self.parent.vtkPanel.renderer
		if not rend:  # rend doesnt exist at first
			print 'Try again to change the color (you didnt "click" on the color; one time bug)'
			return
			rend = self.parent.vtkPanel.renderer
		## bkgColor range from 0 to 255
		## color ranges from 0 to 1
		color = [bkgColor[0] / 255., bkgColor[1] / 255., bkgColor[2] / 255.]
		rend.SetBackground(color)
		self.parent.vtkPanel.widget.Render()


	def viewOnZMinusNormalPlane(self, event):

		"""
		direction of the axis is copied from paraview convention
		"""

		print("view on ZMinus plane")
		rend = self.parent.vtkPanel.renderer

		cam = rend.GetActiveCamera()
		cam.SetFocalPoint(0, 0, 0);
		#Camera in Z so it display XY planes.
		cam.SetPosition(0, 0, 1)
		#Up direction is the X not the y
		cam.SetViewUp(0, 1, 0)
		#it is important to reset the camera before the zoom
		rend.ResetCamera()
		cam.Zoom(0)        

		self.parent.vtkPanel.widget.Render()


	def viewOnZPlusNormalPlane(self, event):

		"""
		direction of the axis is copied from paraview convention
		"""

		print("view on ZPlus plane")
		rend = self.parent.vtkPanel.renderer

		cam = rend.GetActiveCamera()
		cam.SetFocalPoint(0, 0, 0);
		#Camera in Z so it display XY planes.
		cam.SetPosition(0, 0, -1)
		#Up direction is the X not the y
		cam.SetViewUp(0, 1, 0)
		#it is important to reset the camera before the zoom
		rend.ResetCamera()
		cam.Zoom(0)        

		self.parent.vtkPanel.widget.Render()


	def viewOnYMinusNormalPlane(self, event):

		"""
		direction of the axis is copied from paraview convention
		"""

		print("view on YMinus plane")
		rend = self.parent.vtkPanel.renderer

		cam = rend.GetActiveCamera()
		cam.SetFocalPoint(0, 0, 0);
		#Camera in Z so it display XY planes.
		cam.SetPosition(0, 1, 0)
		#Up direction is the X not the y
		cam.SetViewUp(0, 1, 0)
		#it is important to reset the camera before the zoom
		rend.ResetCamera()
		cam.Zoom(0)        

		self.parent.vtkPanel.widget.Render()


	def viewOnYPlusNormalPlane(self, event):

		"""
		direction of the axis is copied from paraview convention
		"""

		print("view on YPlus plane")
		rend = self.parent.vtkPanel.renderer

		cam = rend.GetActiveCamera()
		cam.SetFocalPoint(0, 0, 0);
		#Camera in Z so it display XY planes.
		cam.SetPosition(0, -1, 0)
		#Up direction is the X not the y
		cam.SetViewUp(0, 1, 0)
		#it is important to reset the camera before the zoom
		rend.ResetCamera()
		cam.ParallelProjectionOn()
		cam.Zoom(0)        

		self.parent.vtkPanel.widget.Render()


	def viewOnXMinusNormalPlane(self, event):

		"""
		direction of the axis is copied from paraview convention
		"""

		print("view on XMinus plane")
		rend = self.parent.vtkPanel.renderer

		cam = rend.GetActiveCamera()
		cam.SetFocalPoint(0, 0, 0);
		#Camera in Z so it display XY planes.
		cam.SetPosition(1, 0, 0)
		#Up direction is the X not the y
		cam.SetViewUp(1, 0, 1)
		#it is important to reset the camera before the zoom
		rend.ResetCamera()
		cam.Zoom(0)        

		self.parent.vtkPanel.widget.Render()


	def viewOnXPlusNormalPlane(self, event):

		"""view On X Plus Normal Plane.
		direction of the axis is copiedParallelProjectionOff from paraview convention
		"""

		print("view on XPlus plane")
		rend = self.parent.vtkPanel.renderer

		cam = rend.GetActiveCamera()

		cam.SetFocalPoint(0, 0, 0);
		#Camera in Z so it display XY planes.
		cam.SetPosition(-1, 0, 0)
		#Up direction is the X not the y
		cam.SetViewUp(1, 0, 1)
		#it is important to reset the camera before the zoom
		rend.ResetCamera()
		cam.Zoom(0)        

		self.parent.vtkPanel.widget.Render()


	def resetZoom(self, event):

		"""Reset zoom.      
		"""

		print("reset zoom")
		rend = self.parent.vtkPanel.renderer

		cam = rend.GetActiveCamera()

		#cam.SetFocalPoint(0, 0, 0);
		#Camera in Z so it display XY planes.
		#cam.SetPosition(-1, 0, 0)
		#Up direction is the X not the y
		#cam.SetViewUp(1, 0, 1)
		#it is important to reset the camera before the zoom
		rend.ResetCamera()
		cam.Zoom(0)        

		self.parent.vtkPanel.widget.Render()


	def shadeObject(self, event):

		"""Shade object.      
		"""

		print("shade object")
		rend = self.parent.vtkPanel.renderer
		cam = rend.GetActiveCamera()

		#-----------------------------------------        
		coneActor = rend.GetActors().GetLastActor()
		coneActor.GetProperty().EdgeVisibilityOff()
		#coneActor.GetProperty().PointVisibilityOn()
		#coneActor.GetProperty().SetEdgeColor(0, 0, 0)
		coneActor.GetProperty().LightingOn()
		coneActor.GetProperty().ShadingOn()
		coneActor.GetProperty().SetOpacity(1.0)
		#-----------------------------------------

		#rend.ResetCamera()
		self.parent.vtkPanel.widget.Render()


	def shadeAndEdgesObject(self, event):

		"""Shade and Edges object.      
		"""

		print("RED COLOUR: show shade and edges of the object")
		rend = self.parent.vtkPanel.renderer
		cam = rend.GetActiveCamera()

		#-----------------------------------------       
		coneActor = rend.GetActors().GetLastActor()
		coneActor.GetProperty().EdgeVisibilityOn()
		#coneActor.GetProperty().PointVisibilityOn()
		coneActor.GetProperty().SetEdgeColor(0, 0, 0)
		coneActor.GetProperty().ShadingOn()
		coneActor.GetProperty().SetOpacity(1.0)
		#-----------------------------------------
		#rend.ResetCamera()
		self.parent.vtkPanel.widget.Render()


	def showLatticeFFD(self, event):

		"""Show/render the FFD lattice.
		"""
		print("show FFD the only linked button for now")
		rend = self.parent.vtkPanel.renderer

		CPLattice, xLatticeMin, xLatticeMax, yLatticeMin, yLatticeMax, zLatticeMin, zLatticeMax = self.constructLattice()
		X = CPLattice[:, :, :, 0].flatten()
		Y = CPLattice[:, :, :, 1].flatten()
		Z = CPLattice[:, :, :, 2].flatten()

		for i in range(len(X)):
			source = vtk.vtkSphereSource()
			source.SetCenter(X[i],Y[i],Z[i])
			source.SetRadius(0.03)		
			mapper = vtk.vtkPolyDataMapper()
			mapper.SetInputConnection(source.GetOutputPort())

			actor = vtk.vtkActor()
			actor.SetMapper(mapper)
			actor.GetProperty().SetColor(0.57,0,0) 
			rend.AddActor(actor)
		
		CPDeformed = self.showDeformedLatticeFFD(event)
		
		meshPoints = self.getMeshPoints()
		x = meshPoints[:,0]
		y = meshPoints[:,1]
		z = meshPoints[:,2]
		xSelected, ySelected, zSelected, IDSelected = tool.findPointsInLattice(CPLattice,x,y,z)
		pack = [xSelected, ySelected, zSelected, IDSelected]

		for i in range(len(xSelected)):
			source = vtk.vtkSphereSource()
			source.SetCenter(xSelected[i],ySelected[i], zSelected[i])
			source.SetRadius(0.007)		
			mapper = vtk.vtkPolyDataMapper()
			mapper.SetInputConnection(source.GetOutputPort())

			actor = vtk.vtkActor()
			actor.SetMapper(mapper)
			actor.GetProperty().SetColor(0,0,205) 
			rend.AddActor(actor)
		
		self.showDeformedPoints(event)

			

			
	def showDeformedPoints(self, event):
	
		rend = self.parent.vtkPanel.renderer
	
		CPDeformed = self.showDeformedLatticeFFD(event)
		CPLattice, xLatticeMin, xLatticeMax, yLatticeMin, yLatticeMax, zLatticeMin, zLatticeMax = self.constructLattice()
		meshPoints = self.getMeshPoints()
		x = meshPoints[:,0]
		y = meshPoints[:,1]
		z = meshPoints[:,2]
		# We need the cartesian coordinates and then its ID (position in the list)
		xSelected,ySelected,zSelected, IDSelected = tool.findPointsInLattice(CPLattice,x,y,z)
		
		xDef,yDef,zDef = tool.FFD(CPDeformed, xSelected,ySelected,zSelected, xLatticeMin, xLatticeMax, yLatticeMin, yLatticeMax, zLatticeMin, zLatticeMax)		
		pack = [xDef, yDef, zDef, IDSelected]
		
		for i in range(len(xDef)):
			source = vtk.vtkSphereSource()
			source.SetCenter(xDef[i],yDef[i], zDef[i])
			source.SetRadius(0.006)		
			mapper = vtk.vtkPolyDataMapper()
			mapper.SetInputConnection(source.GetOutputPort())
			actor = vtk.vtkActor()
			actor.SetMapper(mapper)
			actor.GetProperty().SetColor(0,205,5) 
			rend.AddActor(actor)
			
			
		self.showRenderedDeformedMesh(pack)			
	
		
	def showDeformedLatticeFFD(self, event):

		"""Show/render the FFD lattice.
		"""
		print("show FFD")
		rend = self.parent.vtkPanel.renderer

		CPLattice, xLatticeMin, xLatticeMax, yLatticeMin, yLatticeMax, zLatticeMin, zLatticeMax = self.constructLattice()
		import copy
		CPLatticeDeformed = copy.deepcopy(CPLattice)
		print CPLattice[1,1,3,2]
		CPLatticeDeformed[1,1,3,2]+=CPLatticeDeformed[1,1,3,2] * 0.5
		CPLatticeDeformed[1,2,3,2]+=CPLatticeDeformed[1,2,3,2] * 0.5
		print CPLatticeDeformed[1,1,3,2]
		
		X = CPLatticeDeformed[:, :, :, 0].flatten()
		Y = CPLatticeDeformed[:, :, :, 1].flatten()
		Z = CPLatticeDeformed[:, :, :, 2].flatten()

		for i in range(len(X)):
			source = vtk.vtkSphereSource()
			source.SetCenter(X[i],Y[i],Z[i])
			source.SetRadius(0.029)		
			mapper = vtk.vtkPolyDataMapper()
			mapper.SetInputConnection(source.GetOutputPort())

			actor = vtk.vtkActor()
			actor.SetMapper(mapper)
			actor.GetProperty().SetColor(0/255,255/255,0/255) 
			rend.AddActor(actor)

		return CPLatticeDeformed


	def constructLattice(self):
		
		"""Set up the lattice.
		"""
		
		CPx, CPy, CPz = 3, 4, 4
		xLatticeMin, xLatticeMax = 0.55, 0.9
		yLatticeMin, yLatticeMax = -1.95, -1.25
		zLatticeMin, zLatticeMax = 0, 0.7
		CPLattice = tool.createLattice(CPx, CPy, CPz, xLatticeMin, xLatticeMax, yLatticeMin, yLatticeMax, zLatticeMin, zLatticeMax)
		
		return CPLattice, xLatticeMin, xLatticeMax, yLatticeMin, yLatticeMax, zLatticeMin, zLatticeMax
		

	def getMeshPoints(self):
		
		"""Get mesh points.
		
		return x,y,z read from the .stl file.
		"""
		
		reader = vtk.vtkSTLReader()
		reader.SetFileName(self.parent.vtkPanel.filename)		
		reader.Update()	
		#get the polydata		
		data = reader.GetOutput()
		
		#get the mesh
		n_points = data.GetNumberOfPoints()		
		meshPoints = np.zeros([n_points, 3])
		for i in range(n_points):
			meshPoints[i][0], meshPoints[i][1], meshPoints[i][2] = data.GetPoint(i)
			
		return meshPoints	

	def showRenderedDeformedMesh(self, pack):
		
		
		xUpdated, yUpdated, zUpdated, IDSelected = pack[0],pack[1],pack[2],pack[3]
		
		print IDSelected
		print IDSelected[0]
		print type(IDSelected)
		
		print ("get rendered deformed mesh")
		"""Get mesh points.
		
		https://www.programcreek.com/python/example/10678/vtk.vtkPoints
		return x,y,z read from the .stl file.
		"""

		rend = self.parent.vtkPanel.renderer
		reader = vtk.vtkSTLReader()
		reader.SetFileName(self.parent.vtkPanel.filename)		
		reader.Update()	
		#get the polydata		
		poly = reader.GetOutput()
		
		#get the mesh
		NoPts = poly.GetNumberOfPoints()				
		meshPts = np.zeros((NoPts, 3), dtype = np.single)
		
		for i in range(NoPts):			
			meshPts[i, :] = (poly.GetPoint(i)[0], poly.GetPoint(i)[1], poly.GetPoint(i)[2])

		#deform the mesh by making it 1.1 bigger		
		scalars = vtk.vtkFloatArray()
		pts = vtk.vtkPoints()
		pts.SetNumberOfPoints(NoPts)
		for i in range(NoPts):
			if i in IDSelected:			
				itemIndex = np.where(IDSelected == i)
				pts.SetPoint(i, xUpdated[itemIndex], yUpdated[itemIndex], zUpdated[itemIndex])				
			else:
				pts.SetPoint(i, meshPts[i, 0], meshPts[i, 1], meshPts[i, 2])
			#scalars.InsertTuple1(i, 1.1)
			
		poly.SetPoints(pts)
		
		#start rendering
		mapper = vtk.vtkPolyDataMapper()
		mapper.SetInputData(poly)		
		actor = vtk.vtkActor()		
		actor.SetMapper(mapper)
		actor.GetProperty().SetColor(0,255/255,0/255) 
		rend.AddActor(actor)		
			
			
		
	def edgesObject(self, event):

		"""Show edges only object.      
		"""

		print("show edges only object")
		rend = self.parent.vtkPanel.renderer
		cam = rend.GetActiveCamera()

		#-----------------------------------------       
		coneActor = rend.GetActors().GetLastActor()		
		coneActor.GetProperty().EdgeVisibilityOn()
		#coneActor.GetProperty().PointVisibilityOff()		
		coneActor.GetProperty().LightingOn()
		coneActor.GetProperty().ShadingOff()
		coneActor.GetProperty().SetOpacity(0.1)
		coneActor.GetProperty().SetEdgeColor(0, 0, 0)
		#-----------------------------------------

		#rend.ResetCamera()
		self.parent.vtkPanel.widget.Render()


	def onToggleStatusBar(self, e):
		"""
		status bar toogle
		"""
		if self.parent.isstatusbar:
				self.parent.statusbar.Hide()
				self.parent.isstatusbar = False
		else:
			self.parent.statusbar.Show()
			self.parent.isstatusbar = True

	def onToggleToolBar(self, e):
		"""
	tool baR toogle
		"""
		if self.parent.istoolbar:
			self.parent.toolbar1.Hide()
			self.parent.istoolbar = False
		else:
			self.parent.toolbar1.Show()
			self.parent.istoolbar = True

	# Help Menu About
	def onAbout(self, event):

		print("on about")
		about = [
			'VTK STL Viewer\n',
			'',
			'',
			'Keyboard Controls',
			'',
			'R   - Fit the model',
			'F   - Zoom the moDEL',
			'S   - surface',
			'W   - wireframe',]

		dlg = wx.MessageDialog(None, '\n'.join(about), 'About', wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()

#==========================	
class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):
 
    def __init__(self,parent=None):
        self.AddObserver("LeftButtonPressEvent",self.leftButtonPressEvent)
 
        self.LastPickedActor = None
        self.LastPickedProperty = vtk.vtkProperty()
 
    def leftButtonPressEvent(self,obj,event):
        clickPos = self.GetInteractor().GetEventPosition()
 
        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())
 
        # get the new
        self.NewPickedActor = picker.GetActor()
 
        # If something was selected
        if self.NewPickedActor:
            # If we picked something before, reset its property
            if self.LastPickedActor:
                self.LastPickedActor.GetProperty().DeepCopy(self.LastPickedProperty)
 
 
            # Save the property of the picked actor so that we can
            # restore it next time
            self.LastPickedProperty.DeepCopy(self.NewPickedActor.GetProperty())
            # Highlight the picked actor by changing its properties
            self.NewPickedActor.GetProperty().SetColor(1.0, 0.0, 0.0)
            self.NewPickedActor.GetProperty().SetDiffuse(1.0)
            self.NewPickedActor.GetProperty().SetSpecular(0.0)
 
            # save the last picked actor
            self.LastPickedActor = self.NewPickedActor
 
        self.OnLeftButtonDown()
        return
#==========================
 
class vtkPanel(wx.Panel):
    print("__init__ vtkPanel")
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        
        #to interact with the scene using the mouse use an instance of vtkRenderWindowInteractor. 
        self.widget = wxVTKRenderWindowInteractor(self, -1)
        #self.widget.Enable(1)
              

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.widget, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.renderer = vtk.vtkRenderer()		
		
        self.renderer.SetBackground(0.1, 0.3, 0.4)
        self.widget.GetRenderWindow().AddRenderer(self.renderer)        
        self.Layout()
        self.widget.Render()
        self.filename=None
        self.isploted = False
    
            
    def onTakePicture(self, event):

        renderLarge = vtk.vtkRenderLargeImage()
        renderLarge.SetInput(self.renderer)
        renderLarge.SetMagnification(4)

        wildcard = "PNG (*.png)|*.png|" \
            "JPEG (*.jpeg; *.jpeg; *.jpg; *.jfif)|*.jpg;*.jpeg;*.jpg;*.jfif|" \
            "TIFF (*.tif; *.tiff)|*.tif;*.tiff|" \
            "BMP (*.bmp)|*.bmp|" \
            "PostScript (*.ps)|*.ps|" \
            "All files (*.*)|*.*"

        dlg = wx.FileDialog(None, "Choose a file", "",
                            "", wildcard, wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            fname = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            fname = os.path.join(self.dirname, fname)
            # We write out the image which causes the rendering to occur. If you
            # watch your screen you might see the pieces being rendered right
            # after one another.
            lfname = fname.lower()
            if lfname.endswith('.png'):
                writer = vtk.vtkPNGWriter()
            elif lfname.endswith('.jpeg'):
                writer = vtk.vtkJPEGWriter()
            elif lfname.endswith('.tiff'):
                writer = vtk.vtkTIFFWriter()
            elif lfname.endswith('.ps'):
                writer = vtk.vtkPostScriptWriter()
            else:
                writer = vtk.vtkPNGWriter()

            writer.SetInputConnection(renderLarge.GetOutputPort())
            writer.SetFileName(fname)
            writer.Write()
        dlg.Destroy()

    #write your VTK panel methods here
    def plot(self,event):

	print("plot")
        self.renderthis()
          
    def renderthis(self):

		print("render this")

		# open a window and create a renderer            
		self.widget.GetRenderWindow().AddRenderer(self.renderer)

	   # open file             
		self.filename = ""
		openFileDialog = wx.FileDialog(self, "Open .stl file", "", self.filename, "*.stl", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		
		if openFileDialog.ShowModal() == wx.ID_CANCEL:
			return
		self.filename = openFileDialog.GetPath()
		# render the data loading either VTK or OBJ file, vtk offers it
		reader = vtk.vtkSTLReader()
		#reader = vtk.vtkOBJReader()
		reader.SetFileName(self.filename)
		
		#take the polygonal data from the vtkConeSource and  create a rendering for the renderer.
		coneMapper = vtk.vtkPolyDataMapper()
		coneMapper.SetInputConnection(reader.GetOutputPort())


		# create an actor for our scene
		if self.isploted:
			coneActor=self.renderer.GetActors().GetLastActor()
			self.renderer.RemoveActor(coneActor)
			
		coneActor = vtk.vtkActor()	
		coneActor.SetMapper(coneMapper)
		# Add actor
		self.renderer.AddActor(coneActor)
		#print self.ren.GetActors().GetNumberOfItems()

		if not self.isploted:
			axes = vtk.vtkAxesActor()
			self.marker = vtk.vtkOrientationMarkerWidget()
			self.marker.SetInteractor( self.widget._Iren )
			self.marker.SetOrientationMarker( axes )
			#Coordinates are expressed as (xmin,ymin,xmax,ymax
			self.marker.SetViewport(0.75,0,1,0.25)
			self.marker.SetEnabled(1)

		self.renderer.ResetCamera()
		self.renderer.ResetCameraClippingRange()
		cam = self.renderer.GetActiveCamera()

		#when you first load the .stl file, you want to see the model at quarte view with no zoom
		cam.SetFocalPoint(0, 0, 0);
		#Camera in Z so it display XY planes.
		cam.SetPosition(1, 1, 1)
		#Up direction is the X not the y
		cam.SetViewUp(-1, 0, 0)
		cam.Zoom(0)
		self.renderer.ResetCamera()
		#coneActor.GetProperty().LightingOff()		
		#cam.Elevation(10)
		#cam.Azimuth(700)

		self.isploted = True
		self.renderer.Render()

		
class AppFrame(wx.Frame):
    def __init__(self,parent,title,iconpath):
        wx.Frame.__init__(self, parent, title = title,size=(800, 600))
        self.title = title
        self.iconPath=iconpath
        self.SetupFrame()        
  
    def settingTitle(self):
             self.SetTitle(self.title+self.vtkPanel.filename)
            
    def Createstatusbar(self):
            self.statusbar = self.CreateStatusBar()
            self.statusbar.SetStatusText("Ready")
            self.isstatusbar = True
            
    def buildToolBar(self):
	    print("buidToolBar")
            self.istoolbar = True            
            events = self.eventsHandler 
            
            toolbar1 = self.CreateToolBar()
            topen = os.path.join(self.iconPath, 'topen.png')
            #assert os.path.exists(topen), 'topen=%r' % topen

            topen = wx.Image(topen, wx.BITMAP_TYPE_ANY)
            topen = toolbar1.AddLabelTool(1, '', wx.BitmapFromImage(topen), longHelp='Loads a Model')

            tcamera = wx.Image(os.path.join(self.iconPath, 'tcamera.png'), wx.BITMAP_TYPE_ANY)
            camera = toolbar1.AddLabelTool(2, '', wx.BitmapFromImage(tcamera), longHelp='Take a Screenshot')

            texit = wx.Image(os.path.join(self.iconPath, 'exit.png'), wx.BITMAP_TYPE_ANY)
            etool = toolbar1.AddLabelTool(wx.ID_EXIT, '', wx.BitmapFromImage(texit), longHelp='Exit App')

            ZMinus = wx.Image(os.path.join(self.iconPath, 'normalZPlaneMinus.png'), wx.BITMAP_TYPE_ANY)
            aZMinus = toolbar1.AddLabelTool(3, '', wx.BitmapFromImage(ZMinus), longHelp='ZMinus')

            ZPlus = wx.Image(os.path.join(self.iconPath, 'normalZPlanePlus.png'), wx.BITMAP_TYPE_ANY)
            aZPlus = toolbar1.AddLabelTool(4, '', wx.BitmapFromImage(ZPlus), longHelp='ZPlus')

            YMinus = wx.Image(os.path.join(self.iconPath, 'normalYPlaneMinus.png'), wx.BITMAP_TYPE_ANY)
            aYMinus = toolbar1.AddLabelTool(5, '', wx.BitmapFromImage(YMinus), longHelp='YMinus')

            YPlus = wx.Image(os.path.join(self.iconPath, 'normalYPlanePlus.png'), wx.BITMAP_TYPE_ANY)
            aYPlus = toolbar1.AddLabelTool(6, '', wx.BitmapFromImage(YPlus), longHelp='YPlus')

            XMinus = wx.Image(os.path.join(self.iconPath, 'normalXPlaneMinus.png'), wx.BITMAP_TYPE_ANY)
            aXMinus = toolbar1.AddLabelTool(7, '', wx.BitmapFromImage(XMinus), longHelp='XMinus')

            XPlus = wx.Image(os.path.join(self.iconPath, 'normalXPlanePlus.png'), wx.BITMAP_TYPE_ANY)
            aXPlus = toolbar1.AddLabelTool(8, '', wx.BitmapFromImage(XPlus), longHelp='XPlus')

            resetZoom = wx.Image(os.path.join(self.iconPath, 'resetZoom.png'), wx.BITMAP_TYPE_ANY)
            aresetZoom = toolbar1.AddLabelTool(9, '', wx.BitmapFromImage(resetZoom), longHelp='resetZoom')

            shade = wx.Image(os.path.join(self.iconPath, 'shade.png'), wx.BITMAP_TYPE_ANY)
            ashade = toolbar1.AddLabelTool(10, '', wx.BitmapFromImage(shade), longHelp='showShade')

            shadeAndEdges = wx.Image(os.path.join(self.iconPath, 'shadeAndEdges.png'), wx.BITMAP_TYPE_ANY)
            ashadeAndEdges = toolbar1.AddLabelTool(11, '', wx.BitmapFromImage(shadeAndEdges), longHelp='showShadeAndEdges')

            edges = wx.Image(os.path.join(self.iconPath, 'edges.png'), wx.BITMAP_TYPE_ANY)
            aedges = toolbar1.AddLabelTool(12, '', wx.BitmapFromImage(edges), longHelp='showEdges')

            showLatticeFFD = wx.Image(os.path.join(self.iconPath, 'FFD.png'), wx.BITMAP_TYPE_ANY)
            ashowLatticeFFD = toolbar1.AddLabelTool(13, '', wx.BitmapFromImage(showLatticeFFD), longHelp='showLatticeFFD')


            toolbar1.Realize()

            self.toolbar1 = toolbar1

            #always vsibile items in the toolbar
            self.Bind(wx.EVT_TOOL, events.onExit, id = wx.ID_EXIT)           
            self.Bind(wx.EVT_TOOL, self.vtkPanel.onTakePicture, id=camera.GetId())
            self.Bind(wx.EVT_TOOL, self.vtkPanel.plot, id=topen.GetId())
            self.Bind(wx.EVT_TOOL, events.viewOnZMinusNormalPlane, id = aZMinus.GetId())
            self.Bind(wx.EVT_TOOL, events.viewOnZPlusNormalPlane, id =aZPlus.GetId())
            self.Bind(wx.EVT_TOOL, events.viewOnYMinusNormalPlane, id = aYMinus.GetId())
            self.Bind(wx.EVT_TOOL, events.viewOnYPlusNormalPlane, id =aYPlus.GetId())
            self.Bind(wx.EVT_TOOL, events.viewOnXMinusNormalPlane, id = aXMinus.GetId())
            self.Bind(wx.EVT_TOOL, events.viewOnXPlusNormalPlane, id =aXPlus.GetId())
            self.Bind(wx.EVT_TOOL, events.shadeObject, id =ashade.GetId())
            self.Bind(wx.EVT_TOOL, events.shadeAndEdgesObject, id =ashadeAndEdges.GetId())
            self.Bind(wx.EVT_TOOL, events.edgesObject, id =aedges.GetId())
            self.Bind(wx.EVT_TOOL, events.resetZoom, id =aresetZoom.GetId())
            self.Bind(wx.EVT_TOOL, events.showLatticeFFD, id =ashowLatticeFFD.GetId())

            
    def buildMenuBar(self):
	    print("buidMenuBar")
            events = self.eventsHandler
            menubar = wx.MenuBar()
             # --------- File Menu -------------------------------------------------
            fileMenu = wx.Menu()
            loadModel = fileMenu.Append(wx.ID_NEW,'Load &Model','Loads a Model Input File')
            sys.stdout.flush()
            loadModel.SetBitmap(wx.Image(os.path.join(self.iconPath, 'topen.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())

            fileMenu.AppendSeparator()
            # ---------     ------------------------------------------------------------
            exitButton = wx.MenuItem(fileMenu,wx.ID_EXIT, 'Exit', 'Exits App')
            exitButton.SetBitmap(wx.Image(os.path.join(self.iconPath, 'exit.png'),wx.BITMAP_TYPE_PNG).ConvertToBitmap())
            fileMenu.AppendItem(exitButton)

             # --------- View Menu -------------------------------------------------
             # status bar at bottom - toggles
            viewMenu = wx.Menu()
            camera = viewMenu.Append(wx.ID_ANY,'Take a Screenshot','Take a Screenshot')
            camera.SetBitmap(wx.Image(os.path.join(self.iconPath, 'tcamera.png'),wx.BITMAP_TYPE_PNG).ConvertToBitmap())


            viewMenu.AppendSeparator()          
            self.showStatusBar = viewMenu.Append(wx.ID_ANY, 'Show/Hide Statusbar','Show Statusbar')
            self.showToolBar   = viewMenu.Append(wx.ID_ANY, 'Show/Hide Toolbar','Show Toolbar')
            viewMenu.AppendSeparator()                      
            self.bkgColorView = viewMenu.Append(wx.ID_ANY,'Change Background Color','Change Background Color')                                         

            # --------- Help / About Menu -----------------------------------------
            helpMenu = wx.Menu()
            self.helpM = helpMenu.Append(wx.ID_ANY, '&About', 'About App')
            #menu bar
            menubar.Append(fileMenu, '&File')
            menubar.Append(viewMenu, '&View')
            menubar.Append(helpMenu, '&Help')
            self.menubar = menubar
            self.SetMenuBar(menubar)

            #bind all menubar events
            self.Bind(wx.EVT_MENU, events.onExit, id=wx.ID_EXIT)
            self.Bind(wx.EVT_MENU, events.onBackgroundColor, id=self.bkgColorView.GetId())
            self.Bind(wx.EVT_MENU, events.onToggleStatusBar, id=self.showStatusBar.GetId())
            self.Bind(wx.EVT_MENU, events.onToggleToolBar, id=self.showToolBar.GetId())
            self.Bind(wx.EVT_MENU, events.onAbout, id=self.helpM.GetId())
            self.Bind(wx.EVT_MENU, self.vtkPanel.plot, id=loadModel.GetId())
            self.Bind(wx.EVT_MENU, self.vtkPanel.onTakePicture, id=camera.GetId())
            
            
    def SetupFrame(self):
            self.eventsHandler = EventsHandler(self)
            self.vtkPanel = vtkPanel(self)
            self.buildMenuBar()
            self.buildToolBar()
            self.Createstatusbar()


def Main():
	print("main")
	appPath = sys.path[0]   
	appFilename=sys.argv[0]
	iconPath = os.path.join(appPath, "icons")
	app = wx.App(redirect=False)
	frame = AppFrame(None, "stl/obj viewer : ", iconPath)
	frame.Show()
	app.MainLoop()

if __name__ == "__main__": 
     Main()
