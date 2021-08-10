from .figure import Figure
from .traces import Scatter, ErrorBand, Histogram, Heatmap, Contour, KDE
import matplotlib.pyplot as plt
import matplotlib.colors as matplotlib_colors
import numpy as np
import warnings

class MatplotlibFigure(Figure):
	def __init__(self):
		super().__init__()
		fig, ax = plt.subplots()
		self.matplotlib_figure = fig
		self.matplotlib_axes = ax
	
	# Methods that must be overridden ----------------------------------
	
	def show(self):
		# Overriding this method as specified in the class Figure.
		plt.show()
	
	def save(self, file_name=None, format='png', facecolor=(1,1,1,0), **kwargs):
		# Overriding this method as specified in the class Figure.
		if file_name is None:
			file_name = self.title
		if file_name is None:
			raise ValueError(f'Please provide a name for saving the figure to a file by the <file_name> argument.')
		if file_name[-4] != '.':
			file_name = f'{file_name}.{format}'
		self.matplotlib_figure.savefig(fname=file_name, format=format, facecolor=facecolor, **kwargs)
	
	def draw_layout(self):
		# Overriding this method as specified in the class Figure.
		self.matplotlib_axes.set_xlabel(self.xlabel)
		self.matplotlib_axes.set_ylabel(self.ylabel)
		self.matplotlib_axes.set_xscale(map_axes_scale_to_Matplotlib_scale(self.xscale))
		self.matplotlib_axes.set_yscale(map_axes_scale_to_Matplotlib_scale(self.yscale))
		if self.title != None:
			self.matplotlib_figure.canvas.manager.set_window_title(self.title)
			if self.show_title == True:
				self.matplotlib_figure.suptitle(self.title)
		if self.aspect == 'equal':
			self.matplotlib_axes.set_aspect('equal')
		if self.subtitle != None:
			self.matplotlib_axes.set_title(self.subtitle)
	
	def draw_trace(self, trace):
		# Overriding this method as specified in the class Figure.
		traces_drawing_methods = {
			Scatter: self._draw_scatter,
			Histogram: self._draw_histogram,
			Heatmap: self._draw_heatmap,
			Contour: self._draw_contour,
			ErrorBand: self._draw_errorband,
			KDE: self._draw_scatter,
		}
		if type(trace) not in traces_drawing_methods:
			raise RuntimeError(f"Don't know how to draw a {type(trace)} trace...")
		traces_drawing_methods[type(trace)](trace)
	
	# Methods that draw each of the traces (for internal use only) -----
	
	def _draw_scatter(self, scatter):
		if not isinstance(scatter, Scatter):
			raise TypeError(f'<scatter> must be an instance of {Scatter}, received object of type {type(scatter)}.')
		self.matplotlib_axes.plot(
			scatter.x,
			scatter.y,
			color = scatter.color,
			marker = scatter.marker,
			linestyle = map_linestyle_to_Matplotlib_linestyle(scatter.linestyle),
			linewidth = scatter.linewidth,
			alpha = scatter.alpha,
			label = scatter.label,
		)
		if scatter.label != None: # If you gave me a label it is obvious (for me) that you want to display it, no?
			self.matplotlib_axes.legend()
	
	def _draw_errorband(self, errorband: ErrorBand):
		if not isinstance(errorband, ErrorBand):
			raise TypeError(f'<errorband> must be an instance of {ErrorBand}, received object of type {type(errorband)}.')
		self.matplotlib_axes.fill_between(
			errorband.x,
			errorband.y - errorband.lower,
			errorband.y + errorband.higher,
			alpha = errorband.alpha/2,
			color = errorband.color,
			linewidth = 0,
		)
		self.matplotlib_axes.plot(
			errorband.x,
			errorband.y,
			color = errorband.color,
			marker = errorband.marker,
			linestyle = map_linestyle_to_Matplotlib_linestyle(errorband.linestyle),
			linewidth = errorband.linewidth,
			alpha = errorband.alpha,
			label = errorband.label,
		)
		if errorband.label != None: # If you gave me a label it is obvious (for me) that you want to display it, no?
			self.matplotlib_axes.legend()
	
	def _draw_histogram(self, histogram):
		if not isinstance(histogram, Histogram):
			raise TypeError(f'<histogram> must be an instance of {Histogram}, received object of type {type(histogram)}.')
		x = np.array(histogram.x) # Make a copy to avoid touching the original data.
		x[0] = x[1] - (x[3]-x[1]) # Matplotlib does not plot points in infinity.
		x[-1] = x[-2] + (x[-2]-x[-4]) # Matplotlib does not plot points in infinity.
		self.matplotlib_axes.plot(
			x,
			histogram.y,
			color = histogram.color,
			linewidth = histogram.linewidth,
			linestyle = map_linestyle_to_Matplotlib_linestyle(histogram.linestyle),
			alpha = histogram.alpha,
		)
		
		self.matplotlib_axes.plot(
			[x[2*i] + (x[2*i+1]-x[2*i])/2 for i in range(int(len(x)/2))][1:-1],
			histogram.y[::2][1:-1],
			color = histogram.color,
			marker = histogram.marker,
			linestyle = 'none',
		)
		self.matplotlib_axes.plot(
			[0],
			[float('NaN')],
			color = histogram.color,
			marker = histogram.marker,
			label = histogram.label,
		)
		if histogram.label is not None: # If you gave me a label it is obvious (for me) that you want to display it, no?
			self.matplotlib_axes.legend()
	
	def _draw_heatmap(self, heatmap):
		if not isinstance(heatmap, Heatmap):
			raise TypeError(f'<heatmap> must be an instance of {Heatmap}, received object of type {type(heatmap)}.')
		x = heatmap.x
		y = heatmap.y
		z = np.array(heatmap.z) # Make a copy so I don't touch the original.
		vmin = heatmap.zlim[0] if heatmap.zlim is not None else np.nanmin(z)
		vmax = heatmap.zlim[1] if heatmap.zlim is not None else np.nanmax(z)
		if heatmap.zscale in [None, 'lin']: # Linear scale
			norm = matplotlib_colors.Normalize(vmin=vmin, vmax=vmax)
		elif heatmap.zscale == 'log':
			if (z<=0).any():
				warnings.warn('Warning: log color scale was selected and there are <z> values <= 0. In the plot you will see them as NaN.')
				z[z<=0] = float('Nan')
			norm = matplotlib_colors.LogNorm(vmin=max(vmin,np.nanmin(z)), vmax=vmax)
		cs = self.matplotlib_axes.pcolormesh(
			x, 
			y, 
			z, 
			rasterized = True, # To avoid heavy PDF files. After all, the heatmap plot is a pixel map...
			shading = 'auto', 
			cmap = 'plasma',
			norm = norm, 
		)
		cbar = self.matplotlib_figure.colorbar(cs)
		if heatmap.zlabel is not None:
			cbar.set_label(heatmap.zlabel, rotation = 90)
	
	def _draw_contour(self, contour):
		if not isinstance(contour, Contour):
			raise TypeError(f'<contour> must be an instance of {Contour}, received object of type {type(contour)}.')
		x = contour.x
		y = contour.y
		z = np.array(contour.z) # Make a copy so I don't touch the original.
		vmin = contour.zlim[0] if contour.zlim is not None else np.nanmin(z)
		vmax = contour.zlim[1] if contour.zlim is not None else np.nanmax(z)
		if contour.zscale in [None, 'lin']: # Linear scale
			norm = matplotlib_colors.Normalize(vmin=vmin, vmax=vmax)
		elif contour.zscale == 'log':
			if (z<=0).any():
				warnings.warn('Warning: log color scale was selected and there are <z> values <= 0. In the plot you will see them as NaN.')
				z[z<=0] = float('Nan')
			norm = matplotlib_colors.LogNorm(vmin=max(vmin,np.nanmin(z)), vmax=vmax)
		cs = self.matplotlib_axes.pcolormesh(
			x, 
			y, 
			z, 
			rasterized = True, # To avoid heavy PDF files. After all, the heatmap plot is a pixel map...
			shading = 'auto', 
			cmap = 'plasma',
			norm = norm,
			alpha = contour.alpha,
		)
		cbar = self.matplotlib_figure.colorbar(cs)
		if contour.zlabel is not None:
			cbar.set_label(contour.zlabel, rotation = 90)
		cs = self.matplotlib_axes.contour(
			x, 
			y, 
			z, 
			colors = 'k',
			norm = norm,
			alpha = contour.alpha,
			levels = contour.contours,
		)
		self.matplotlib_axes.clabel(cs, inline=True)
	
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
