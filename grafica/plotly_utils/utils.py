import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import numpy as np

# Create my own template and set it as default -------------------------
MARKERS = ['circle', 'cross', 'x', 'triangle-up', 'star', 'hexagram', 'square', 'diamond', 'hourglass', 'bowtie', 'pentagon', 'triangle-down', 'triangle-left', 'triangle-right', 'star-triangle-up', 'star-triangle-down', 'star-square', 'star-diamond', 'diamond-tall', 'diamond-wide', 'triangle-ne', 'triangle-se', 'triangle-sw', 'triangle-nw',  'hexagon', 'hexagon2', 'octagon']
my_template = pio.templates['plotly']
my_template.data.scatter = [
    go.Scatter(marker=dict(symbol=s, size=12)) for s in MARKERS
]

pio.templates['my_template'] = my_template
pio.templates.default = 'my_template'

# ----------------------------------------------------------------------

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
			line_width = 0 if 'symbol' in param['px'] else None,
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
	
	return fig
