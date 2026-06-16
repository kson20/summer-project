# Royal Holloway Physics department first year fitting toolset
# Fit types: linear, inverse, quadratic, exponential, gaussian, lorentzian, and charging.

# Written by Daniel R. M. Woods

# Code adapted from Fitter by Prof. Stewart T. Boogert

# First Version 06/03/2019
# Current Version - 2.11 - 15/11/2021

import numpy as np

import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

from sys import exit as _exit

def read_file(file_name):
    """
    Reads in a data file and assigns the labels and data to given variables.

    The file name must be passed in as a string, i.e. surrounded by ' or ".

    Usage: labels, data = pl.read_file('file_name')

     File  :

    <Title>

    <xDataLabel>    <yDataLabel>  <--- Tab Separated

    <x1>         <y1>         <x1Err>    <y1Err>

    <x2>         <y2>         <x2Err>    <y2Err>

    <x3>         <y3>         <x3Err>    <y3Err>

    """

    file = open(file_name)

    data = []

    labels = []

    i_read_labels = 0

    # Loop checks the first lines of the data file, then reads the axis labels
    # and the data

    for l in file:

        if l[0] == '#' :

        # Ignores commented lines

            continue

        elif i_read_labels == 0  :

        # Reads the first line (i.e. title)

            title = l.strip()

            labels.append(title)

            i_read_labels += 1

            continue

        elif i_read_labels == 1 :

        # Reads the second line (i.e. x and y-axis)

            axis_names = l.strip()

            if not axis_names:  # Checks if axis_names is an empty string,
                                # meaning that there is no figure title in the
                                # data file

                print('\n'+'----------')
                print('''\
    ERROR: Figure title not correctly formatted. First uncommented line of file
    must be the figure title, next uncommented line must be the axis titles
    seperated by a tab.'''+'\n')
                print('''\
    You will need to redo read_file before continuing.''')
                print('----------'+'\n')
                labels = None
                data = None
                _exit()

            axis_names = axis_names.split('\t')

            if len(axis_names) != 2:    # Checks that axis labels were formatted
                                        # correctly

                print('\n'+'----------')
                print('''\
    ERROR: Axis titles not correctly formatted. Axes titles must be seperated
    by a single tab. Some editors may not enter a tab properly (i.e. Spyder),
    instead you can open your file in notepad and press tab there.'''+'\n')
                print('''\
    You will need to redo read_file before continuing.''')
                print('----------'+'\n')
                labels = None
                data = None
                _exit()

            labels.append(axis_names[0])
            labels.append(axis_names[1])

            i_read_labels += 1

            continue

        # Reads every line in file, adding lines with data of length 4,
        # removing blank lines and throwing an error if line is not length 4

        line = l.strip().split()

        if line != []:

            if len(line) == 4:

                data.append(list(map(float,line)))

            else:

                print('\n'+'----------')
                print('''\
    ERROR: line '''+str(line)+'''
    is not of length 4. All lines in the file must contain an x-value, a
    y-value, an x-error, and a y-error.'''+'\n')
                print('''\
    If this looks like an axis or figure title, then your file was not
    correctly formatted. First uncommented line of file must be the figure
    title, next uncommented line must be the axis titles seperated by a tab,
    and all other uncommented lines must be data.'''+'\n')
                print('''\
    You will need to redo read_file before continuing.''')
                print('----------'+'\n')
                labels = None
                data = None
                _exit()

        else:

            continue

    data = np.array(data)

    xErr  = data[:,2]

    yErr  = data[:,3]

# Checks for 0s in errors
# May not be required with the proper set-up of curve_fit
    for i in xErr:
        if i == 0:
            print('\n'+'----------')
            print('''\
    ERROR: Plotter will not be able to fit a curve to data that has
    uncertainties of zero.'''+'\n')
            print('''\
    You will need to redo read_file before continuing.''')
            print('----------'+'\n')
            labels = None
            data = None
            _exit()

    for i in yErr:
        if i == 0:
            print('\n'+'----------')
            print('''\
    ERROR: Plotter will not be able to fit a curve to data that has
    uncertainties of zero.'''+'\n')
            print('''\
    You will need to redo read_file before continuing.''')
            print('----------'+'\n')
            labels = None
            data = None
            _exit()

    print('File name             = ',file_name)

    print('Data shape            = ',np.shape(data))

    return(labels, data)


