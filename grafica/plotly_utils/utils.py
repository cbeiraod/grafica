import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from .colors import MyColors2021
import numpy as np

PLOTLY_SYMBOLS = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'triangle-down', 'triangle-left', 'triangle-right', 'triangle-ne', 'triangle-se', 'triangle-sw', 'triangle-nw', 'pentagon', 'hexagon', 'hexagon2', 'octagon', 'star', 'hexagram', 'star-triangle-up', 'star-triangle-down', 'star-square', 'star-diamond', 'diamond-tall', 'diamond-wide', 'hourglass', 'bowtie', 'circle-cross', 'circle-x', 'square-cross', 'square-x', 'diamond-cross', 'diamond-x', 'cross-thin', 'x-thin', 'asterisk', 'hash', 'y-up', 'y-down', 'y-left', 'y-right', 'line-ew', 'line-ns', 'line-ne', 'line-nw', 'arrow-up', 'arrow-down', 'arrow-left', 'arrow-right', 'arrow-bar-up', 'arrow-bar-down', 'arrow-bar-left', 'arrow-bar-right']

def add_grouped_legend(fig, data_frame, graph_dimensions):
def add_grouped_legend(fig, data_frame, x, graph_dimensions):
	"""Create a grouped legend based on the example here https://stackoverflow.com/a/69829305/8849755
	- fig: The figure in which to add such grouped legend.
	- data_frame: The data frame from which to create the legend, in principle it should be the same that was plotted in `fig`.
	- graph_dimensions: A dictionary with the arguments such as `color`, `symbol`, `line_dash` passed to plotly.express functions you want to group, with the names of the columns in the data_frame."""
	param_list = [{'px': {dimension: dimension_value}, 'lg': {'legendgrouptitle_text': dimension_value}} for dimension, dimension_value in graph_dimensions.items()]
	legend_traces = []
	for param in param_list:
		this_dimension_trace = px.line(
			data_frame,
			x = x,
			y = np.full(len(data_frame), float('NaN')),
			**param["px"],
		).update_traces(
			**param["lg"],
			legendgroup = str(param["px"]),
		)
		if 'color' not in param['px']:
			this_dimension_trace.update_traces(
				marker = {'color': '#000000'},
				line = {'color': '#000000'},
			)
		legend_traces.append(this_dimension_trace)
	for t in legend_traces:
		fig.add_traces(t.data)

def line(error_y_mode=None, grouped_legend=False, **kwargs):
	"""Extension of `plotly.express.line` to use error bands."""
	ERROR_MODES = {'bar','band','bars','bands',None}
	if error_y_mode not in ERROR_MODES:
		raise ValueError(f"'error_y_mode' must be one of {ERROR_MODES}, received {repr(error_y_mode)}.")
	if 'symbol_sequence' not in kwargs:
		kwargs['symbol_sequence'] = PLOTLY_SYMBOLS # See https://community.plotly.com/t/plotly-express-is-repeating-symbols/57928
	if 'color_discrete_sequence' not in kwargs:
		kwargs['color_discrete_sequence'] = MyColors2021
	if error_y_mode in {'bar','bars',None}:
		fig = px.line(**kwargs)
	elif error_y_mode in {'band','bands'}:
		if 'error_y' not in kwargs:
			raise ValueError(f"If you provide argument 'error_y_mode' you must also provide 'error_y'.")
		figure_with_error_bars = px.line(**kwargs)
		fig = px.line(**{arg: val for arg,val in kwargs.items() if arg != 'error_y'})
		for data in figure_with_error_bars.data:
			x = list(data['x'])
			y_upper = list(data['y'] + data['error_y']['array'])
			y_lower = list(data['y'] - data['error_y']['array'] if data['error_y']['arrayminus'] is None else data['y'] - data['error_y']['arrayminus'])
			color = f"rgba({tuple(int(data['line']['color'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))},.3)".replace('((','(').replace('),',',').replace(' ','')
			fig.add_trace(
				go.Scatter(
					x = x+x[::-1],
					y = y_upper+y_lower[::-1],
					fill = 'toself',
					fillcolor = color,
					line = dict(
						color = 'rgba(255,255,255,0)'
					),
					hoverinfo = "skip",
					showlegend = False,
					legendgroup = data['legendgroup'],
					xaxis = data['xaxis'],
					yaxis = data['yaxis'],
				)
			)
		# Reorder data as said here: https://stackoverflow.com/a/66854398/8849755
		reordered_data = []
		for i in range(int(len(fig.data)/2)):
			reordered_data.append(fig.data[i+int(len(fig.data)/2)])
			reordered_data.append(fig.data[i])
		fig.data = tuple(reordered_data)
	
	if grouped_legend == True:
		add_grouped_legend(
			fig = fig,
			data_frame = kwargs['data_frame'],
			x = kwargs.get('x'),
			graph_dimensions = {param: kwargs[param] for param in {'color','symbol','line_dash'} if param in kwargs},
		)
	
	fig.update_traces(marker_size=11) # Increase the default size of markers to my taste.
	return fig
