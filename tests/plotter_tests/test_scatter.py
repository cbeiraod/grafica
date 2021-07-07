import unifiedplottinginterface as upi
import numpy as np

x = np.linspace(1,2,9)
fig = upi.manager.new(
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

for plotter in ['plotly', 'matplotlib']:
	upi.manager.draw(plotter=plotter)

upi.manager.save(mkdir=True)
