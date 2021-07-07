from unifiedplottinginterface.figure import Figure
import unittest

class TestProperties(unittest.TestCase):
	
	def test_title(self):
		fig = Figure()
		self.assertEqual(fig.title, None)
		title = 'Hola, cómo te va?'
		fig.title = title
		self.assertEqual(fig.title, title)
	
	def test_show_title(self):
		fig = Figure()
		for show in {True,False}:
			fig.show_title = show
			self.assertEqual(fig.show_title, show)
		with self.assertRaises(TypeError):
			fig.show_title = 'false'
	
	def test_subtitle(self):
		fig = Figure()
		self.assertEqual(fig.subtitle, None)
		subtitle = 'Todo bien, acá andamos. Vos?'
		fig.subtitle = subtitle
		self.assertEqual(fig.subtitle, subtitle)
	
	def test_xlabel(self):
		fig = Figure()
		self.assertEqual(fig.xlabel, None)
		xlabel = 'Eje x'
		fig.xlabel = xlabel
		self.assertEqual(fig.xlabel, xlabel)
	
	def test_ylabel(self):
		fig = Figure()
		self.assertEqual(fig.ylabel, None)
		ylabel = 'Eje y'
		fig.ylabel = ylabel
		self.assertEqual(fig.ylabel, ylabel)
	
	def test_xscale(self):
		fig = Figure()
		self.assertEqual(fig.xscale, None)
		for scale in {'lin','log'}:
			fig.xscale = scale
			self.assertEqual(fig.xscale, scale)
		with self.assertRaises(ValueError):
			fig.xscale = 'linear'
		
	def test_yscale(self):
		fig = Figure()
		self.assertEqual(fig.yscale, None)
		for scale in {'lin','log'}:
			fig.yscale = scale
			self.assertEqual(fig.yscale, scale)
		with self.assertRaises(ValueError):
			fig.yscale = 'linear'
	
	def test_aspect(self):
		fig = Figure()
		self.assertEqual(fig.aspect, None)
		fig.aspect = 'equal'
		self.assertEqual(fig.aspect, 'equal')
		with self.assertRaises(ValueError):
			fig.aspect = 'other'
		fig.aspect = None
		self.assertEqual(fig.aspect, None)
	
	def test_set(self):
		fig = Figure()
		
		nice_cases = [
			dict(title = 'Título', subtitle = 'Subtítulo'),
			dict(xlabel = 'Eje x', ylabel = 'Eje y'),
		]
		for kwargs in nice_cases:
			with self.subTest(i=kwargs):
				try:
					fig.set(**kwargs)
				except:
					self.fail()
				for arg,value in kwargs.items():
					with self.subTest(i=arg):
						self.assertEqual(getattr(fig,arg),value)
		
		bad_cases = [
			dict(Title = 'Título'), # Title instead of title
			dict(x_label = 'x'), # x_label instead of xlabel
		]
		for kwargs in bad_cases:
			with self.subTest(i=kwargs):
				try:
					fig.set(**kwargs)
				except ValueError:
					pass
				else:
					self.fail()
	
if __name__ == '__main__':
	unittest.main()
