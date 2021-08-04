from .FigureManager import FigureManager

manager = FigureManager()

def new(*args, **kwargs):
	"""A shorthand wrapper around grafica.manager.new"""
	return manager.new(*args, **kwargs)

def save_unsaved(*args, **kwargs):
	"""A shorthand wrapper around grafica.manager.save_unsaved"""
	return manager.save_unsaved(*args, **kwargs)