def plot_data_scatter(labels, data, format_data = ['b','o', 'None']):
    """
    Plots a scatter plot of a given set of data with a given set of axis labels.

    Data should by of the form of an array of 4 element lists, containing
    x-data, y-data, x-error, and y-error.

    A list of three strings can be passed to the function to provide line
    formating in the following format: ['colour', 'marker', 'linestyle'].

    Go to the following site for information on allowed formating
    parameters: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html

    Usage: pl.plot_data_scatter(labels, data)
       or: pl.plot_data_scatter(labels, data, ['m','x','-'])

    """

    plt.scatter(data[:,0], data[:,1], color=format_data[0],
                marker=format_data[1], linestyle=format_data[2])
    plt.title(labels[0])
    plt.xlabel(labels[1])
    plt.ylabel(labels[2])


def plot_data_scatter_errorbars(labels, data, format_data = ['b','o','None']):
    """
    Plots a scatter plot, with errors, of a given set of data with a given set
    of axis labels.

    Data should by of the form of an array of 4 element lists, containing
    x-data, y-data, x-error, and y-error.

    A list of three strings can be passed to the function to provide line
    formating in the following format: ['colour', 'marker', 'linestyle'].

    Go to the following site for information on allowed formating
    parameters: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html

    Usage: pl.plot_data_scatter_errorbars(labels, data)
       or: pl.plot_data_scatter_errorbars(labels, data, ['m','x','-'])

    """

    plt.errorbar(data[:,0], data[:,1], data[:,3], data[:,2],
                 color=format_data[0], marker=format_data[1],
                 linestyle='solid')
    plt.title(labels[0])
    plt.xlabel(labels[1])
    plt.ylabel(labels[2])


def plot_data_HR(labels, data, format_data = ['b','o','None']):
    """

    Plots an HR diagram, with errors, of a given set of data with a given set
    of axis labels.

    Data should by of the form of an array of 4 element lists, containing
    x-data, y-data, x-error, and y-error.

    A list of three strings can be passed to the function to provide line
    formating in the following format: ['colour', 'marker', 'linestyle'].

    Go to the following site for information on allowed formating
    parameters: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html

    Usage: plot_data_HR(labels, data)
       or: plot_data_HR(labels, data, ['m','x','-'])

    """

    plt.errorbar(data[:,0], data[:,1], data[:,3], data[:,2],
                 color=format_data[0], marker=format_data[1],
                 linestyle=format_data[2])
    plt.title(labels[0])
    plt.xlabel(labels[1])
    plt.ylabel(labels[2])
    plt.gca().invert_yaxis()


def plot_data_line(labels, data, format_data = ['b','None','-']):
    """
    Plots a line plot of a given set of data with a given set of axis labels.

    Data should by of the form of an array of 4 element lists, containing
    x-data, y-data, x-error, and y-error.

    A list of three strings can be passed to the function to provide line
    formating in the following format: ['colour', 'marker', 'linestyle'].

    Go to the following site for information on allowed formating
    parameters: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html

    Usage: pl.plot_data_line(labels, data)
       or: pl.plot_data_line(labels, data, ['m','x','-'])
    """

    plt.plot(data[:,0], data[:,1],
             color=format_data[0], marker=format_data[1],
             linestyle=format_data[2])
    plt.title(labels[0])
    plt.xlabel(labels[1])
    plt.ylabel(labels[2])


