'''
Parses the analysis files (created by the analysis module) to perform statistical
analysis, specifically by evaluating the means, medians, and Wilcoxon's tests.
'''

import numpy as np
import scipy.stats
from common import dilation_radii, rau_dsc_dtype, yuanxia_dsc_dtype, rau_gtc_dtype, yuanxia_gtc_dtype

def print_mean_median(matrix, measure, dilation_radii):
    '''
    Calculates and prints the mean and median of a measure (DSC or GTC) for all
    given dilation radii. Also prints out the dilation radii that had the largest
    differences for mean and median.

    matrix: The read in matrix with columns corresponding to the analysis files.
    measure: Either 'dsc' or 'gtc'.
    dilation_radii: An iteratable for the dilation radii to consider.
    '''
    min_measure_mean = 1
    min_radius_mean = -1
    max_measure_mean = 0
    max_radius_mean = -1
    min_measure_median = 1
    min_radius_median = -1
    max_measure_median = 0
    max_radius_median = -1

    for dilation_radius in dilation_radii:
        filtered = [row[measure] for row in matrix if row['dilation_radius'] == dilation_radius]
        mean = np.mean(filtered)
        median = np.median(filtered)
        print('Radius', dilation_radius)
        print('  Mean ' + measure.upper() + ':', mean)
        print('  Median ' + measure.upper() + ':', median)
        
        if mean < min_measure_mean:
            min_measure_mean = mean
            min_radius_mean = dilation_radius
        if mean > max_measure_mean:
            max_measure_mean = mean
            max_radius_mean = dilation_radius
        if median < min_measure_median:
            min_measure_median = median
            min_radius_median = dilation_radius
        if median > max_measure_median:
            max_measure_median = median
            max_radius_median = dilation_radius
        
    print('Largest %s mean difference was between radii %d and %d = %.4f' % (measure.upper(), min_radius_mean, max_radius_mean, max_measure_mean - min_measure_mean))
    print('Largest %s median difference was between radii %d and %d = %.4f' % (measure.upper(), min_radius_median, max_radius_median, max_measure_median - min_measure_median))

def print_wilcoxon(matrix, measure, radius1, radius2):
    '''
    Calculates and prints the Wilcoxon test p-value for comparing between two radii.

    matrix: The read in matrix with columns corresponding to the analysis files.
    measure: Either 'dsc' or 'gtc'.
    radius1, radius2: The dilation radii that are being compared (the independent
    variables in this test).
    '''
    filtered1 = [row[measure] for row in matrix if row['dilation_radius'] == radius1]
    filtered2 = [row[measure] for row in matrix if row['dilation_radius'] == radius2]
    _, p_value = scipy.stats.wilcoxon(filtered1, filtered2)
    print('Wilcoxon result for %s between radii %d and %d has p = %.6f' % (measure.upper(), radius1, radius2, p_value))

def print_pop_normality(matrix, measure):
    filtered = [row[measure] for row in matrix]
    _, p = scipy.stats.normaltest(filtered)
    print('Data is NOT normally distributed with p = %.4f' % p)

def print_groups_std(matrix, measure, dilation_radii):
    std = []
    for radius in dilation_radii:
        filtered_radii = [row[measure] for row in matrix if row['dilation_radius'] == radius]
        std.append(np.std(filtered_radii))
    print('Standard deviations for %s are %s' % (measure.upper(), str(std)))
        
def print_anova(matrix, measure, dilation_radii):
    filtered_by_radi = []
    for radius in dilation_radii:
        filtered_radii = [row[measure] for row in matrix if row['dilation_radius'] == radius]
        filtered_by_radi.append(filtered_radii)
    _, p_value = scipy.stats.f_oneway(*filtered_by_radi)
    print('ANOVA for %s has p value = %0.4f' % (measure.upper(), p_value))

rau_dsc_strokes = np.loadtxt('./analysis/dsc/rau_strokes.txt', dtype=rau_dsc_dtype, skiprows=1)
rau_dsc_points = np.loadtxt('./analysis/dsc/rau_points.txt', dtype=rau_dsc_dtype, skiprows=1)
yuanxia_dsc = np.loadtxt('./analysis/dsc/yuanxia.txt', dtype=yuanxia_dsc_dtype, skiprows=1)
rau_gtc_strokes = np.loadtxt('./analysis/gtc/rau_strokes.txt', dtype=rau_gtc_dtype, skiprows=1)
rau_gtc_points = np.loadtxt('./analysis/gtc/rau_points.txt', dtype=rau_gtc_dtype, skiprows=1)
yuanxia_gtc = np.loadtxt('./analysis/gtc/yuanxia.txt', dtype=yuanxia_gtc_dtype, skiprows=1)

print('Rau\'s strokes:')
print_mean_median(rau_dsc_strokes, 'dsc', dilation_radii)
print_mean_median(rau_gtc_strokes, 'gtc', dilation_radii)
print_wilcoxon(rau_dsc_strokes, 'dsc', 0, 4)
print_wilcoxon(rau_gtc_strokes, 'gtc', 0, 4)
print_pop_normality(rau_dsc_strokes, 'dsc')
print_pop_normality(rau_gtc_strokes, 'gtc')
print_groups_std(rau_dsc_strokes, 'dsc', dilation_radii)
print_groups_std(rau_gtc_strokes, 'gtc', dilation_radii)
print_anova(rau_dsc_strokes, 'dsc', dilation_radii)
print_anova(rau_gtc_strokes, 'gtc', dilation_radii)

print('\nRau\'s points:')
print_mean_median(rau_dsc_points, 'dsc', dilation_radii)
print_mean_median(rau_gtc_points, 'gtc', dilation_radii)
print_wilcoxon(rau_dsc_points, 'dsc', 0, 4)
print_wilcoxon(rau_gtc_points, 'gtc', 0, 4)
print_pop_normality(rau_dsc_points, 'dsc')
print_pop_normality(rau_gtc_points, 'gtc')
print_groups_std(rau_dsc_points, 'dsc', dilation_radii)
print_groups_std(rau_gtc_points, 'gtc', dilation_radii)
print_anova(rau_dsc_points, 'dsc', dilation_radii)
print_anova(rau_gtc_points, 'gtc', dilation_radii)

print('\nYuaxia\'s points:')
print_mean_median(yuanxia_dsc, 'dsc', dilation_radii)
print_mean_median(yuanxia_gtc, 'gtc', dilation_radii)
print_wilcoxon(yuanxia_dsc, 'dsc', 0, 4)
print_wilcoxon(yuanxia_gtc, 'gtc', 0, 4)
print_pop_normality(yuanxia_dsc, 'dsc')
print_pop_normality(yuanxia_gtc, 'gtc')
print_groups_std(yuanxia_dsc, 'dsc', dilation_radii)
print_groups_std(yuanxia_gtc, 'gtc', dilation_radii)
print_anova(yuanxia_dsc, 'dsc', dilation_radii)
print_anova(yuanxia_gtc, 'gtc', dilation_radii)
