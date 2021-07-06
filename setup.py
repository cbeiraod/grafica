import setuptools


setuptools.setup(
	name="unifiedplottinginterface",
	version="0.0.0",
	author="Matias H. Senger",
	author_email="m.senger@hotmail.com",
	description="A unified plotting interface to make plots with any package",
	# ~ url="https://github.com/SengerM/myplotlib",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	package_data = {
		'': ['rc_styles/*']
	}
)