def fit_data(data, fit_type, initial_guess = None):
    """
    Performs a fit on a data set of a type given and assigns the fit parameters
    to some given variable.

    A list of initial guess values of the fit parameters can also be passed
    into the function, but are not required.

    Allowed fit types: linear, inverse, quadratic, exponential, gaussian, lorentzian,
    and charging.

    The length of the list of initial guess values passed to the function
    varies based on fit type: 2, 3, 2, 3, 3, 3 respectively

    Usage: fit = pl.fit_data(data, 'linear')
       or: fit = pl.fit_data(data, 'linear', [m, c])
    """
    if fit_type == 'linear' or fit_type == 'Linear':
        print('Fit Type = linear')
        if initial_guess == None:
            initial_guess =  np.zeros(2)
        elif len(initial_guess) != 2:
            print('\n'+'----------')
            print('''\
    ERROR: Initial fit parameters not of the correct format. Parameters must be
    in a two element list or numpy array.''')
            print('----------'+'\n')
            _exit()
        fit = curve_fit(_linear_fit, data[:,0], data[:,1], initial_guess,
                        data[:,3], xtol=1e-12,full_output=True)
        print('Parameters                    =  m, c')

    elif fit_type == 'inverse' or fit_type == 'Inverse':
        print('Fit Type = inverse')
        if initial_guess == None:
            initial_guess =  np.zeros(1)
            initial_guess[0] = 1
        elif len(initial_guess) != 1:
            print('\n'+'----------')
            print('''\
    ERROR: Initial fit parameters not of the correct format. Parameters must be
    in a two element list or numpy array.''')
            print('----------'+'\n')
            _exit()
        fit = curve_fit(_inverse_fit, data[:,0], data[:,1], initial_guess,
                        data[:,3], xtol=1e-12,full_output=True)
        print('Parameters                    =  A')

    elif fit_type == 'quadratic' or fit_type == 'Quadratic':
        print('Fit Type = quadratic')
        if initial_guess == None:
            initial_guess =  np.zeros(3)
        elif len(initial_guess) != 3:
            print('\n'+'----------')
            print('''\
    ERROR: Initial fit parameters not of the correct format. Parameters must be
    in a three element list or numpy array.''')
            print('----------'+'\n')
            _exit()
        fit = curve_fit(_quadratic_fit, data[:,0], data[:,1], initial_guess,
                        data[:,3], xtol=1e-12)
        print('Parameters                    =  a, b, c')

    elif fit_type == 'exponential' or fit_type == 'Exponential':
        print('Fit Type = exponential')
        if initial_guess == None:
            initial_guess =  np.zeros(2)
        elif len(initial_guess) != 2:
            print('\n'+'----------')
            print('''\
    ERROR: Initial fit parameters not of the correct format. Parameters must be
    in a two element list or numpy array.''')
            print('----------'+'\n')
            _exit()
        fit = curve_fit(_exponential_fit, data[:,0], data[:,1], initial_guess,
                        data[:,3], xtol=1e-12)
        print('Parameters                    =  A, k')

    elif fit_type == 'gaussian' or fit_type == 'Gaussian':
        print('Fit Type = gaussian')
        if initial_guess == None:
            initial_guess =  np.zeros(3)
            initial_guess[0] = data[:,1].max()
            initial_guess[1] = data[:,0].mean()
            initial_guess[2] = 5.0
        elif len(initial_guess) != 3:
            print('\n'+'----------')
            print('''\
    ERROR: Initial fit parameters not of the correct format. Parameters must be
    in a three element list or numpy array.''')
            print('----------'+'\n')
            _exit()
        fit = curve_fit(_gaussian_fit, data[:,0], data[:,1], initial_guess,
                        data[:,3], xtol=1e-12)
        print('Parameters                    =  a, sigma, mu')

    elif fit_type == 'lorentzian' or fit_type == 'Lorentzian':
        print('Fit Type = lorentzian')
        if initial_guess == None:
            initial_guess =  np.zeros(3)
            initial_guess[0] = data[:,1].max()
            initial_guess[1] = 1.0
            initial_guess[2] = data[:,0].mean()
        elif len(initial_guess) != 3:
            print('\n'+'----------')
            print('''\
    ERROR: Initial fit parameters not of the correct format. Parameters must be
    in a three element list or numpy array.''')
            print('----------'+'\n')
            _exit()
        fit = curve_fit(_lorentzian_fit, data[:,0], data[:,1], initial_guess,
                        data[:,3], xtol=1e-12)
        print('Parameters                    =  A, w0, b')

    elif fit_type == 'charging' or fit_type == 'Charging':
        print('Fit Type = charging')
        if initial_guess == None:
            initial_guess =  np.zeros(3)
        elif len(initial_guess) != 3:
            print('\n'+'----------')
            print('''\
    ERROR: Initial fit parameters not of the correct format. Parameters must be
    in a three element list or numpy array.''')
            print('----------'+'\n')
            _exit()
        fit = curve_fit(_charging_fit, data[:,0], data[:,1], initial_guess,
                        data[:,3], xtol=1e-12)
        print('Parameters                    =  A, B, k')

    else:
        print('\n'+'----------')
        print('''\
    ERROR: function not known. Known functions are: linear, inverse, quadratic,
    exponential, gaussian, lorentzian, and charging.''')
        print('----------'+'\n')
        _exit()

    print('Original fit parameters       = ',initial_guess)
    print('Calculated fit parameters     = ',fit[0])
    print('Errors on fit parameters      = ',np.sqrt(np.diag(fit[1])))
    fit = [fit, fit_type]
    return fit


