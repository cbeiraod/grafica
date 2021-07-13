from .figure import Figure
from .plotter import Plotter
import plotly.graph_objects as go
import plotly
import numpy as np
import warnings

class PlotlyPlotter(Plotter):
	def __init__(self, figure):
		super().__init__(figure)
		self.plotly_figure = go.Figure()
		self.draw_figure()
		self.draw_traces()
	
	def show(self):
		self.plotly_figure.show()
	
	def save(self, file_name=None, include_plotlyjs='cdn', auto_open=False, **kwargs):
		if file_name is None:
			file_name = self.parent_figure.title
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
	
	def draw_figure(self):
		if self.parent_figure.show_title == True and self.parent_figure.title != None:
			self.plotly_figure.update_layout(title = self.parent_figure.title)
		self.plotly_figure.update_layout(
			xaxis_title = self.parent_figure.xlabel,
			yaxis_title = self.parent_figure.ylabel,
		)
		# Axes scale:
		if self.parent_figure.xscale in [None, 'lin']:
			pass
		elif self.parent_figure.xscale == 'log':
			self.plotly_figure.update_layout(xaxis_type = 'log')
		if self.parent_figure.yscale in [None, 'lin']:
			pass
		elif self.parent_figure.yscale == 'log':
			self.plotly_figure.update_layout(yaxis_type = 'log')
		
		if self.parent_figure.aspect == 'equal':
			self.plotly_figure.update_yaxes(
				scaleanchor = "x",
				scaleratio = 1,
			)
		
		if self.parent_figure.subtitle != None:
			self.plotly_figure.add_annotation(
				text = self.parent_figure.subtitle.replace('\n','<br>'),
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
	
	def draw_traces(self):
		traces_drawing_methods = {
			'scatter': self.draw_scatter,
			'histogram': self.draw_histogram,
			'heatmap': self.draw_heatmap,
			'contour': self.draw_contour,
		}
		for trace in self.parent_figure.traces:
			if trace['type'] not in traces_drawing_methods:
				raise RuntimeError(f"Don't know how to draw a <{trace['type']}> trace...")
			traces_drawing_methods[trace['type']](trace)
	
	def draw_scatter(self, scatter):
		"""Draws a scatter plot created by super().scatter."""
		self.plotly_figure.add_trace(
			go.Scatter(
				x = scatter['data']['x'],
				y = scatter['data']['y'],
				name = scatter.get('label'),
				opacity = scatter.get('alpha'),
				mode = translate_marker_and_linestyle_to_Plotly_mode(scatter.get('marker'), scatter.get('linestyle')),
				marker_symbol = map_marker_to_Plotly_markers(scatter.get('marker')),
				showlegend = True if scatter.get('label') != None else False,
				line = dict(
					dash = map_linestyle_to_Plotly_linestyle(scatter.get('linestyle')),
				)
			)
		)
		self.plotly_figure['data'][-1]['marker']['color'] = rgb2hexastr_color(scatter.get('color'))
		self.plotly_figure['data'][-1]['line']['width'] = scatter.get('linewidth')
	
	def draw_histogram(self, histogram):
		"""Draws a histogram plot created by super().histogram."""
		x = np.array(histogram['data']['x']) # Make a copy to avoid touching the original data.
		x[0] = x[1] - (x[3]-x[1]) # Plotly does not plot points in infinity.
		x[-1] = x[-2] + (x[-2]-x[-4]) # Plotly does not plot points in infinity.
		legendgroup = str(np.random.rand(3))
		self.plotly_figure.add_traces(
			go.Scatter(
				x = x, 
				y = histogram['data']['y'],
				opacity = histogram.get('alpha'),
				mode = 'lines',
				line = dict(
					dash = map_linestyle_to_Plotly_linestyle(histogram.get('linestyle')),
				),
				legendgroup = legendgroup,
				showlegend = False,
				hoverinfo='skip',
			)
		)
		self.plotly_figure['data'][-1]['marker']['color'] = rgb2hexastr_color(histogram.get('color'))
		self.plotly_figure['data'][-1]['line']['width'] = histogram.get('linewidth')
		if histogram.get('marker') is not None:
			self.plotly_figure.add_traces(
				go.Scatter(
					x = [x[2*i] + (x[2*i+1]-x[2*i])/2 for i in range(int(len(x)/2))],
					y = histogram['data']['y'][::2],
					name = histogram.get('label'),
					mode = 'markers',
					marker_symbol = map_marker_to_Plotly_markers(histogram.get('marker')),
					opacity = histogram.get('alpha'),
					line = dict(
						dash = map_linestyle_to_Plotly_linestyle(histogram.get('linestyle')),
					),
					legendgroup = legendgroup,
					hoverinfo = 'skip',
					showlegend = False,
				)
			)
			self.plotly_figure['data'][-1]['marker']['color'] = rgb2hexastr_color(histogram.get('color'))
		self.plotly_figure.add_traces(
			go.Scatter(
				x = [x[2*i] + (x[2*i+1]-x[2*i])/2 for i in range(int(len(x)/2))],
				y = histogram['data']['y'][::2],
				name = histogram.get('label'),
				mode = 'lines',
				marker_symbol = map_marker_to_Plotly_markers(histogram.get('marker')),
				opacity = histogram.get('alpha'),
				line = dict(
					dash = map_linestyle_to_Plotly_linestyle(histogram.get('linestyle')),
				),
				legendgroup = legendgroup,
				showlegend = False,
				text = [f'Bin: [-∞, {histogram["data"]["bin_edges"][0]:.2e}]<br>Count: {histogram["data"]["bin_count"][0]:.2e}'] + [f'Bin: [{histogram["data"]["bin_edges"][i]:.2e}, {histogram["data"]["bin_edges"][i+1]:.2e}]<br>Count: {histogram["data"]["bin_count"][i]:.2e}' for i in range(len(histogram["data"]["bin_edges"])-1)] + [f'Bin: [{histogram["data"]["bin_edges"][-1]:.2e},∞]<br>Count: {histogram["data"]["bin_count"][-1]:.2e}'],
				hovertemplate = "%{text}",
			)
		)
		self.plotly_figure['data'][-1]['marker']['color'] = rgb2hexastr_color(histogram.get('color'))
		self.plotly_figure['data'][-1]['line']['width'] = 0
		self.plotly_figure.add_traces(
			go.Scatter(
				x = [0],
				y = [float('NaN')],
				name = histogram.get('label'),
				mode = translate_marker_and_linestyle_to_Plotly_mode(histogram.get('marker'), histogram.get('linestyle')),
				marker_symbol = map_marker_to_Plotly_markers(histogram.get('marker')),
				opacity = histogram.get('alpha'),
				showlegend = True if histogram.get('label') != None else False,
				line = dict(
					dash = map_linestyle_to_Plotly_linestyle(histogram.get('linestyle')),
				),
				legendgroup = legendgroup,
			)
		)
		self.plotly_figure['data'][-1]['marker']['color'] = rgb2hexastr_color(histogram.get('color'))
		self.plotly_figure['data'][-1]['line']['width'] = histogram.get('linewidth')
	
	def draw_heatmap(self, heatmap):
		x = heatmap['data']['x']
		y = heatmap['data']['y']
		z = heatmap['data']['z']
		if heatmap.get('zscale') == 'log' and (z<=0).any():
			warnings.warn('Warning: log color scale was selected and there are <z> values <= 0. In the plot you will see them as NaN.')
			with warnings.catch_warnings():
				warnings.filterwarnings("ignore", message="invalid value encountered in log")
				z = np.log(z)
		self.plotly_figure.add_trace(
			go.Heatmap(
				x = x,
				y = y,
				z = z,
				opacity = heatmap.get('alpha'),
				zmin = heatmap.get('zlim')[0] if heatmap.get('zlim') is not None else None,
				zmax = heatmap.get('zlim')[1] if heatmap.get('zlim') is not None else None,
				colorbar = dict(
					title = ('log ' if heatmap.get('zscale') == 'log' else '') + (heatmap.get('zlabel') if heatmap.get('zlabel') is not None else ''),
					titleside = 'right',
				),
				hovertemplate = f'{(self.parent_figure.xlabel if self.parent_figure.xlabel is not None else "x")}: %{{x}}<br>{(self.parent_figure.ylabel if self.parent_figure.ylabel is not None else "y")}: %{{y}}<br>{(heatmap["zlabel"] if heatmap.get("zlabel") is not None else "color scale")}: %{{z}}<extra></extra>', # https://community.plotly.com/t/heatmap-changing-x-y-and-z-label-on-tooltip/23588/6
			)
		)
		self.plotly_figure.update_layout(legend_orientation="h")
	
	def draw_contour(self, contour):
		x = contour['data']['x']
		y = contour['data']['y']
		z = contour['data']['z']
		if contour.get('zscale') == 'log' and (z<=0).any():
			warnings.warn('Warning: log color scale was selected and there are <z> values <= 0. In the plot you will see them as NaN.')
			with warnings.catch_warnings():
				warnings.filterwarnings("ignore", message="invalid value encountered in log")
				z = np.log(z)
		self.plotly_figure.add_trace(
			go.Contour(
				x = x,
				y = y,
				z = z,
				opacity = contour.get('alpha'),
				zmin = contour.get('zlim')[0] if contour.get('zlim') is not None else None,
				zmax = contour.get('zlim')[1] if contour.get('zlim') is not None else None,
				colorbar = dict(
					title = ('log ' if contour.get('zscale') == 'log' else '') + (contour.get('zlabel') if contour.get('zlabel') is not None else ''),
					titleside = 'right',
				),
				hovertemplate = f'{(self.parent_figure.xlabel if self.parent_figure.xlabel is not None else "x")}: %{{x}}<br>{(self.parent_figure.ylabel if self.parent_figure.ylabel is not None else "y")}: %{{y}}<br>{(contour["zlabel"] if contour.get("zlabel") is not None else "color scale")}: %{{z}}<extra></extra>',
				contours=dict(
					coloring = 'heatmap',
					showlabels = True, # show labels on contours
					labelfont = dict( # label font properties
						color = 'black',
					)
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
