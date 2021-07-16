import unifiedplottinginterface as upi
import numpy as np

x = np.linspace(1,2,9)

fig = upi.PlotlyFigure()
fig.title = 'Test'
fig.xlabel = 'x axis'
fig.yscale = 'log'
fig.scatter(x, x**2, label = 'x²')
fig.histogram(np.random.randn(99))
fig.title = 'Test 2'
# ~ fig.show()
