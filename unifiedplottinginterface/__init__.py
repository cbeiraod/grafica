from .figure import Figure

class FigureManager:
	def __init__(self):
		self.default_plotting_package = 'plotly'
		self.figures = []
	
	@property
	def default_plotting_package(self):
		return self._default_plotting_package
	@default_plotting_package.setter
	def default_plotting_package(self, pkg):
		IMPLEMENTED_PACKAGES = {'plotly'}
		if pkg not in IMPLEMENTED_PACKAGES:
			raise ValueError(f'<pkg> must be one of the implemented packaged which are {IMPLEMENTED_PACKAGES}.')
		self._default_plotting_package = pkg
	
	def new(self, **kwargs):
		fig = Figure()
		self.figures.append(fig)
		fig.set(**kwargs)
		return fig

manager = FigureManager()
