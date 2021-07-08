import unifiedplottinginterface as upi
import numpy as np

# ~ samples = [item for sublist in [[i+.6]*i for i in [1,2,3,4,5]] for item in sublist]
samples = np.random.randn(999)
fig = upi.manager.new(
	title = 'Histogram',
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

for plotter in upi.manager.plotters:
	upi.manager.draw(plotter=plotter)
upi.manager.save(mkdir=True)
