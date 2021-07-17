from .figure import Figure
from .traces import Scatter, ErrorBand, Histogram, Heatmap, Contour
import plotly.graph_objects as go
import plotly
import numpy as np
import warnings

class PlotlyFigure(Figure):
	def __init__(self):
		super().__init__()
		self.plotly_figure = go.Figure()
	
	# Methods that must be overridden ----------------------------------
	
	def show(self):
		# Overriding this method as specified in the class Figure.
		self.plotly_figure.show()
	
	def save(self, file_name=None, include_plotlyjs='cdn', auto_open=False, **kwargs):
		# Overriding this method as specified in the class Figure.
		if file_name is None:
			file_name = self.title
		if file_name is None: # If it is still None...
			raise ValueError(f'Please provide a name for saving the figure to a file by the <file_name> argument.')
		if file_name[-5:] != '.html':
			file_name += '.html'
		plotly.offline.plot(
			self.plotly_figure,
			filename = file_name,
			auto_open = auto_open,
			include_plotlyjs = include_plotlyjs,
			**kwargs
		)
	
	def draw_layout(self):
		# Overriding this method as specified in the class Figure.
		if self.show_title == True and self.title != None:
			self.plotly_figure.update_layout(title = self.title)
		self.plotly_figure.update_layout(
			xaxis_title = self.xlabel,
			yaxis_title = self.ylabel,
		)
		# Axes scale:
		if self.xscale in [None, 'lin']:
			pass
		elif self.xscale == 'log':
			self.plotly_figure.update_layout(xaxis_type = 'log')
		if self.yscale in [None, 'lin']:
			pass
		elif self.yscale == 'log':
			self.plotly_figure.update_layout(yaxis_type = 'log')
		
		if self.aspect == 'equal':
			self.plotly_figure.update_yaxes(
				scaleanchor = "x",
				scaleratio = 1,
			)
		
		if self.subtitle != None:
			self.plotly_figure.add_annotation(
				text = self.subtitle.replace('\n','<br>'),
				xref = "paper", 
				yref = "paper",
				x = .5, 
				y = 1,
				align = 'left',
				arrowcolor="#ffffff",
				font=dict(
					family="Courier New, monospace",
					color="#999999"
				),
			)
	
	def draw_trace(self, trace):
		# Overriding this method as specified in the class Figure.
		traces_drawing_methods = {
			Scatter: self._draw_scatter,
			ErrorBand: self._draw_errorband,
			Histogram: self._draw_histogram,
			Heatmap: self._draw_heatmap,
			Contour: self._draw_contour,
		}
		if type(trace) not in traces_drawing_methods:
			raise RuntimeError(f"Don't know how to draw a <{type(trace)}> trace...")
		traces_drawing_methods[type(trace)](trace)
	
	# Methods that draw each of the traces (for internal use only) -----
	
	def _draw_scatter(self, scatter: Scatter):
		if not isinstance(scatter, Scatter):
			raise TypeError(f'<scatter> must be an instance of {Scatter}, received object of type {type(scatter)}.')
		self.plotly_figure.add_trace(
			go.Scatter(
				x = scatter.x,
				y = scatter.y,
				name = scatter.label,
				opacity = scatter.alpha,
				mode = translate_marker_and_linestyle_to_Plotly_mode(scatter.marker, scatter.linestyle),
				marker_symbol = map_marker_to_Plotly_markers(scatter.marker),
				showlegend = True if scatter.label is not None else False,
				line = dict(
					dash = map_linestyle_to_Plotly_linestyle(scatter.linestyle),
				)
			)
		)
		self.plotly_figure['data'][-1]['marker']['color'] = rgb2hexastr_color(scatter.color)
		self.plotly_figure['data'][-1]['line']['width'] = scatter.linewidth
	
	def _draw_errorband(self, errorband: ErrorBand):
		if not isinstance(errorband, ErrorBand):
			raise TypeError(f'<errorband> must be an instance of {ErrorBand}, received object of type {type(errorband)}.')
		x = errorband.x
		y1 = errorband.y + errorband.higher
		y2 = errorband.y - errorband.lower
		legendgroup = str(np.random.rand(3))
		# Draw the error band ---
		self.plotly_figure.add_trace(
			go.Scatter(
				x = list(x) + list(x)[::-1],
				y = list(y1) + list(y2)[::-1],
				opacity = errorband.alpha/2,
				mode = 'lines',
				name = errorband.label,
				legendgroup = legendgroup,
				showlegend = False,
				line = dict(
					color = rgb2hexastr_color(errorband.color),
				),
			)
		)
		self.plotly_figure['data'][-1]['fill'] = 'toself'
		self.plotly_figure['data'][-1]['hoveron'] = 'points'
		self.plotly_figure['data'][-1]['line']['width'] = 0
		# Draw the trace itself ---
		self.plotly_figure.add_trace(
			go.Scatter(
				x = errorband.x,
				y = errorband.y,
				name = errorband.label,
				opacity = errorband.alpha,
				mode = translate_marker_and_linestyle_to_Plotly_mode(errorband.marker, errorband.linestyle),
				marker_symbol = map_marker_to_Plotly_markers(errorband.marker),
				showlegend = True if errorband.label is not None else False,
				line = dict(
					dash = map_linestyle_to_Plotly_linestyle(errorband.linestyle),
					color = rgb2hexastr_color(errorband.color),
					width = errorband.linewidth,
				),
				legendgroup = legendgroup,
			)
		)
	
	def _draw_histogram(self, histogram):
		if not isinstance(histogram, Histogram):
			raise TypeError(f'<histogram> must be an instance of {Histogram}, received object of type {type(histogram)}.')
		x = np.array(histogram.x) # Make a copy to avoid touching the original data.
		x[0] = x[1] - (x[3]-x[1]) # Plotly does not plot points in infinity.
		x[-1] = x[-2] + (x[-2]-x[-4]) # Plotly does not plot points in infinity.
		legendgroup = str(np.random.rand(3))
		self.plotly_figure.add_traces(
			go.Scatter(
				x = x, 
				y = histogram.y,
				opacity = histogram.alpha,
				mode = 'lines',
				line = dict(
					dash = map_linestyle_to_Plotly_linestyle(histogram.linestyle),
				),
				legendgroup = legendgroup,
				showlegend = False,
				hoverinfo='skip',
			)
		)
		self.plotly_figure['data'][-1]['marker']['color'] = rgb2hexastr_color(histogram.color)
		self.plotly_figure['data'][-1]['line']['width'] = histogram.linewidth
		if histogram.marker is not None:
			self.plotly_figure.add_traces(
				go.Scatter(
					x = [x[2*i] + (x[2*i+1]-x[2*i])/2 for i in range(int(len(x)/2))],
					y = histogram.y[::2],
					name = histogram.label,
					mode = 'markers',
					marker_symbol = map_marker_to_Plotly_markers(histogram.marker),
					opacity = histogram.alpha,
					line = dict(
						dash = map_linestyle_to_Plotly_linestyle(histogram.linestyle),
					),
					legendgroup = legendgroup,
					hoverinfo = 'skip',
					showlegend = False,
				)
			)
			self.plotly_figure['data'][-1]['marker']['color'] = rgb2hexastr_color(histogram.color)
		self.plotly_figure.add_traces(
			go.Scatter(
				x = [x[2*i] + (x[2*i+1]-x[2*i])/2 for i in range(int(len(x)/2))],
				y = histogram.y[::2],
				name = histogram.label,
				mode = 'lines',
				marker_symbol = map_marker_to_Plotly_markers(histogram.marker),
				opacity = histogram.alpha,
				line = dict(
					dash = map_linestyle_to_Plotly_linestyle(histogram.linestyle),
				),
				legendgroup = legendgroup,
				showlegend = False,
				text = [f'Bin: [-∞, {histogram.bin_edges[0]:.2e}]<br>Count: {histogram.bin_counts[0]:.2e}'] + [f'Bin: [{histogram.bin_edges[i]:.2e}, {histogram.bin_edges[i+1]:.2e}]<br>Count: {histogram.bin_counts[i]:.2e}' for i in range(len(histogram.bin_edges)-1)] + [f'Bin: [{histogram.bin_edges[-1]:.2e},∞]<br>Count: {histogram.bin_counts[-1]:.2e}'],
				hovertemplate = "%{text}",
			)
		)
		self.plotly_figure['data'][-1]['marker']['color'] = rgb2hexastr_color(histogram.color)
		self.plotly_figure['data'][-1]['line']['width'] = 0
		self.plotly_figure.add_traces(
			go.Scatter(
				x = [0],
				y = [float('NaN')],
				name = histogram.label,
				mode = translate_marker_and_linestyle_to_Plotly_mode(histogram.marker, histogram.linestyle),
				marker_symbol = map_marker_to_Plotly_markers(histogram.marker),
				opacity = histogram.alpha,
				showlegend = True if histogram.label != None else False,
				line = dict(
					dash = map_linestyle_to_Plotly_linestyle(histogram.linestyle),
				),
				legendgroup = legendgroup,
			)
		)
		self.plotly_figure['data'][-1]['marker']['color'] = rgb2hexastr_color(histogram.color)
		self.plotly_figure['data'][-1]['line']['width'] = histogram.linewidth
	
	def _draw_heatmap(self, heatmap):
		if not isinstance(heatmap, Heatmap):
			raise TypeError(f'<heatmap> must be an instance of {Heatmap}, received object of type {type(heatmap)}.')
		x = heatmap.x
		y = heatmap.y
		z = heatmap.z
		if heatmap.zscale == 'log' and (z<=0).any():
			warnings.warn('Warning: log color scale was selected and there are <z> values <= 0. In the plot you will see them as NaN.')
			with warnings.catch_warnings():
				warnings.filterwarnings("ignore", message="invalid value encountered in log")
				z = np.log(z)
		self.plotly_figure.add_trace(
			go.Heatmap(
				x = x,
				y = y,
				z = z,
				opacity = heatmap.alpha,
				zmin = heatmap.zlim[0] if heatmap.zlim is not None else None,
				zmax = heatmap.zlim[1] if heatmap.zlim is not None else None,
				colorbar = dict(
					title = ('log ' if heatmap.zscale == 'log' else '') + (heatmap.zlabel if heatmap.zlabel is not None else ''),
					titleside = 'right',
				),
				hovertemplate = f'{(self.xlabel if self.xlabel is not None else "x")}: %{{x}}<br>{(self.ylabel if self.ylabel is not None else "y")}: %{{y}}<br>{(heatmap.zlabel if heatmap.zlabel is not None else "color scale")}: %{{z}}<extra></extra>', # https://community.plotly.com/t/heatmap-changing-x-y-and-z-label-on-tooltip/23588/6
			)
		)
		self.plotly_figure.update_layout(legend_orientation="h")
	
	def _draw_contour(self, contour):
		if not isinstance(contour, Contour):
			raise TypeError(f'<contour> must be an instance of {Contour}, received object of type {type(contour)}.')
		x = contour.x
		y = contour.y
		z = contour.z
		if contour.zscale == 'log' and (z<=0).any():
			warnings.warn('Warning: log color scale was selected and there are <z> values <= 0. In the plot you will see them as NaN.')
			with warnings.catch_warnings():
				warnings.filterwarnings("ignore", message="invalid value encountered in log")
				z = np.log(z)
		lowest_contour = contour.zlim[0] if contour.zlim is not None else contour.z.min()
		highest_contour = contour.zlim[1] if contour.zlim is not None else contour.z.max()
		if hasattr(contour.contours, '__iter__'):
			raise NotImplementedError(f'An iterable specifying which contours to use was not yet implemented. Only implemented an integer number specifying number of equidistant contours.')
		n_contours = contour.contours
		self.plotly_figure.add_trace(
			go.Contour(
				x = x,
				y = y,
				z = z,
				opacity = contour.alpha,
				zmin = contour.zlim[0] if contour.zlim is not None else None,
				zmax = contour.zlim[1] if contour.zlim is not None else None,
				colorbar = dict(
					title = ('log ' if contour.zscale == 'log' else '') + (contour.zlabel if contour.zlabel is not None else ''),
					titleside = 'right',
				),
				hovertemplate = f'{(self.xlabel if self.xlabel is not None else "x")}: %{{x}}<br>{(self.ylabel if self.ylabel is not None else "y")}: %{{y}}<br>{(contour.zlabel if contour.zlabel is not None else "color scale")}: %{{z}}<extra></extra>',
				contours = dict(
					coloring = 'heatmap',
					showlabels = True, # show labels on contours
					labelfont = dict( # label font properties
						color = 'black',
					),
					start = lowest_contour,
					end = highest_contour,
					size = (highest_contour-lowest_contour)/(n_contours),
				)
			)
		)
		self.plotly_figure.update_layout(legend_orientation="h")
		
