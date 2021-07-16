from unifiedplottinginterface.FigureManager import FigureManager
import numpy as np

FM = FigureManager()

samples = np.random.randn(999)

for plotter in FM.plotters:
	fig = FM.new(
		title = 'Histogram',
		subtitle = 'All the traces use the exact same data',
		plotter_name = plotter,
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

FM.save(mkdir=True)
