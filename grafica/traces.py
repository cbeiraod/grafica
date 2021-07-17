from .validation import validate_alpha, validate_color, validate_label, validate_linestyle, validate_linewidth, validate_marker
import numpy as np

VALID_ZSCALES = {'lin','log'}

class Trace:
	"""Most basic trace definition. Other traces should inherit from this
	parent class. This class (and sub classes) are intended to be just
	containers of information, with validation. Nothing else."""
	def __init__(self, label=None):
		self._label = validate_label(label)
	
	@property
	def label(self):
		if hasattr(self, '_label'):
			return self._label
		else:
			return None

class Scatter(Trace):
	def __init__(self, x, y, color, marker=None, linestyle='solid', linewidth=1, alpha=1, label=None):
		"""A Scatter trace is a line in an xy plane given by two arrays 
		of points x=[x1,x2,...] and y=[y1,y2,...].
		- color: RGB tuple.
		- marker: One of {'.','o','+','x','*', None}.
		- linestyle: One of {'solid','dotted','dashed', 'none', None}.
		- linewidth: Float number.
		- alpha: Float number.
		- label: String."""
		super().__init__(label)
		self._color = validate_color(color)
		self._marker = validate_marker(marker)
		self._linestyle = validate_linestyle(linestyle)
		self._linewidth = validate_linewidth(linewidth)
		self._alpha = validate_alpha(alpha)
		if not hasattr(x, '__iter__') or not hasattr(y, '__iter__') or len(x) != len(y):
			raise ValueError(f'<x> and <y> must be two iterables of the same length.')
		self._x = x
		self._y = y
	
	@property
	def color(self):
		return self._color
	
	@property
	def marker(self):
		return self._marker
	
	@property
	def linestyle(self):
		return self._linestyle
	
	@property
	def linewidth(self):
		return self._linewidth
	
	@property
	def alpha(self):
		return self._alpha
	
	@property
	def x(self):
		return self._x
	
	@property
	def y(self):
		return self._y

class ErrorBand(Scatter):
	def __init__(self, x, y, lower, higher, color, marker=None, linestyle='solid', linewidth=1, alpha=1, label=None):
		"""A Scatter trace with a solid and continuous "error band" going
		from <y-lower> up to <y+higher>.
		- color: RGB tuple.
		- marker: One of {'.','o','+','x','*', None}.
		- linestyle: One of {'solid','dotted','dashed', 'none', None}.
		- linewidth: Float number.
		- alpha: Float number.
		- label: String."""
		super().__init__(x=x, y=y, color=color, marker=marker, linestyle=linestyle, linewidth=linewidth, alpha=alpha, label=label)
		if not hasattr(lower, '__iter__') or not hasattr(higher, '__iter__') or not len(higher) == len(lower) == len(x):
			raise ValueError(f'<lower> and <higher> must be two iterables of the same length than <x> and <y>.')
		self._lower = lower
		self._higher = higher
	
	@property
	def lower(self):
		return self._lower
	
	@property
	def higher(self):
		return self._higher

class Histogram(Trace):
	def __init__(self, samples, color, marker=None, linestyle='solid', linewidth=1, alpha=1, label=None, density=False, bins='auto'):
		"""Given an array of samples produces a histogram.
		- color: RGB tuple.
		- marker: One of {'.','o','+','x','*', None}.
		- linestyle: One of {'solid','dotted','dashed', 'none', None}.
		- linewidth: Float number.
		- alpha: Float number.
		- label: String.
		- density: Same as homonym argument in numpy.histogram.
		- bins: Same as homonym argument in numpy.histogram."""
		super().__init__(label)
		self._color = validate_color(color)
		self._marker = validate_marker(marker)
		self._linestyle = validate_linestyle(linestyle)
		self._linewidth = validate_linewidth(linewidth)
		self._alpha = validate_alpha(alpha)
		if not hasattr(samples, '__iter__'):
			raise ValueError(f'<samples> must be iterable.')
		self._samples = samples
		# The following is for handling to whoever is going to plot this a collection of xy points to draw this as a scatter plot.
		samples = np.array(samples)
		hist, bin_edges = np.histogram(
			samples[~np.isnan(samples)], 
			bins = bins,
			density = density,
		)
		x = [-float('inf')]
		y = [sum(samples<bin_edges[0])]
		for idx,count in enumerate(hist):
			x.append(bin_edges[idx])
			x.append(bin_edges[idx])
			y.append(y[-1])
			y.append(count)
		x.append(bin_edges[-1])
		y.append(y[-1])
		x.append(bin_edges[-1])
		y.append(sum(samples>bin_edges[-1]))
		x.append(float('inf'))
		y.append(y[-1])
		self._x = np.array(x)
		self._y = np.array(y)
		
		self._bin_edges = bin_edges
		self._bin_counts = np.array([y[0]] + list(hist) + [y[-1]])
	
	@property
	def color(self):
		return self._color
	
	@property
	def marker(self):
		return self._marker
	
	@property
	def linestyle(self):
		return self._linestyle
	
	@property
	def linewidth(self):
		return self._linewidth
	
	@property
	def alpha(self):
		return self._alpha
	
	@property
	def x(self):
		return self._x
	
	@property
	def y(self):
		return self._y
	
	@property
	def bin_edges(self):
		return self._bin_edges
		
	@property
	def bin_counts(self):
		return self._bin_counts

