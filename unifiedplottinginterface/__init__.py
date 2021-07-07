from .figure import Figure
from .PlotlyPlotter import PlotlyPlotter
from .MatplotlibPlotter import MatplotlibPlotter
from .plotter import Plotter
import __main__
from pathlib import Path

class _FigureManager:
	def __init__(self):
		self.figures = [] # Figures of class "from .figure import Figure" are stored here.
		self.plots = [] # Drawn plots are stored here, i.e. Plotter objects.
		self.plotters = {} # Plotters (e.g. PlotlyPlotter) are stored here.
		BUILT_IN_PLOTTERS = {
			'plotly': PlotlyPlotter,
			'matplotlib': MatplotlibPlotter,
		}
		for name, plotter in BUILT_IN_PLOTTERS.items():
			self.add_plotter(plotter = plotter, name = name)
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
	
	def draw(self, plotter=None):
		if plotter is None:
			plotter = self.default_plotter
		else:
			if plotter not in self.plotters:
				raise ValueError(f'<plotter> must be one of {set(self.plotters.keys())}.')
		for figure in self.figures:
			plotted_figure = self.plotters[plotter](figure)
			self.plots.append(plotted_figure)
	
	def show(self):
		for plot in self.plots:
			plot.show()
	
	def save(self, mkdir=False):
		if mkdir == False: # Save the plots in the current working directory.
			directory = './'
		else:
			if mkdir == True: # I create a directory automatically with the name of the script, in the same place as the script.
				directory = __main__.__file__.replace('.py', '') + '_plots/'
			else: # I assume mkdir is a path to a directory where to save the plots.
				directory = str(mkdir)
			Path(directory).mkdir(parents=True, exist_ok=True)
		for idx,plot in enumerate(self.plots):
			file_name = plot.parent_figure.title if plot.parent_figure.title is not None else f'figure_{idx+1}'
			plot.save(file_name = str(Path(directory)/Path(file_name)))

manager = _FigureManager()
