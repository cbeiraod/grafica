import unifiedplottinginterface as upi
from unifiedplottinginterface.plotter import PlotlyPlotter
import numpy as np

figure_properties = [
	dict(), # Completely blank figure
	dict(title = 'Figure with title'),
	dict(title = 'Figure with all', subtitle = 'Subtitle', xlabel = 'x axis', ylabel = 'y axis', xscale = 'log', yscale = 'log'),
	dict(title = 'Hidden title', subtitle = 'Subtitle', xlabel = 'x axis', ylabel = 'y axis', xscale = 'log', yscale = 'log', show_title = False),
]

for idx,props in enumerate(figure_properties):
	fig = upi.manager.new(**props)
	plotly_figure = PlotlyPlotter(fig)
	plotly_figure.save(f'{idx+1}')

fig = upi.manager.new(
	title = 'Figure with some traces',
	subtitle = 'This is the first figure with traces',
	xlabel = 'x',
	ylabel = 'y',
)
x = np.linspace(-1,1)
fig.scatter(
	x, 
	x**2, 
	label = 'x^2'
)
fig.scatter(
	x,
	x**3,
	marker = '.',
	label = 'x^3',
)
PlotlyPlotter(fig).show()
