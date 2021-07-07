from .figure import Figure
from .PlotlyPlotter import PlotlyPlotter
from .plotter import Plotter

class _FigureManager:
	def __init__(self):
		self.figures = [] # Figures of class "from .figure import Figure" are stored here.
		self.plots = [] # Drawn plots are stored here, i.e. Plotter objects.
		self.plotters = {} # Plotters (e.g. PlotlyPlotter) are stored here.
		self.add_plotter(plotter = PlotlyPlotter, name = 'plotly')
		self.default_plotter = 'plotly'
	
	@property
	def default_plotter(self):
		return self._default_plotter
	@default_plotter.setter
	def default_plotter(self, plotter_name):
		if plotter_name not in self.plotters:
			raise ValueError(f'<plotter_name> must be one of {set(self.plotters.keys())}.')
		self._default_plotter = plotter_name
	
	def new(self, **kwargs):
		fig = Figure()
		self.figures.append(fig)
		fig.set(**kwargs)
		return fig
	
	def add_plotter(self, plotter, name):
		if not issubclass(plotter, Plotter):
			raise TypeError(f'<plotter> must be a subclass of Plotter. Received {plotter}.')
		if not isinstance(name, str):
			raise TypeError(f'<name> must be a string, received {name} of type {type(name)}.')
		self.plotters[name] = plotter
	
	def draw(self):
		for figure in self.figures:
			plotted_figure = self.plotters[self.default_plotter](figure)
			self.plots.append(plotted_figure)

manager = _FigureManager()
