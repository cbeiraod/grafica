from grafica.validation import *
import unittest

class TestProperties(unittest.TestCase):
	
	def test_validate_label(self):
		for label in ['Gráfico','This is a long label because sometimes labels are long', None]:
			with self.subTest(i=label):
				self.assertEqual(validate_label(label), label)
		
		with self.assertRaises(TypeError):
			validate_label(9)
	
	def test_validate_color(self):
		for color in [(0,0,0),(1,2,3),(255,255,255),[1,2,3]]:
			with self.subTest(i=color):
				self.assertEqual(validate_color(color),tuple([rgb/255 for rgb in color]))
		for color in [(-1,1,1),(444,0,0),'#fcba03',(1,2,3,4)]:
			with self.subTest(i=color):
				with self.assertRaises(ValueError):
					validate_color(color)
	
	def test_validate_marker(self):
		for marker in VALID_MARKERS:
			with self.subTest(i=marker):
				self.assertEqual(validate_marker(marker),marker)
		for marker in {',','dot','cross'}:
			with self.subTest(i=marker):
				with self.assertRaises(ValueError):
					validate_marker(marker)
	
	def test_validate_linestyle(self):
		for linestyle in VALID_LINESTYLES:
			with self.subTest(i=linestyle):
				self.assertEqual(validate_linestyle(linestyle),linestyle)
		for linestyle in {',','dot','cross'}:
			with self.subTest(i=linestyle):
				with self.assertRaises(ValueError):
					validate_linestyle(linestyle)
	
	def test_validate_linewidth(self):
		for linewidth in [1,1.5,'1.5']:
			with self.subTest(i=linewidth):
				self.assertEqual(validate_linewidth(linewidth), float(linewidth))
		for linewidth in {',','dot','cross'}:
			with self.subTest(i=linewidth):
				with self.assertRaises(TypeError):
					validate_linewidth(linewidth)
		for linewidth in {'-2',-1,-1.5}:
			with self.subTest(i=linewidth):
				with self.assertRaises(ValueError):
					validate_linewidth(linewidth)
	
	def test_validate_alpha(self):
		for alpha in [0,1,0.5]:
			with self.subTest(i=alpha):
				self.assertEqual(validate_alpha(alpha), float(alpha))
		for alpha in {',','dot','cross'}:
			with self.subTest(i=alpha):
				with self.assertRaises(TypeError):
					validate_alpha(alpha)
		for alpha in {'-2',-1,-1.5,2}:
			with self.subTest(i=alpha):
				with self.assertRaises(ValueError):
					validate_alpha(alpha)
	
	def test_validate_kwargs(self):
		no_error_cases = [
			{'kwargs2validate': {'linestyle','linewidth'}, 'kwargs': {'linestyle': 'solid', 'linewidth': 2}},
			{'kwargs2validate': {'linestyle','marker','color','label'}, 'kwargs': {'linestyle': 'dashed', 'marker': '.', 'color': (255,0,0), 'label': 'My plot'}},
			{'kwargs2validate': {'color','label','linestyle','marker'}, 'kwargs': {'linestyle': 'dashed', 'marker': '.', 'color': (255,0,0), 'label': 'My plot'}},
			{'kwargs2validate': {'linestyle','linewidth', 'marker'}, 'kwargs': {'linestyle': 'solid', 'linewidth': 2}},
			{'kwargs2validate': {'linestyle','linewidth'}, 'kwargs': {}},
		]
		for no_error_case in no_error_cases:
			with self.subTest(i=no_error_case):
				self.assertTrue(validate_kwargs(**no_error_case) is not None)
		error_cases = [
			{'kwargs2validate': {'linestyle','linewidth'}, 'kwargs': {'linestyle': 'solid', 'linewidth': -2}}, # linewidth < 0
			{'kwargs2validate': {'linestyle','linewidth'}, 'kwargs': {'linestyle': '--', 'linewidth': 2}}, # invalid linestyle
			{'kwargs2validate': {'linestyle','linewidth'}, 'kwargs': {'linestylesssss': 'solid'}}, # linestylesssss not in kwargs2validate
		]
		for error_case in error_cases:
			with self.subTest(i=error_case):
				try:
					validate_kwargs(**error_case)
				except (ValueError, TypeError):
					pass
				else:
					self.fail()
	
if __name__ == '__main__':
	unittest.main()
