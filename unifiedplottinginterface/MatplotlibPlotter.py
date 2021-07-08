from .figure import Figure
from .plotter import Plotter
import matplotlib.pyplot as plt
import numpy as np

class MatplotlibPlotter(Plotter):
	def __init__(self, figure):
		super().__init__(figure)
		fig, ax = plt.subplots()
		self.matplotlib_figure = fig
		self.matplotlib_axes = ax
		self.draw_figure()
		self.draw_traces()
	
	def show(self):
		plt.show()
	
	def save(self, file_name=None, format='png', facecolor=(1,1,1,0), **kwargs):
		if file_name is None:
			file_name = self.parent_figure.title
		if file_name is None:
			raise ValueError(f'Please provide a name for saving the figure to a file by the <file_name> argument.')
		if file_name[-4] != '.':
			file_name = f'{file_name}.{format}'
		self.matplotlib_figure.savefig(fname=file_name, format=format, facecolor=facecolor, **kwargs)
	
	def draw_figure(self):
		self.matplotlib_axes.set_xlabel(self.parent_figure.xlabel)
		self.matplotlib_axes.set_ylabel(self.parent_figure.ylabel)
		self.matplotlib_axes.set_xscale(map_axes_scale_to_Matplotlib_scale(self.parent_figure.xscale))
		self.matplotlib_axes.set_yscale(map_axes_scale_to_Matplotlib_scale(self.parent_figure.yscale))
		if self.parent_figure.title != None:
			self.matplotlib_figure.canvas.set_window_title(self.parent_figure.title)
			if self.parent_figure.show_title == True:
				self.matplotlib_figure.suptitle(self.parent_figure.title)
		if self.parent_figure.aspect == 'equal':
			self.matplotlib_axes.set_aspect('equal')
		if self.parent_figure.subtitle != None:
			self.matplotlib_axes.set_title(self.parent_figure.subtitle)
	
	def draw_traces(self):
		traces_drawing_methods = {
			'scatter': self.draw_scatter,
			'histogram': self.draw_histogram,
		}
		for trace in self.parent_figure.traces:
			if trace['type'] not in traces_drawing_methods:
				raise RuntimeError(f"Don't know how to draw a <{trace['type']}> trace...")
			traces_drawing_methods[trace['type']](trace)
	
	def draw_scatter(self, scatter):
		"""Draws a scatter plot created by super().scatter."""
		kwargs4matplotlib = dict(scatter) # Make a copy.
		kwargs4matplotlib.pop('data')
		kwargs4matplotlib.pop('type')
		kwargs4matplotlib['linestyle'] = map_linestyle_to_Matplotlib_linestyle(kwargs4matplotlib.get('linestyle'))
		self.matplotlib_axes.plot(
			scatter['data']['x'],
			scatter['data']['y'],
			**kwargs4matplotlib,
		)
		if scatter.get('label') != None: # If you gave me a label it is obvious (for me) that you want to display it, no?
			self.matplotlib_axes.legend()
	
	def draw_histogram(self, histogram):
		"""Draws a histogram plot created by super().histogram."""
		kwargs4matplotlib = dict(histogram) # Make a copy.
		kwargs4matplotlib.pop('data')
		kwargs4matplotlib.pop('type')
		kwargs4matplotlib['linestyle'] = map_linestyle_to_Matplotlib_linestyle(kwargs4matplotlib.get('linestyle'))
		x = np.array(histogram['data']['x']) # Make a copy to avoid touching the original data.
		x[0] = x[1] - (x[3]-x[1]) # Matplotlib does not plot points in infinity.
		x[-1] = x[-2] + (x[-2]-x[-4]) # Matplotlib does not plot points in infinity.
		self.matplotlib_axes.plot(
			x,
			histogram['data']['y'],
			**kwargs4matplotlib,
		)
		if histogram.get('label') != None: # If you gave me a label it is obvious (for me) that you want to display it, no?
			self.matplotlib_axes.legend()
	
def map_axes_scale_to_Matplotlib_scale(scale):
	if scale is None or scale == 'lin':
		return 'linear'
	elif scale == 'log':
		return 'log'
	else:
		raise ValueError(f"Don't know the meaning of scale = {scale}.")

def map_linestyle_to_Matplotlib_linestyle(linestyle):
	linestyle_map = {
		'solid': 'solid',
		None: 'solid',
		'none': 'none',
		'dashed': 'dashed',
		'dotted':  'dotted',
	}
	return linestyle_map[linestyle]
