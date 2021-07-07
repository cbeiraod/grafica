from .figure import Figure
import plotly.graph_objects as go
import plotly

class Plotter:
	"""This is a template class to inherit from when creating a specific
	plotter for some package, e.g. PlotlyPlotter should receive an instance
	of Figure and create the corresponding plot using Plotly."""
	
	def __init__(self, figure):
		if not isinstance(figure, Figure):
			raise TypeError(f'<figure> must be an instance of {type(Figure())}, received {type(figure)}.')
		self.parent_figure = figure
	
	def show(self):
		"""Must override this method when inheriting."""
		raise NotImplementedError(f'Not implemented yet for the plotting package you are using! (Specifically for the class {self.__class__.__name__}.)')
	
	def save(self, file_name=None, **kwargs):
		"""Must override this method when inheriting."""
		raise NotImplementedError(f'Not implemented yet for the plotting package you are using! (Specifically for the class {self.__class__.__name__}.)')
	
	def draw_figure(self):
		"""Must override this method when inheriting. This method should
		draw all elements of the figure such as the title, axes labels, etc."""
		raise NotImplementedError(f'Not implemented yet for the plotting package you are using! (Specifically for the class {self.__class__.__name__}.)')
	
	def draw_traces(self):
		"""Must override this method when inheriting. This method should 
		draw all the traces, e.g. scatter plots, histograms, etc."""
		raise NotImplementedError(f'Not implemented yet for the plotting package you are using! (Specifically for the class {self.__class__.__name__}.)')

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
		
def translate_marker_and_linestyle_to_Plotly_mode(marker, linestyle):
	"""<marker> and <linestyle> are each one and only one of the valid
	options for each object."""
	if marker is None and linestyle is not None:
		mode = 'lines'
	elif marker is not None and linestyle is not None:
		mode = 'lines+markers'
	elif marker is not None and linestyle is None:
		mode = 'markers'
	else:
		mode = 'lines'
	return mode

def map_marker_to_Plotly_markers(marker):
	if marker is None:
		return None
	markers_map = {
		'.': 'circle',
		'+': 'cross',
		'x': 'x',
		'o': 'circle-open',
		'*': 'asterisk',
	}
	return markers_map[marker]

def map_linestyle_to_Plotly_linestyle(linestyle):
	linestyle_map = {
		'solid': None,
		None: None,
		'dashed': 'dash',
		'dotted':  'dot',
	}
	return linestyle_map[linestyle]

def rgb2hexastr_color(rgb_color: tuple):
	# Assuming that <rgb_color> is a (r,g,b) tuple.
	color_str = '#'
	for rgb in rgb_color:
		color_hex_code = hex(rgb)[2:]
		if len(color_hex_code) < 2:
			color_hex_code = f'0{color_hex_code}'
		color_str += color_hex_code
	return color_str
