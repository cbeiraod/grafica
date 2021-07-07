import unifiedplottinginterface as upi
import numpy as np

figure_properties = [
	dict(), # Completely blank figure
	dict(title = 'Figure with title'),
	dict(title = 'Figure with all', subtitle = 'Subtitle', xlabel = 'x axis', ylabel = 'y axis', xscale = 'log', yscale = 'log'),
	dict(title = 'Hidden title', subtitle = 'Subtitle', xlabel = 'x axis', ylabel = 'y axis', xscale = 'log', yscale = 'log', show_title = False),
]

for idx,props in enumerate(figure_properties):
	fig = upi.manager.new(**props)

for plotter in ['plotly', 'matplotlib']:
	upi.manager.draw(plotter=plotter)

upi.manager.save(mkdir=True)
