GENERAL_KWARGS_FOR_PLOTTING_METHODS = {'label','color','marker','linestyle','linewidth'}

def validate_label(label):
	if label is None:
		return None
	if not isinstance(label, str):
		raise TypeError(f'<label> must be a string, received {label} of type {type(label)}.')
	return label

def validate_color(color):
	received_color = color
	try:
		color = tuple(color)
	except:
		raise TypeError(f'<color> must be an iterable of the form (r,g,b) where r,g and b are integer numbers from 0 to 255. Received {color}.')
	if len(color) != 3 or any({not isinstance(i,int) for i in color}) or any({not 0<=i<=255 for i in color}):
		raise ValueError(f'<color> must contain 3 integer numbers ranging from 0 to 255, received {received_color}.')
	return color

VALID_MARKERS = {'.','o','+','x','*', None}
def validate_marker(marker):
	if marker not in VALID_MARKERS:
		raise ValueError(f'<marker> must be one of {VALID_MARKERS}, received {marker}.')
	return marker

VALID_LINESTYLES = {'solid','dotted','dashed', None}
def validate_linestyle(linestyle):
	if linestyle not in VALID_LINESTYLES:
		raise ValueError(f'<linestyle> must be one of {VALID_LINESTYLES}, received {linestyle}.')
	return linestyle

def validate_linewidth(linewidth):
	received_linewidth = linewidth
	try:
		linewidth = float(linewidth)
	except:
		raise TypeError(f'<linewidth> must be a float number, received {received_linewidth} of type {type(received_linewidth)}.')
	if linewidth < 0:
		raise ValueError(f'<linewidth> must be a positive number, received {linewidth}.')
	return linewidth

def validate_kwargs(kwargs2validate, kwargs):
	"""
	kwargs2validate: An iterable with the names of the kwargs that have 
		to be validated from <kwargs>.
	kwargs: A dictionary with the kwargs to validate.
	
	- If an argument is in <kwargs2validate> and it is also in <kwargs> then
	the corresponding validating function (according to the mapping below)
	is called to check whether it is correct. 
	- If an argument in <kwargs2validate> is NOT in <kwargs> then a ValueError
	is raised.
	- Arguments in <kwargs> that are not in <kwargs2validate> are ignored.
	"""
	VALIDATION_FUNCTIONS = {
		'label': validate_label,
		'color': validate_color,
		'marker': validate_marker,
		'linestyle': validate_linestyle,
		'linewidth': validate_linewidth,
	}
	for arg in kwargs2validate:
		if arg not in kwargs:
			raise ValueError(f'<{arg}> is not among the kwargs.')
		kwargs[arg] = VALIDATION_FUNCTIONS[arg](kwargs[arg])
	return kwargs
