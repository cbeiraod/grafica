import grafica
import numpy as np

x = np.linspace(0,np.pi,99)
y = np.linspace(0,2*np.pi,77)

xx, yy = np.meshgrid(x,y)
zz = np.sin(yy)*np.exp(xx)

for plotter in grafica.manager.plotters:
	fig = grafica.manager.new(
		title = 'Basic contour plot',
		xlabel = 'x',
		ylabel = 'y',
		plotter_name = plotter,
	)
	fig.contour(
		x = x,
		y = y,
		z = zz,
	)

	fig = grafica.manager.new(
		title = 'Heatmap plot with zlabel and 25 contours',
		xlabel = 'x',
		ylabel = 'y',
		plotter_name = plotter,
	)
	fig.contour(
		x = x,
		y = y,
		z = zz,
		zlabel = 'Temperature (°C)',
		contours = 25,
	)

	fig = grafica.manager.new(
		title = 'Heatmap plot with logarithmic scale',
		xlabel = 'x',
		ylabel = 'y',
		plotter_name = plotter,
	)
	fig.contour(
		x = x,
		y = y,
		z = zz-.5,
		zlabel = 'Temperature (°C)',
		zscale = 'log',
	)

	fig = grafica.manager.new(
		title = 'Heatmap plot with zlim',
		xlabel = 'x',
		ylabel = 'y',
		plotter_name = plotter,
	)
	fig.contour(
		x = x,
		y = y,
		z = zz,
		zlim = (.5,1.5),
	)
grafica.save_unsaved(mkdir=True)
