import unifiedplottinginterface as upi
import numpy as np

x = np.linspace(-1,1)
fig = upi.manager.new(
	title = 'Test markers',
)
for idx,marker in enumerate({'.','o','+','x','*', None}):
	fig.scatter(
		x = x,
		y = (idx+1)*x,
		label = f'marker={marker}',
		marker = marker,
	)

for plotter in ['plotly', 'matplotlib']:
	upi.manager.draw(plotter=plotter)

upi.manager.save(mkdir=True)
