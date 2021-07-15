import unifiedplottinginterface as upi
import numpy as np

samples = np.random.randn(999)
fig = upi.manager.new(
	title = 'Histogram',
	subtitle = 'All the traces use the exact same data',
)
fig.histogram(
	samples,
	label = 'No args',
)
bins = 5
fig.histogram(
	samples,
	bins = bins,
	label = f'bins = {bins}',
)
bins = [-1,-.1,.1,1,2]
fig.histogram(
	samples,
	bins = bins,
	label = f'bins = {bins}',
	marker = '*',
)
bins = 6
fig.histogram(
	samples,
	marker = '.',
	label = f'bins={bins}',
	bins = bins,
)

for plotter in {'plotly'}:# upi.manager.plotters:
	upi.manager.draw(plotter=plotter)
upi.manager.save(mkdir=True)
