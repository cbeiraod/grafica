import numpy as np
import warnings
from shutil import copyfile
from .utils import validate_kwargs, GENERAL_KWARGS_FOR_PLOTTING_METHODS

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
	
	DEFAULT_LINEWIDTH = 1
	DEFAULT_ALPHA = 1
	
	def scatter(self, x, y, **kwargs):
		"""
		Given two iterables <x> and <y> produces a scatter plot.
		kwargs: Any of {'label','color','marker','linestyle','linewidth',
		'alpha'} is supported. Additional arguments rise a ValueError.
		"""
		# Arguments that must have a default value ---
		if 'linewidth' not in kwargs:
			kwargs['linewidth'] = self.DEFAULT_LINEWIDTH
		if 'alpha' not in kwargs:
			kwargs['alpha'] = self.DEFAULT_ALPHA
		if 'color' not in kwargs:
			kwargs['color'] = self.pick_default_color()
		# --------------------------------------------
		kwargs = validate_kwargs({'label','color','marker','linestyle','linewidth','alpha'}, kwargs)
		if not hasattr(x, '__iter__') or not hasattr(y, '__iter__'):
			raise ValueError(f'<x> and <y> must be iterables, at least one of them is not.')
		if len(x) != len(y):
			raise ValueError(f'<x> and <y> must be of the same length but len(x)={len(x)} and len(y)={len(y)}.')
		trace = {'type': 'scatter', 'data': {'x':x,'y':y}}
		for arg in kwargs:
			trace[arg] = kwargs[arg]
		self.traces.append(trace)
