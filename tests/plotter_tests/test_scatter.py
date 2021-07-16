from unifiedplottinginterface.FigureManager import FigureManager
import numpy as np

x = np.linspace(1,2,9)

FM = FigureManager()
fig = FM.new(
	title = 'Markers and linestyles',
	yscale = 'log',
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

fig = FM.new(
	title = 'Colors',
)
for idx,color in enumerate({(0,0,0),(1,0,0),(255,0,0)}):
	fig.scatter(
		x,
		x*0 + idx,
		color = color,
		label = f'color={color}',
		marker = '.',
	)

fig = FM.new(
	title = 'Alpha',
	aspect = 'equal',
)
fig.scatter(
	np.random.randn(999),
	np.random.randn(999),
	alpha = .5,
	linestyle = 'none',
	marker = '.',
)

fig = FM.new(
	title = 'Linewidth',
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

FM.save(mkdir=True)
