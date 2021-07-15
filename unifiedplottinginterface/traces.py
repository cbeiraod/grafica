from .validation import validate_alpha, validate_color, validate_label, validate_linestyle, validate_linewidth, validate_marker
import numpy as np

class Trace:
	"""Most basic trace definition. Other traces should inherit from this
	parent class. This class (and sub classes) are intended to be just
	containers of information, with validation. Nothing else."""
	def __init__(self, label=None):
		self._label = validate_label(label)
	
	@property
	def label(self):
		return self._label

class Scatter(Trace):
	def __init__(self, x, y, color, marker=None, linestyle='solid', linewidth=1, alpha=1, label=None):
		"""A Scatter trace is a line in an xy plane given by two arrays of points x=[x1,x2,...] and y=[y1,y2,...]."""
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

class Histogram(Trace):
	def __init__(self, samples, color, marker=None, linestyle='solid', linewidth=1, alpha=1, label=None, density=False, bins='auto'):
		"""We all know what a histogram is."""
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
