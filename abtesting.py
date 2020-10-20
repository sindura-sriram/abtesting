from scipy import stats
from scipy.stats import t as t_dist
from scipy.stats import chi2
import numpy as np

from abtesting_test import *

# You can comment out these lines! They are just here to help follow along to the tutorial.
#print(t_dist.cdf(-2, 20)) # should print .02963
#print(t_dist.cdf(2, 20)) # positive t-score (bad), should print .97036 (= 1 - .2963)

#print(chi2.cdf(23.6, 12)) # prints 0.976
#print(1 - chi2.cdf(23.6, 12)) # prints 1 - 0.976 = 0.023 (yay!)

# TODO: Fill in the following functions! Be sure to delete "pass" when you want to use/run a function!
# NOTE: You should not be using any outside libraries or functions other than the simple operators (+, **, etc)
# and the specifically mentioned functions (i.e. round, cdf functions...)

def slice_2D(list_2D, start_row, end_row, start_col, end_col):
    '''
    Splices a the 2D list via start_row:end_row and start_col:end_col
    :param list: list of list of numbers
    :param nums: start_row, end_row, start_col, end_col
    :return: the spliced 2D list (ending indices are exclsive)
    '''
    to_append = []
    for l in range(start_row, end_row):
        to_append.append(list_2D[l][start_col:end_col])

    return to_append

def get_avg(nums):
    '''
    Helper function for calculating the average of a sample.
    :param nums: list of numbers
    :return: average of list
    '''
    #TODO: fill me in!
    total = float(0);
    count = 0;
    for i in nums:
        total += i;
        count += 1;
    return total/count;


def get_stdev(nums):
    '''
    Helper function for calculating the standard deviation of a sample.
    :param nums: list of numbers
    :return: standard deviation of list
    '''
    #TODO: fill me in!
    mean = get_avg(nums)
    count = 0;
    for i in nums:
        count+=1;
    variance = float(0);
    for i in nums:
        variance += (i-mean)**2;
    variance = variance/(count-1);
    return variance**0.5;

