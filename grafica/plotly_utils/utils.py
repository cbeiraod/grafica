import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

PLOTLY_SYMBOLS = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'triangle-down', 'triangle-left', 'triangle-right', 'triangle-ne', 'triangle-se', 'triangle-sw', 'triangle-nw', 'pentagon', 'hexagon', 'hexagon2', 'octagon', 'star', 'hexagram', 'star-triangle-up', 'star-triangle-down', 'star-square', 'star-diamond', 'diamond-tall', 'diamond-wide', 'hourglass', 'bowtie', 'circle-cross', 'circle-x', 'square-cross', 'square-x', 'diamond-cross', 'diamond-x', 'cross-thin', 'x-thin', 'asterisk', 'hash', 'y-up', 'y-down', 'y-left', 'y-right', 'line-ew', 'line-ns', 'line-ne', 'line-nw', 'arrow-up', 'arrow-down', 'arrow-left', 'arrow-right', 'arrow-bar-up', 'arrow-bar-down', 'arrow-bar-left', 'arrow-bar-right']

def line(error_y_mode=None, **kwargs):
	"""Extension of `plotly.express.line` to use error bands."""
	ERROR_MODES = {'bar','band','bars','bands',None}
	if error_y_mode not in ERROR_MODES:
		raise ValueError(f"'error_y_mode' must be one of {ERROR_MODES}, received {repr(error_y_mode)}.")
	if 'symbol_sequence' not in kwargs:
		kwargs['symbol_sequence'] = PLOTLY_SYMBOLS # See https://community.plotly.com/t/plotly-express-is-repeating-symbols/57928
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
	fig.update_traces(marker_size=11) # Increase the default size of markers to my taste.
	return fig
