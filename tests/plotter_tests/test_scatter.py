import grafica
import numpy as np

x = np.linspace(1,2,9)

for plotter in grafica.manager.plotters:
	fig = grafica.manager.new(
		title = 'Markers and linestyles',
		yscale = 'log',
		plotter_name = plotter,
	)
	for idx_marker,marker in enumerate({'.','o','+','x','*', None}):
		for idx_linestyle,linestyle in enumerate({'solid','dotted','dashed', 'none', None}):
			fig.scatter(
				x = x,
				y = (idx_marker+1)*x**idx_linestyle,
				label = f'{linestyle}-{marker}',
				marker = marker,
				linestyle = linestyle,
			)

	fig = grafica.manager.new(
		title = 'Colors',
		plotter_name = plotter,
	)
	for idx,color in enumerate({(0,0,0),(1,0,0),(255,0,0)}):
		fig.scatter(
			x,
			x*0 + idx,
			color = color,
			label = f'color={color}',
			marker = '.',
		)

	fig = grafica.manager.new(
		title = 'Alpha',
		aspect = 'equal',
		plotter_name = plotter,
	)
	fig.scatter(
		np.random.randn(999),
		np.random.randn(999),
		alpha = .5,
		linestyle = 'none',
		marker = '.',
	)

	fig = grafica.manager.new(
		title = 'Linewidth',
		plotter_name = plotter,
	)
	for idx,linewidth in enumerate([.5,1,3,6,None]):
		if linewidth is not None:
			fig.scatter(
				x,
				x**2 + idx,
				linewidth = linewidth,
				label = f'linewidth={linewidth}',
				color = (0,0,0),
			)
		else:
			fig.scatter(
				x,
				x**2 + idx,
				label = f'Default linewidth',
				color = (0,0,1),
			)

grafica.save_unsaved(mkdir=True)
