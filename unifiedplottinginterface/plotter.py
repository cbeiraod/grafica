from .figure import Figure

class Plotter:
	"""This is a template class to inherit from when creating a specific
	plotter for some package, e.g. PlotlyPlotter should receive an instance
	of Figure and create the corresponding plot using Plotly."""
	
	def __init__(self, figure):
		if not isinstance(figure, Figure):
			raise TypeError(f'<figure> must be an instance of {type(Figure())}, received {type(figure)}.')
		self.parent_figure = figure
	
	def show(self):
		"""Must override this method when inheriting."""
		raise NotImplementedError(f'Not implemented yet for the plotting package you are using! (Specifically for the class {self.__class__.__name__}.)')
	
	def save(self, file_name=None, **kwargs):
		"""Must override this method when inheriting."""
		raise NotImplementedError(f'Not implemented yet for the plotting package you are using! (Specifically for the class {self.__class__.__name__}.)')
	
	def draw_figure(self):
		"""Must override this method when inheriting. This method should
		draw all elements of the figure such as the title, axes labels, etc."""
		raise NotImplementedError(f'Not implemented yet for the plotting package you are using! (Specifically for the class {self.__class__.__name__}.)')
	
	def draw_traces(self):
		"""Must override this method when inheriting. This method should 
		draw all the traces, e.g. scatter plots, histograms, etc."""
		raise NotImplementedError(f'Not implemented yet for the plotting package you are using! (Specifically for the class {self.__class__.__name__}.)')

