# Unified Plotting Interface

My personal unified interface for doing plots. The idea is to wrap any plotting package (Matplotlib, Plotly, etc.) with a simple and single interface, at least for "basic everyday" plots.

### Maxims

The maxims to guide the development of this package are:

- The interface tries to capture the "concept" of each kind of plot rather than its drawing details.
- The interface is simple and easy without complicated details.
- The user must be able to easily access any property of the figure and/or any trace it contains.

This is an evolution of [myplotlib](https://github.com/SengerM/myplotlib).

## Illustrative example

The example below illustrates the philosophy of the Unified Plotting Interface package:
```Python
import unifiedplottinginterface as upi
import numpy

x = numpy.linspace(0,1)

for package in {'plotly','matplotlib'}:
	figure = upi.manager.new(
		plotter_name=package, # Just tell me which package you want to use, I'll take care of the rest.
	)
	figure.scatter(x, x**2) # Draw a scatter plot.

upi.manager.show()
```
