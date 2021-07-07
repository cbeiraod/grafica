from unifiedplottinginterface.figure import Figure
import unittest

class TestProperties(unittest.TestCase):
	
	def test_nice_cases(self):
		tests = [
			dict(x = [1,2,3], y = [1,2,3], kwargs = dict()),
			dict(x = [1], y = [1], kwargs = dict()),
			dict(x = [1,2,3], y = [1,2,3], kwargs = dict(color = (0,0,0))),
			dict(x = [1,2,3], y = [1,2,3], kwargs = dict(marker = '.', linestyle = 'solid')),
			dict(x = [1,2,3], y = [1,2,3], kwargs = dict(label = 'My plot', color = (255,0,0), alpha = .5, marker = None)),
		]
		fig = Figure()
		for args in tests:
			with self.subTest(i=args):
				try:
					fig.scatter(args['x'], args['y'], **args['kwargs'])
				except:
					self.fail()
	
	def test_not_matching_xy(self):
		fig = Figure()
		with self.assertRaises(ValueError):
			fig.scatter([1,2,3],[1,2,3,4])
	
	def test_wrong_keyword_arguments(self):
		tests = [
			dict(x = [1,2,3], y = [1,2,3], kwargs = dict(random_argument = 9)), # random_argument
			dict(x = [1,2,3], y = [1,2,3], kwargs = dict(colorr = (0,0,0))), # colorr instead of color
			dict(x = [1,2,3], y = [1,2,3], kwargs = dict(markers = '.', linestyle = 'solid')), # markers instead of marker
			dict(x = [1,2,3], y = [1,2,3], kwargs = dict(legend = 'My plot', color = (255,0,0), alpha = .5, marker = None)), # legend instead of label
		]
		fig = Figure()
		for args in tests:
			with self.subTest(i=args):
				with self.assertRaises(ValueError):
					fig.scatter(args['x'], args['y'], **args['kwargs'])
	
if __name__ == '__main__':
	unittest.main()
