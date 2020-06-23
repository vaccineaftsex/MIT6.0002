# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # TODO
    result = []
    for deg in degs:
        result.append(pylab.polyfit(x, y, deg))
    return result

#print(generate_models(pylab.array([1961, 1962, 1963]), pylab.array([-4.4, -5.5, -6.6]), [1, 2]))
    


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # TODO
    a = y - estimated
    mean = pylab.mean(y)
    b = y - mean
    return 1 - pylab.sum(a * a)/pylab.sum(b * b)


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    for model in models:
        pylab.figure()
        
        pylab.plot(x, y, 'b.')
        est = pylab.polyval(model, x)
        pylab.plot(x, est, 'r-')
        
        pylab.xlabel("years")
        pylab.ylabel("degrees Celsius")
        
        deg = len(model) - 1
        r_2 = r_squared(y, est)
        
        if deg == 1:
            pylab.title("degree " + str(deg) + " model, R^2 = " + str(r_2) + 
                        ",\n ratio of the standard error of this fitted curve's slope = "
                        + str(se_over_slope(x, y, est, model)))
        else:
            pylab.title("degree" + str(deg) + "model, R^2 = " + str(r_2))
        
#x = pylab.array(range(10))
#y = x * x
#models = generate_models(x, y, range(5))
#evaluate_models_on_training(x, y, models)

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # TODO
    temp = []
    for year in years:
        annual_temp = []
        for city in multi_cities:
            annual_temp.append(climate.get_yearly_temp(city, year).mean())
        temp.append(pylab.array(annual_temp).mean())
    return pylab.array(temp)


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moving_avg = []
    for i in range(len(y)):
        start = i - window_length + 1
        if start < 0:
            start = 0
            
        moving_avg.append(sum(y[start:i + 1])/(i - start + 1))
    return pylab.array(moving_avg)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # TODO
    x = y - estimated
    return pylab.sqrt(pylab.sum(x*x) / pylab.shape(y)[0])

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # TODO
    stand_dev = []
    for year in years:
        multi_cities_temp = pylab.zeros_like(climate.get_yearly_temp(multi_cities[0], year))
        for city in multi_cities:
            yearly_temp = climate.get_yearly_temp(city, year)
            multi_cities_temp = multi_cities_temp + yearly_temp
        city_avg = multi_cities_temp / len(multi_cities)
        stand_dev.append(pylab.std(city_avg))
    return pylab.array(stand_dev)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        pylab.figure()
        
        pylab.plot(x, y, 'b.')
        est = pylab.polyval(model, x)
        pylab.plot(x, est, 'r-')
        
        pylab.xlabel("years")
        pylab.ylabel("degrees Celsius")
        
        deg = len(model) - 1
        root_mean_sqr_error = rmse(y, est)
        
        pylab.title("degree " + str(deg) + " model, rmse = " + str(root_mean_sqr_error))
        

if __name__ == '__main__':
    
    data = Climate("data.csv")
    training_years = pylab.array(TRAINING_INTERVAL)
    testing_years = pylab.array(TESTING_INTERVAL)
    
    # Part A.4

#    temp = []
#    for year in TRAINING_INTERVAL:
#        temp.append(data.get_daily_temp('NEW YORK', 1, 10, year))
#    temperature = pylab.array(temp)
#    models = generate_models(training_years, temperature, [1])
#    evaluate_models_on_training(training_years, temperature, models)
#    
#    annual_temp = []
#    for year in TRAINING_INTERVAL:
#        annual_temp.append(data.get_yearly_temp('NEW YORK', year).mean())
#    annual_temperature = pylab.array(annual_temp)
#    models = generate_models(training_years, annual_temperature, [1])
#    evaluate_models_on_training(training_years, annual_temperature, models)
            
    
    # Part B
    
#    national = gen_cities_avg(data, CITIES, training_years)
#    models = generate_models(training_years, national, [1])
#    evaluate_models_on_training(training_years, national, models)

    # Part C
    
#    national = gen_cities_avg(data, CITIES, training_years)
#    national_moving_avg = moving_average(national, 5)
#    models = generate_models(training_years, national_moving_avg, [1])
#    evaluate_models_on_training(training_years, national_moving_avg, models)

    # Part D.2
#    national_train = gen_cities_avg(data, CITIES, training_years)
#    moving_avg_train = moving_average(national_train, 5)
#    models = generate_models(training_years, moving_avg_train, [1, 2, 20])
#    evaluate_models_on_training(training_years, moving_avg_train, models)
#    
#    national_test = gen_cities_avg(data, CITIES, testing_years)
#    moving_avg_test = moving_average(national_test, 5)
#    evaluate_models_on_testing(testing_years, moving_avg_test, models)

    # Part E
stand_dev = gen_std_devs(data, CITIES, training_years)
sigma_moving_avg = moving_average(stand_dev, 5)
models = generate_models(training_years, sigma_moving_avg, [1])
evaluate_models_on_training(training_years, sigma_moving_avg, models)