def get_standard_error(a, b):
    '''
    Helper function for calculating the standard error, given two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: standard error of a and b (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    stdev_squared_a = get_stdev(a)**2;
    stdev_squared_b = get_stdev(b)**2;

    stderr = stdev_squared_a/len(a) + stdev_squared_b/len(b);

    return stderr**0.5;

def get_2_sample_df(a, b):
    '''
    Calculates the combined degrees of freedom between two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: integer representing the degrees of freedom between a and b (see studio 6 guide for this equation!)
    HINT: you can use Math.round() to help you round!
    '''
    #TODO: fill me in!
    std_a = get_stdev(a);
    std_b = get_stdev(b);
    stderr = get_standard_error(a,b);
    df = round(stderr**4/(((std_a**2/len(a))**2)/(len(a)-1)+((std_b**2/len(b))**2)/(len(b)-1)));
    return df;


def get_t_score(a, b):
    '''
    Calculates the t-score, given two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: number representing the t-score given lists a and b (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    return (-np.abs(get_avg(b) - get_avg(a)))/get_standard_error(a,b);

def perform_2_sample_t_test(a, b):
    '''
    ** DO NOT CHANGE THE NAME OF THIS FUNCTION!! ** (this will mess with our autograder)
    Calculates a p-value by performing a 2-sample t-test, given two lists of numbers.
    :param a: list of numbers
    :param b: list of numbers
    :return: calculated p-value
    HINT: the t_dist.cdf() function might come in handy!
    '''
    #TODO: fill me in!
    t_score = get_t_score(a,b);
    deg_freedom = get_2_sample_df(a,b);
    return t_dist.cdf(t_score,deg_freedom);


# [OPTIONAL] Some helper functions that might be helpful in get_expected_grid().
# def row_sum(observed_grid, ele_row):
# def col_sum(observed_grid, ele_col):
# def total_sum(observed_grid):
# def calculate_expected(row_sum, col_sum, tot_sum):

def row_sum(observed_grid, row):
    sum = 0;
    for cell in observed_grid[row]:
        sum += cell;
    return sum;

def col_sum(observed_grid, col):
    sum = 0;
    row=0;
    for row in range(len(observed_grid)):
        sum += observed_grid[row][col];
    return sum;

def total_sum(observed_grid):
    sum = 0;
    row = 0;
    for i in range(len(observed_grid)):
        for j in range(len(observed_grid[row])):
            sum+=observed_grid[i][j];
        row+=1;
    return sum;

def calculate_expected(row, col, tot):
    return (row*col)/tot;

def get_expected_grid(observed_grid):
    '''
    Calculates the expected counts, given the observed counts.
    ** DO NOT modify the parameter, observed_grid. **
    :param observed_grid: 2D list of observed counts
    :return: 2D list of expected counts
    HINT: To clean up this calculation, consider filling in the optional helper functions below!
    '''
    #TODO: fill me in!
    expected = np.copy(observed_grid);
    for i in range(len(observed_grid)):
        for j in range(len(observed_grid[i])):
            expected[i][j] = calculate_expected(row_sum(observed_grid, i), col_sum(observed_grid, j), total_sum(observed_grid));
    return expected;

def df_chi2(observed_grid):
    '''
    Calculates the degrees of freedom of the expected counts.
    :param observed_grid: 2D list of observed counts
    :return: degrees of freedom of expected counts (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    row=0;
    col=0;
    for i in range(len(observed_grid)):
        col=0;
        for j in range(len(observed_grid[i])):
            col+=1;
        row+=1;
    return (row-1)*(col-1);

def chi2_value(observed_grid):
    '''
    Calculates the chi^2 value of the expected counts.
    :param observed_grid: 2D list of observed counts
    :return: associated chi^2 value of expected counts (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    expected = get_expected_grid(observed_grid);
    chi_squared = 0;
    for i in range(len(expected)):
        for j in range(len(expected[i])):
            chi_squared+= ((observed_grid[i][j]-expected[i][j])**2)/expected[i][j];
    return chi_squared;

def perform_chi2_homogeneity_test(observed_grid):
    '''
    ** DO NOT CHANGE THE NAME OF THIS FUNCTION!! ** (this will mess with our autograder)
    Calculates the p-value by performing a chi^2 test, given a list of observed counts
    :param observed_grid: 2D list of observed counts
    :return: calculated p-value
    HINT: the chi2.cdf() function might come in handy!
    '''
    #TODO: fill me in!
    chi_score = chi2_value(observed_grid);
    deg_freedom = df_chi2(observed_grid);
    hg = 1-chi2.cdf(chi_score,deg_freedom);
    if hg < 1e-6:
        return round(hg);
    return hg;

# These commented out lines are for testing your main functions. 
# Please uncomment them when finished with your implementation and confirm you get the same values :)
def data_to_num_list(s):
  '''
    Takes a copy and pasted row/col from a spreadsheet and produces a usable list of nums. 
    This will be useful when you need to run your tests on your cleaned log data!
    :param str: string holding data
    :return: the spliced list of numbers
    '''
  return list(map(float, s.split()))


# t_test 1:
a_t1_list = data_to_num_list(a1) 
b_t1_list = data_to_num_list(b1)
print(get_t_score(a_t1_list, b_t1_list)) 
print("this should be -129.500\n")
print(perform_2_sample_t_test(a_t1_list, b_t1_list)) 
print("this should be 0.0000\n")
# why do you think this is? Take a peek at a1 and b1 in abtesting_test.py :)

# t_test 2:
a_t2_list = data_to_num_list(a2) 
b_t2_list = data_to_num_list(b2)
print(get_t_score(a_t2_list, b_t2_list)) #
print("this should be -1.48834\n")
print(perform_2_sample_t_test(a_t2_list, b_t2_list)) # 
print("this should be .082379\n")

# t_test 3:
a_t3_list = data_to_num_list(a3) 
b_t3_list = data_to_num_list(b3)
print(get_t_score(a_t3_list, b_t3_list)) # 
print("this should be -2.88969\n")
print(perform_2_sample_t_test(a_t3_list, b_t3_list)) # 
print("this should be .005091\n")

# chi2_test 1:
a_c1_list = data_to_num_list(a_count_1) 
b_c1_list = data_to_num_list(b_count_1)
c1_observed_grid = [a_c1_list, b_c1_list]
print(chi2_value(c1_observed_grid)) # 
print("this should be 4.103536 ")
print(perform_chi2_homogeneity_test(c1_observed_grid)) # 
print("this should be .0427939\n")

# chi2_test 2:
a_c2_list = data_to_num_list(a_count_2) 
b_c2_list = data_to_num_list(b_count_2)
c2_observed_grid = [a_c2_list, b_c2_list]
print(chi2_value(c2_observed_grid)) # 
print("this should be 33.86444\n")
print(perform_chi2_homogeneity_test(c2_observed_grid)) # 
print("this should be 0.0000\n")
# Again, why do you think this is? Take a peek at a_count_2 and b_count_2 in abtesting_test.py :)

# chi2_test 3:
a_c3_list = data_to_num_list(a_count_3) 
b_c3_list = data_to_num_list(b_count_3)
c3_observed_grid = [a_c3_list, b_c3_list]
print(chi2_value(c3_observed_grid)) # 
print("this should be .3119402\n")
print(perform_chi2_homogeneity_test(c3_observed_grid)) # 
print("this should be .57649202\n")



