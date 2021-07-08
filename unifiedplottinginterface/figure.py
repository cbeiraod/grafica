import numpy as np
from .validation import validate_kwargs

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
	
	def scatter(self, x, y, **kwargs):
		"""Given two iterables <x> and <y> produces a scatter plot.
		kwargs: Any of {'label','color','marker','linestyle','linewidth',
		'alpha'} is supported. Additional arguments rise a ValueError.
		"""
		if kwargs.get('color') is None:
			kwargs['color'] = self.pick_default_color()
		kwargs = validate_kwargs({'label','color','marker','linestyle','linewidth','alpha'}, kwargs)
		if not hasattr(x, '__iter__') or not hasattr(y, '__iter__'):
			raise ValueError(f'<x> and <y> must be iterables, at least one of them is not.')
		if len(x) != len(y):
			raise ValueError(f'<x> and <y> must be of the same length but len(x)={len(x)} and len(y)={len(y)}.')
		trace = {'type': 'scatter', 'data': {'x':x,'y':y}}
		for arg in kwargs:
			trace[arg] = kwargs[arg]
		self.traces.append(trace)
	
	def histogram(self, samples, density=False, bins='auto', **kwargs):
		"""Given a collection of sample data <x> produces a histogram
		plot.
		samples: Array like containing the data.
		density: Same behavior as density argument of numpy.histogram function.
		bins: Same behavior as the bins argument of numpy.histogram function.
		kwargs: Any of {'label','color','marker','linestyle','linewidth',
		'alpha'} is supported."""
		if kwargs.get('color') is None:
			kwargs['color'] = self.pick_default_color()
		kwargs = validate_kwargs({'label','color','marker','linestyle','linewidth','alpha'}, kwargs)
		if not hasattr(samples, '__iter__'):
			raise ValueError(f'<samples> must be iterable.')
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
		trace = {'type': 'histogram', 'data': {'x':np.array(x),'y':np.array(y), 'bin_edges': np.array(bin_edges), 'bin_count': np.array([y[0]] + list(hist) + [y[-1]])}}
		for arg in kwargs:
			trace[arg] = kwargs[arg]
		self.traces.append(trace)
	
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
