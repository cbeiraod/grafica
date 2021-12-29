import grafica
import numpy as np

samples = np.random.randn(999)

for plotter in grafica.manager.plotters:
	for density in {True, False}:
		fig = grafica.manager.new(
			title = f'Histogram density {density}',
			subtitle = 'All the traces use the exact same data',
			plotter_name = plotter,
		)
		fig.histogram(
			samples,
			label = 'No args',
			density = density,
		)
		bins = 5
		fig.histogram(
			samples,
			bins = bins,
			label = f'bins = {bins}',
			density = density,
		)
		bins = [-1,-.1,.1,1,2]
		fig.histogram(
			samples,
			bins = bins,
			label = f'bins = {bins}',
			marker = '*',
			density = density,
		)
		bins = 6
		fig.histogram(
			samples,
			marker = '.',
			label = f'bins={bins}',
			bins = bins,
			density = density,
		)

samples = [0,1,1,2,3,3,3]
for plotter in grafica.manager.plotters:
	for density in {True, False}:
		fig = grafica.manager.new(
			title = f'Checking boundaries in bins density {density}',
			subtitle = f'Samples = {samples}',
			plotter_name = plotter,
		)
		fig.histogram(
			samples,
			label = 'No args',
			density = density,
		)
		for bins in [[0,1,2,3], [1,2], [-1,0,1,2,3,4]]:
			fig.histogram(
				samples,
				bins = bins,
				label = f'bins = {bins}',
				density = density,
			)

grafica.save_unsaved(mkdir=True)
