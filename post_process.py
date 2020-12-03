import os
import csv
import pylab
from scipy import interpolate

# Set chemckin output file
output_dir = '/Users/roncha/Master Degree/AC-298/Exercicio_GNV'
prefix = 'CKSoln_'
suffix = '_PSRC1_solution_vs_parameter.csv'
output_file_name = 'Projeto1_1'
path = os.path.join(output_dir, prefix + output_file_name + suffix)
plot_path = '/Users/roncha/Master Degree/AC-298/Project1/plots'


def extract_object(path):
	""" Extract simulation results as list of objects.""" 
	data = []
	with open(path, newline='') as csvfile:
		reader = csv.DictReader(csvfile, skipinitialspace=True)
		for row in reader:
			row = {k:float(v) for k,v in row.items()}
			data.append(row)
	return data


def filter_object(data, data_ref):
	""" Filter list of objects by specific sub-objects. """
	filtered = data
	try:
		for key, value in data_ref.items():
			filtered = list(filter(lambda elem: elem[key] == value, filtered))
	except KeyError:
		print('There is no key', key, 'to be reduced!')
	return filtered


def find_event_on_y(x, y, factor):
	Y_event = factor * y[0]
	f = interpolate.interp1d(y, x)
	T_event = f(Y_event)
	event = (T_event, Y_event)
	return event


def main():
	data_all = extract_object(path)

	taus = [_['Residence_Time_C1__PSR_PSR_(C1)_(msec)'] for _ in data_all]
	taus = sorted(list(set(taus)))
	phis = [_['Equivalence_Ratio_C1_Inlet1_PSR_(C1)_()'] for _ in data_all]
	phis = sorted(list(set(phis)))

	specie = 'CH4'
	
	###
	fig_index = 1
	fig = pylab.figure(fig_index)
	pylab.axes([0.125, 0.2, 0.95-0.125, 0.95-0.2])
	pylab.xlim(800, 2000)
	pylab.ylim(0, 0.1)
	color = ['r', 'b', 'g', 'k', 'm']
	linestyle = ['-', '--']

	keys = ['Temperature_C1__PSR_PSR_(C1)_(K)', 'Mole_fraction_' + specie + '_()'] 
	event = []
	for phi in phis:
		for tau in taus:
			data_ref = {'Equivalence_Ratio_C1_Inlet1_PSR_(C1)_()':phi, 'Residence_Time_C1__PSR_PSR_(C1)_(msec)':tau}
			data = filter_object(data_all, data_ref)
			x = [_[keys[0]] for _ in data]
			y = [_[keys[1]] for _ in data]
			clr = color[taus.index(tau)]
			ls = linestyle[phis.index(phi)]
			lbl = '$\phi: {}, \\tau: {}$'.format(phi, tau)
			pylab.plot(x, y, color=clr, ls=ls, label=lbl)
			event_ = data_ref
			event_['ignition'] = find_event_on_y(x, y, 0.95)
			event_['burnout'] = find_event_on_y(x, y, 0.05)
			event.append(event_)
	pylab.xlabel('Temperature [K]')
	pylab.ylabel('Mole Fraction [-]')
	pylab.legend()
	pylab.savefig(os.path.join(plot_path, specie + '.eps'))

	###
	fig_index = 2
	fig = pylab.figure(fig_index)
	pylab.axes([0.125, 0.2, 0.95-0.125, 0.95-0.2])
	pylab.xlim(min(taus), max(taus))
	pylab.ylim(800, 1800)
	keys = ['Residence_Time_C1__PSR_PSR_(C1)_(msec)', 'ignition', 'burnout']
	for phi in phis:
		data_ref = {'Equivalence_Ratio_C1_Inlet1_PSR_(C1)_()':phi}
		data = filter_object(event, data_ref)
		lbl = '$gas A, ignition, \phi:{}$'.format(phi)
		x = [_[keys[0]] for _ in data]
		y = [_[keys[1]][0] for _ in data]
		clr = color[phis.index(phi)]
		pylab.plot(x, y, color=clr, ls='-', label=lbl)

		lbl = '$gas A, burnout, \phi:{}$'.format(phi)
		y = [_[keys[2]][0] for _ in data]
		pylab.plot(x, y, color=clr, ls='--', label=lbl)
	pylab.legend()
	pylab.xlabel('$\\tau$ [ms]')
	pylab.ylabel('Temperature [K]')
	pylab.savefig(os.path.join(plot_path, specie + 'combustion.eps'))


if __name__ == '__main__':
	main()
