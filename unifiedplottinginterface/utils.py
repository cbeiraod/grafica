def validate_label(label):
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
