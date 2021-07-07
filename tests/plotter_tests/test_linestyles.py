import unifiedplottinginterface as upi
import numpy as np

x = np.linspace(-1,1,5)
fig = upi.manager.new(
	title = 'Test markers',
)
for idx,linestyle in enumerate({'solid','dotted','dashed', 'none', None}):
	fig.scatter(
		x = x,
		y = (idx+1)*x,
		label = f'linestyle={linestyle}',
		linestyle = linestyle,
		marker = '.',
	)

for plotter in ['plotly', 'matplotlib']:
	upi.manager.draw(plotter=plotter)

upi.manager.save(mkdir=True)
