class Charm:

	def __init__(self, input_file, plot_types=("pdf", "cdf", "ccdf")):
		self.input_file = input_file
		self.plot_types = list(plot_types)

	def read(self):
		from pandas import read_csv
		input_data = read_csv(self.input_file, header=None, sep="\t")

		return input_data

	def on_data(self):
		return self.read()[0]

	def draw_plots(self):
		from matplotlib import pyplot as plt

		fig = plt.figure(figsize=(4, 4))
		ax = fig.add_subplot(111)
		data = self.on_data()
		from powerlaw import Fit
		experimental = Fit(data, xmin=min(data))
		experimental.plot_ccdf(ax=ax)

		plt.show()


o = Charm("./1.txt")
print(o.draw_plots())