def plot_fit(labels, data, fit, format_data = ['b','o','None'],
             format_fit = ['r','None', '-'], data_label = None):
    """
    Plots a fit alongside the starting data.

    Two lists of three strings can be passed to the function to dictate the
    formating of the data set and of the fit, with the following
    format: ['colour' , 'marker' , 'linestyle'].

    The data can be given a specific label by passing in a string to the
    function. This changes its name in the legend.

    Usage: pl.plot_fit(labels, data, fit)
       or: pl.plot_fit(labels, data, fit, ['m','x','--'],
                    ['g','^',':'], data_label = 'Data Set A')
           etc.
    """
    fit_type = fit[-1]

    if data_label != None:
        plt.errorbar(data[:,0], data[:,1], data[:,3], data[:,2],
                      label=data_label, color=format_data[0],
                      marker=format_data[1], linestyle=format_data[2])
    else:
        plt.errorbar(data[:,0], data[:,1], data[:,3], data[:,2],
                      label='Original Data', color=format_data[0],
                      marker=format_data[1], linestyle=format_data[2])

    x_range = np.linspace(np.amin(data[:,0]), np.amax(data[:,0]), 100)

    if fit_type == 'linear' or fit_type == 'Linear':
        plt.plot(x_range, _linear_fit(x_range, *fit[0][0]),
                 label = 'Linear Fit', color=format_fit[0],
                 marker=format_fit[1], linestyle=format_fit[2])

    elif fit_type == 'inverse' or fit_type == 'Inverse':
        plt.plot(x_range, _inverse_fit(x_range, *fit[0][0]),
                 label = 'Inverse Fit', color=format_fit[0],
                 marker=format_fit[1], linestyle=format_fit[2])

    elif fit_type == 'quadratic' or fit_type == 'Quadratic':
        plt.plot(x_range, _quadratic_fit(x_range, *fit[0][0]),
                 label = 'Quadratic Fit', color=format_fit[0],
                 marker=format_fit[1], linestyle=format_fit[2])

    elif fit_type == 'exponential' or fit_type == 'Exponential':
        plt.plot(x_range, _exponential_fit(x_range, *fit[0][0]),
                 label = 'Exponential Fit', color=format_fit[0],
                 marker=format_fit[1], linestyle=format_fit[2])

    elif fit_type == 'charging' or fit_type == 'Charging':
        plt.plot(x_range, _charging_fit(x_range, *fit[0][0]),
                 label = 'Charging Fit', color=format_fit[0],
                 marker=format_fit[1], linestyle=format_fit[2])

    elif fit_type == 'gaussian' or fit_type == 'Gaussian':
        plt.plot(x_range, _gaussian_fit(x_range, *fit[0][0]),
                 label = 'Gaussian Fit', color=format_fit[0],
                 marker=format_fit[1], linestyle=format_fit[2])

    elif fit_type == 'lorentzian' or fit_type == 'Lorentzian':
        plt.plot(x_range, _lorentzian_fit(x_range, *fit[0][0]),
                 label = 'Lorentzian Fit', color=format_fit[0],
                 marker=format_fit[1], linestyle=format_fit[2])

    else:
        print('\n'+'----------')
        print('''\
    ERROR: function not known. Known functions are: linear, inverse,  quadratic,
    exponential, gaussian, lorentzian, and charging.''')
        print('----------'+'\n')
        _exit()

    plt.title(labels[0])
    plt.xlabel(labels[1])
    plt.ylabel(labels[2])
    plt.legend(loc='best')

def show_plot(file_name = None):
    """
    Displays all previously made plots on one set of axes.

    A string can be passed to this function to save the figure as a png.

    Usage: pl.show_plot()
       or: pl.show_plot('DataSetA.png')
    """
    if file_name != None:
        plt.savefig(str(file_name))
    plt.show()

_linear_fit = lambda x,p0,p1 : p0*x+p1
_quadratic_fit = lambda x,p0,p1,p2 : p0*x**2+p1*x+p2
_exponential_fit = lambda x,p0,p1 : p0*np.exp(p1*x)
_gaussian_fit = lambda x,p0,p1,p2 : p0/(p2*np.sqrt(2*np.pi))*np.exp(-(x-p1)**2/(2*p2**2))
_lorentzian_fit = lambda x, p0, p1, p2 : p0/np.power((np.power((np.power(p1, 2)-np.power(x,2)), 2) + (np.power(p2*x, 2))),0.5)
_charging_fit = lambda x,p0,p1,p2 : p0-p1*np.exp(-p2*x)
_inverse_fit = lambda x, p0 : p0 / x