def translate_marker_and_linestyle_to_Plotly_mode(marker, linestyle):
	"""<marker> and <linestyle> are each one and only one of the valid
	options for each object."""
	if marker is None and linestyle != 'none':
		mode = 'lines'
	elif marker is not None and linestyle != 'none':
		mode = 'lines+markers'
	elif marker is not None and linestyle == 'none':
		mode = 'markers'
	else:
		mode = 'lines'
	return mode

def map_marker_to_Plotly_markers(marker):
	markers_map = {
		'.': 'circle',
		'+': 'cross',
		'x': 'x',
		'o': 'circle-open',
		'*': 'star',
		None: None
	}
	return markers_map[marker]

def map_linestyle_to_Plotly_linestyle(linestyle):
	linestyle_map = {
		'solid': None,
		None: None,
		'none': None,
		'dashed': 'dash',
		'dotted':  'dot',
	}
	return linestyle_map[linestyle]

def rgb2hexastr_color(rgb_color: tuple):
	# Assuming that <rgb_color> is a (r,g,b) tuple.
	color_str = '#'
	for rgb in rgb_color:
		color_hex_code = hex(int(rgb*255))[2:]
		if len(color_hex_code) < 2:
			color_hex_code = f'0{color_hex_code}'
		color_str += color_hex_code
	return color_str
