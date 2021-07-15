import numpy as np
from .traces import Trace, Scatter, Histogram, Heatmap

_VALID_AXIS_SCALES = {'lin','log'}

class Figure:
	"""
	This class defines the interface and handles all the information until
	the plots are "drawn" with a specific package.
	"""
	
	def __init__(self):
		self._show_title = True
		self.traces = []
	
	# Figure properties ------------------------------------------------
	# 	Figure properties are those things that belong to the figure
	# 	itself and not to particular traces. Examples: title, x scale, etc.
	
	@property
	def title(self):
		return self._title if hasattr(self, '_title') else None
	@title.setter
	def title(self, title):
		self._title = str(title)
	
	@property
	def show_title(self):
		return self._show_title if hasattr(self, '_show_title') else None
	@show_title.setter
	def show_title(self, show: bool):
		if show not in [True, False]:
			raise TypeError(f'<show_title> expects either True or False, received {show}.')
		self._show_title = show
	
	@property
	def subtitle(self):
		return self._subtitle if hasattr(self, '_subtitle') else None
	@subtitle.setter
	def subtitle(self, subtitle):
		self._subtitle = str(subtitle)
	
	@property
	def xlabel(self):
		return self._xlabel if hasattr(self, '_xlabel') else None
	@xlabel.setter
	def xlabel(self, xlabel):
		self._xlabel = str(xlabel)
	
	@property
	def ylabel(self):
		return self._ylabel if hasattr(self, '_ylabel') else None
	@ylabel.setter
	def ylabel(self, ylabel):
		self._ylabel = str(ylabel)
	
	@property
	def xscale(self):
		return self._xscale if hasattr(self, '_xscale') else None
	@xscale.setter
	def xscale(self, xscale):
		if xscale not in _VALID_AXIS_SCALES:
			raise ValueError(f'<xscale> must be one of {_VALID_AXIS_SCALES}, received {xscale}.')
		self._xscale = xscale
	
	@property
	def yscale(self):
		return self._yscale if hasattr(self, '_yscale') else None
	@yscale.setter
	def yscale(self, yscale):
		if yscale not in _VALID_AXIS_SCALES:
			raise ValueError(f'<yscale> must be one of {_VALID_AXIS_SCALES}, received {yscale}.')
		self._yscale = yscale
	
	@property
	def aspect(self):
		return self._aspect if hasattr(self, '_aspect') else None
	@aspect.setter
	def aspect(self, aspect):
		VALID_ASPECTS = {'equal',None}
		if aspect not in VALID_ASPECTS:
			raise ValueError(f'<aspect> must be one of {VALID_ASPECTS}, received {aspect}.')
		self._aspect = aspect
	
	def set(self, **kwargs):
		for key in kwargs.keys():
			if not hasattr(self, key):
				raise ValueError(f'Cannot set <{key}>, invalid property.')
			setattr(self, f'{key}', kwargs[key])
	# ------------------------------------------------------------------
	
	def add_trace(self, trace):
		if not isinstance(trace, Trace):
			raise TypeError(f'<trace> must be an instance of Trace, received an object of type {type(trace)}')
		self.traces.append(trace)
	
	def scatter(self, x, y, **kwargs):
		"""Given two iterables <x> and <y> produces a scatter plot in the xy plane."""
		if kwargs.get('color') is None:
			kwargs['color'] = self.pick_default_color()
		self.add_trace(Scatter(x, y, **kwargs))
	
	def histogram(self, samples, **kwargs):
		"""Given a collection of sample data <x> produces a histogram plot.
		samples: Array like containing the data."""
		if kwargs.get('color') is None:
			kwargs['color'] = self.pick_default_color()
		self.add_trace(Histogram(samples, **kwargs))
	
	def heatmap(self, x, y, z, **kwargs):
		"""Produces a 2D colored heatmap in Cartesian coordinates. z is 
		the color dimension.
		- x, y: One dimensional arrays with the xy values respectively.
		- z: Two dimensional array containing the magnitude that will be 
		translated into a color. The shape of z must be (len(y),len(x)).
		What happens with NaN or missing values is a problem of the specific
		plotter."""
		self.add_trace(Heatmap(x,y,z,**kwargs))
	
	# ~ def contour(self, x, y, z, zscale='lin', zlabel=None, zlim=None, contours=None, **kwargs):
		# ~ """Produces a 2D contour plot in Cartesian coordinates. z is 
		# ~ the "height" dimension.
		# ~ - x, y: One dimensional arrays with the xy values respectively.
		# ~ - z: Two dimensional array containing the magnitude that will be 
		# ~ translated into a height. The shape of z must be (len(y),len(x)).
		# ~ What happens with NaN or missing values is a problem of the specific
		# ~ plotter.
		# ~ - zlabel: A string with the label for the z dimension.
		# ~ - zscale: Either 'lin' or 'log' for linear or logarithmic.
		# ~ - zlim: (zmin, zmax).
		# ~ - contours: Integer number stating number of contours to plot.
		# ~ with the specific contours to use.
		# ~ - kwargs:
			# ~ - alpha: A float specifying the transparency."""
		# ~ # Validation of arguments ---
		# ~ kwargs = validate_kwargs({'alpha'}, kwargs)
		# ~ if zscale not in _VALID_AXIS_SCALES:
			# ~ raise ValueError(f'<zscale> must be one of {_VALID_AXIS_SCALES}, received {zscale}.')
		# ~ if zlabel is not None and not isinstance(zlabel, str):
			# ~ raise TypeError(f'<zlabel> must be a string, received an object of type {type(zlabel)}.')
		# ~ if zlim is not None:
			# ~ try:
				# ~ zlim = tuple(zlim)
				# ~ if len(zlim) != 2:
					# ~ raise ValueError() # Don't care, then I catch all and rise a unique error.
				# ~ zlim = tuple([float(_) for _ in zlim])
			# ~ except:
				# ~ raise ValueError(f'<zlim> must be a tuple of the form (zmin, zmax) with zmin and zmax float numbers.')
		# ~ _x = np.array(x)
		# ~ _y = np.array(y)
		# ~ _z = np.array(z)
		# ~ if any([xy.ndim != 1 for xy in [_x,_y]]):
			# ~ raise ValueError(f'<x>, <y> must be one dimensional arrays, received x.ndim={_x.ndim}, y.ndim={_y.ndim}.')
		# ~ if _z.ndim != 2:
			# ~ raise ValueError(f'<z> must be a two dimensional array, received z.ndim={_z.ndim}')
		# ~ if _z.shape != (len(y),len(x)):
			# ~ raise ValueError(f'The shape of <z> must be (len(y),len(x)). Received z.shape={_z.shape}, (len(y),len(x))={(len(y),len(x))}.')
		# ~ if contours is not None:
			# ~ try:
				# ~ contours = int(contours)
			# ~ except:
				# ~ raise TypeError(f'<contours> must be an integer number, received an object of type {type(contours)}.')
		# ~ # Arguments are validated ---
		# ~ contour_specific_arguments = {'zscale': zscale, 'zlabel': zlabel, 'zlim': zlim, 'contours': contours}
		# ~ trace = {'type': 'contour', 'data': {'x':_x,'y':_y, 'z': _z}}
		# ~ for k,v in {**kwargs, **contour_specific_arguments}.items():
			# ~ trace[k] = v
		# ~ self.traces.append(trace)
	# ------------------------------------------------------------------
	
	DEFAULT_COLORS = [
		(255, 59, 59),
		(52, 71, 217),
		(4, 168, 2),
		(224, 146, 0),
		(224, 0, 183),
		(0, 230, 214),
		(140, 0, 0),
		(9, 0, 140),
		(107, 0, 96),
	]
	def pick_default_color(self):
		color = self.DEFAULT_COLORS[0]
		self.DEFAULT_COLORS = self.DEFAULT_COLORS[1:] + [self.DEFAULT_COLORS[0]]
		return color
