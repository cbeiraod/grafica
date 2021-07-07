import unifiedplottinginterface as upi
import numpy as np

figure_properties = [
	dict(), # Completely blank figure
	dict(title = 'Figure with title'),
	dict(title = 'Figure with all', subtitle = 'Subtitle', xlabel = 'x axis', ylabel = 'y axis', yscale = 'log'),
	dict(title = 'Hidden title', subtitle = 'Subtitle', xlabel = 'x axis', ylabel = 'y axis', xscale = 'log', yscale = 'log', show_title = False),
]

x = np.linspace(-1,1)
for idx,props in enumerate(figure_properties):
	fig = upi.manager.new(**props)
	fig.scatter(
		x = x,
		y = x**2,
		label = 'x²',
	)
	fig.scatter(
		x = x,
		y = x**3,
		label = 'x³',
		marker = '.',
	)
	fig.scatter(
		x = x,
		y = np.sin(x),
		label = 'sin(x)',
		linestyle = 'dashed',
	)
	fig.scatter(
		x = x,
		y = np.exp(x),
		label = 'exp(x)',
		linestyle = 'dotted',
		marker = '*',
	)

for plotter in ['plotly', 'matplotlib']:
	upi.manager.draw(plotter=plotter)

upi.manager.save(mkdir=True)