class Heatmap(Trace):
	def __init__(self, x, y, z, zscale='lin', zlabel=None, zlim=None, alpha=1, label=None):
		"""Produces a 2D colored heat map.
		- x,y: 1D arrays containing the x and y Cartesian values.
		- z: 2D array containing the value at each (x,y).
		- zscale: One of {'lin', 'log'}.
		- zlabel: String with the label to put next to the colorbar (like xlabel or ylabel).
		- zlim: Tuple of the form (zmin, zmax).
		- alpha: Real number for the transparency.
		- label: A label for this heatmap, to distinguish it from other heatmaps."""
		super().__init__(label)
		self._alpha = validate_alpha(alpha)
		if zscale not in VALID_ZSCALES:
			raise ValueError(f'<zscale> must be one of {VALID_ZSCALES}, received {zscale}.')
		self._zscale = zscale
		if zlabel is not None and not isinstance(zlabel, str):
			raise TypeError(f'<zlabel> must be a string, received an object of type {type(zlabel)}.')
		self._zlabel = zlabel
		if zlim is not None:
			try:
				zlim = tuple(zlim)
				if len(zlim) != 2:
					raise ValueError() # Don't care, then I catch all and rise a unique error.
				zlim = tuple([float(_) for _ in zlim])
			except:
				raise ValueError(f'<zlim> must be a tuple of the form (zmin, zmax) with zmin and zmax float numbers.')
		self._zlim = zlim
		_x = np.array(x)
		_y = np.array(y)
		_z = np.array(z)
		if any([xy.ndim != 1 for xy in [_x,_y]]):
			raise ValueError(f'<x>, <y> must be one dimensional arrays, received x.ndim={_x.ndim}, y.ndim={_y.ndim}.')
		if _z.ndim != 2:
			raise ValueError(f'<z> must be a two dimensional array, received z.ndim={_z.ndim}')
		if _z.shape != (len(_y),len(_x)):
			raise ValueError(f'The shape of <z> must be (len(y),len(x)). Received z.shape={_z.shape}, (len(y),len(x))={(len(_y),len(_x))}.')
		self._x = _x
		self._y = _y
		self._z = _z

	@property
	def x(self):
		return self._x
	
	@property
	def y(self):
		return self._y
	
	@property
	def z(self):
		return self._z
	
	@property
	def zscale(self):
		return self._zscale
	
	@property
	def zlabel(self):
		return self._zlabel
	
	@property
	def zlim(self):
		return self._zlim
	
	@property
	def alpha(self):
		return self._alpha
	
	@property
	def label(self):
		return self._label

class Contour(Trace):
	def __init__(self, x, y, z, zscale='lin', zlabel=None, zlim=None, alpha=1, contours=None, label=None):
		"""Produces a 2D colored heat map.
		- x,y: 1D arrays containing the x and y Cartesian values.
		- z: 2D array containing the value at each (x,y).
		- zscale: One of {'lin', 'log'}.
		- zlabel: String with the label to put next to the colorbar (like xlabel or ylabel).
		- zlim: Tuple of the form (zmin, zmax).
		- alpha: Real number for the transparency.
		- contours: Integer specifying the number of contours or iterable containing the values for the contour levels.
		- label: A label for this contour, to distinguish it from other contours."""
		super().__init__(label)
		self._alpha = validate_alpha(alpha)
		if zscale not in VALID_ZSCALES:
			raise ValueError(f'<zscale> must be one of {VALID_ZSCALES}, received {zscale}.')
		self._zscale = zscale
		if zlabel is not None and not isinstance(zlabel, str):
			raise TypeError(f'<zlabel> must be a string, received an object of type {type(zlabel)}.')
		self._zlabel = zlabel
		if zlim is not None:
			try:
				zlim = tuple(zlim)
				if len(zlim) != 2:
					raise ValueError() # Don't care, then I catch all and rise a unique error.
				zlim = tuple([float(_) for _ in zlim])
			except:
				raise ValueError(f'<zlim> must be a tuple of the form (zmin, zmax) with zmin and zmax float numbers.')
		self._zlim = zlim
		_x = np.array(x)
		_y = np.array(y)
		_z = np.array(z)
		if any([xy.ndim != 1 for xy in [_x,_y]]):
			raise ValueError(f'<x>, <y> must be one dimensional arrays, received x.ndim={_x.ndim}, y.ndim={_y.ndim}.')
		if _z.ndim != 2:
			raise ValueError(f'<z> must be a two dimensional array, received z.ndim={_z.ndim}')
		if _z.shape != (len(_y),len(_x)):
			raise ValueError(f'The shape of <z> must be (len(y),len(x)). Received z.shape={_z.shape}, (len(y),len(x))={(len(_y),len(_x))}.')
		self._x = _x
		self._y = _y
		self._z = _z
		if contours is None:
			contours = 5
		if not isinstance(contours, int):
			if not hasattr(contours, '__iter__'):
				raise ValueError(f'<contours> must be an integer number denoting the number of contours to use or an iterable of float numbers specifying the contours.')
			for f in contours:
				try:
					float(f)
				except:
					raise ValueError(f'<contours> must be an iterable of float numbers, but the element {f} was found within <contours> which cannot be interpreted as a float number.')
		self._contours = contours

	@property
	def x(self):
		return self._x
	
	@property
	def y(self):
		return self._y
	
	@property
	def z(self):
		return self._z
	
	@property
	def zscale(self):
		return self._zscale
	
	@property
	def zlabel(self):
		return self._zlabel
	
	@property
	def zlim(self):
		return self._zlim
	
	@property
	def alpha(self):
		return self._alpha
	
	@property
	def label(self):
		return self._label
	
	@property
	def contours(self):
		return self._contours

