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

def print_friedman(matrix, measure, dilation_radii):
    filtered_by_radi = []
    for radius in dilation_radii:
        filtered_radii = [row[measure] for row in matrix if row['dilation_radius'] == radius]
        filtered_by_radi.append(filtered_radii)
    _, p_value = scipy.stats.friedmanchisquare(*filtered_by_radi)
    print('Friedman test for %s has p value = %0.6f' % (measure.upper(), p_value))

rau_dsc_strokes = np.loadtxt('./analysis/dsc/rau_strokes.txt', dtype=rau_dsc_dtype, skiprows=1)
rau_dsc_points = np.loadtxt('./analysis/dsc/rau_points.txt', dtype=rau_dsc_dtype, skiprows=1)
yuanxia_dsc = np.loadtxt('./analysis/dsc/yuanxia.txt', dtype=yuanxia_dsc_dtype, skiprows=1)
rau_gtc_strokes = np.loadtxt('./analysis/gtc/rau_strokes.txt', dtype=rau_gtc_dtype, skiprows=1)
rau_gtc_points = np.loadtxt('./analysis/gtc/rau_points.txt', dtype=rau_gtc_dtype, skiprows=1)
yuanxia_gtc = np.loadtxt('./analysis/gtc/yuanxia.txt', dtype=yuanxia_gtc_dtype, skiprows=1)

# Time pressure versions
yuanxia_dsc15 = yuanxia_dsc[yuanxia_dsc['time_pressure'] == 15]
yuanxia_gtc15 = yuanxia_gtc[yuanxia_gtc['time_pressure'] == 15]
yuanxia_dsc25 = yuanxia_dsc[yuanxia_dsc['time_pressure'] == 25]
yuanxia_gtc25 = yuanxia_gtc[yuanxia_gtc['time_pressure'] == 25]
yuanxia_dsc40 = yuanxia_dsc[yuanxia_dsc['time_pressure'] == 40]
yuanxia_gtc40 = yuanxia_gtc[yuanxia_gtc['time_pressure'] == 40]

print('Stats for Boykov segmentation')
print('Rau\'s strokes:')
print_mean_median(rau_dsc_strokes, 'dsc', dilation_radii)
print_mean_median(rau_gtc_strokes, 'gtc', dilation_radii)
print_wilcoxon(rau_dsc_strokes, 'dsc', 0, 4)
print_wilcoxon(rau_gtc_strokes, 'gtc', 0, 4)
print_pop_normality(rau_dsc_strokes, 'dsc')
print_pop_normality(rau_gtc_strokes, 'gtc')
print_friedman(rau_dsc_strokes, 'dsc', dilation_radii)
print_friedman(rau_gtc_strokes, 'gtc', dilation_radii)

print('\nRau\'s points:')
print_mean_median(rau_dsc_points, 'dsc', dilation_radii)
print_mean_median(rau_gtc_points, 'gtc', dilation_radii)
print_wilcoxon(rau_dsc_points, 'dsc', 0, 4)
print_wilcoxon(rau_gtc_points, 'gtc', 0, 4)
print_pop_normality(rau_dsc_points, 'dsc')
print_pop_normality(rau_gtc_points, 'gtc')
print_friedman(rau_dsc_points, 'dsc', dilation_radii)
print_friedman(rau_gtc_points, 'gtc', dilation_radii)

print('\nYuaxia\'s points (time pressure 15):')
print_mean_median(yuanxia_dsc15, 'dsc', dilation_radii)
print_mean_median(yuanxia_gtc15, 'gtc', dilation_radii)
print_wilcoxon(yuanxia_dsc15, 'dsc', 0, 4)
print_wilcoxon(yuanxia_gtc15, 'gtc', 0, 4)
print_pop_normality(yuanxia_dsc15, 'dsc')
print_pop_normality(yuanxia_gtc15, 'gtc')
print_friedman(yuanxia_dsc15, 'dsc', dilation_radii)
print_friedman(yuanxia_gtc15, 'gtc', dilation_radii)

print('\nYuaxia\'s points (time pressure 25):')
print_mean_median(yuanxia_dsc25, 'dsc', dilation_radii)
print_mean_median(yuanxia_gtc25, 'gtc', dilation_radii)
print_wilcoxon(yuanxia_dsc25, 'dsc', 0, 4)
print_wilcoxon(yuanxia_gtc25, 'gtc', 0, 4)
print_pop_normality(yuanxia_dsc25, 'dsc')
print_pop_normality(yuanxia_gtc25, 'gtc')
print_friedman(yuanxia_dsc25, 'dsc', dilation_radii)
print_friedman(yuanxia_gtc25, 'gtc', dilation_radii)

print('\nYuaxia\'s points (time pressure 40):')
print_mean_median(yuanxia_dsc40, 'dsc', dilation_radii)
print_mean_median(yuanxia_gtc40, 'gtc', dilation_radii)
print_wilcoxon(yuanxia_dsc40, 'dsc', 0, 4)
print_wilcoxon(yuanxia_gtc40, 'gtc', 0, 4)
print_pop_normality(yuanxia_dsc40, 'dsc')
print_pop_normality(yuanxia_gtc40, 'gtc')
print_friedman(yuanxia_dsc40, 'dsc', dilation_radii)
print_friedman(yuanxia_gtc40, 'gtc', dilation_radii)
print()

rau_dsc_strokes_onecut = np.loadtxt('./analysis/dsc/rau_strokes_onecut.txt', dtype=rau_dsc_dtype, skiprows=1)
rau_dsc_points_onecut = np.loadtxt('./analysis/dsc/rau_points_onecut.txt', dtype=rau_dsc_dtype, skiprows=1)
yuanxia_dsc_onecut = np.loadtxt('./analysis/dsc/yuanxia_onecut.txt', dtype=yuanxia_dsc_dtype, skiprows=1)
rau_gtc_strokes_onecut = np.loadtxt('./analysis/gtc/rau_strokes_onecut.txt', dtype=rau_gtc_dtype, skiprows=1)
rau_gtc_points_onecut = np.loadtxt('./analysis/gtc/rau_points_onecut.txt', dtype=rau_gtc_dtype, skiprows=1)
yuanxia_gtc_onecut = np.loadtxt('./analysis/gtc/yuanxia_onecut.txt', dtype=yuanxia_gtc_dtype, skiprows=1)

# Time pressure versions
yuanxia_dsc_onecut15 = yuanxia_dsc_onecut[yuanxia_dsc['time_pressure'] == 15]
yuanxia_gtc_onecut15 = yuanxia_gtc_onecut[yuanxia_gtc['time_pressure'] == 15]
yuanxia_dsc_onecut25 = yuanxia_dsc_onecut[yuanxia_dsc['time_pressure'] == 25]
yuanxia_gtc_onecut25 = yuanxia_gtc_onecut[yuanxia_gtc['time_pressure'] == 25]
yuanxia_dsc_onecut40 = yuanxia_dsc_onecut[yuanxia_dsc['time_pressure'] == 40]
yuanxia_gtc_onecut40 = yuanxia_gtc_onecut[yuanxia_gtc['time_pressure'] == 40]

print('Stats for OneCut segmentation')
print('Rau\'s strokes:')
print_mean_median(rau_dsc_strokes_onecut, 'dsc', dilation_radii)
print_mean_median(rau_gtc_strokes_onecut, 'gtc', dilation_radii)
print_wilcoxon(rau_dsc_strokes_onecut, 'dsc', 0, 4)
print_wilcoxon(rau_gtc_strokes_onecut, 'gtc', 0, 4)
print_pop_normality(rau_dsc_strokes_onecut, 'dsc')
print_pop_normality(rau_gtc_strokes_onecut, 'gtc')
print_friedman(rau_dsc_strokes_onecut, 'dsc', dilation_radii)
print_friedman(rau_gtc_strokes_onecut, 'gtc', dilation_radii)

print('\nRau\'s points:')
print_mean_median(rau_dsc_points_onecut, 'dsc', dilation_radii)
print_mean_median(rau_gtc_points_onecut, 'gtc', dilation_radii)
print_wilcoxon(rau_dsc_points_onecut, 'dsc', 0, 4)
print_wilcoxon(rau_gtc_points_onecut, 'gtc', 0, 4)
print_pop_normality(rau_dsc_points_onecut, 'dsc')
print_pop_normality(rau_gtc_points_onecut, 'gtc')
print_friedman(rau_dsc_points_onecut, 'dsc', dilation_radii)
print_friedman(rau_gtc_points_onecut, 'gtc', dilation_radii)

print('\nYuaxia\'s points (time pressure 15):')
print_mean_median(yuanxia_dsc_onecut15, 'dsc', dilation_radii)
print_mean_median(yuanxia_gtc_onecut15, 'gtc', dilation_radii)
print_wilcoxon(yuanxia_dsc_onecut15, 'dsc', 0, 4)
print_wilcoxon(yuanxia_gtc_onecut15, 'gtc', 0, 4)
print_pop_normality(yuanxia_dsc_onecut15, 'dsc')
print_pop_normality(yuanxia_gtc_onecut15, 'gtc')
print_friedman(yuanxia_dsc_onecut15, 'dsc', dilation_radii)
print_friedman(yuanxia_gtc_onecut15, 'gtc', dilation_radii)

print('\nYuaxia\'s points (time pressure 25):')
print_mean_median(yuanxia_dsc_onecut25, 'dsc', dilation_radii)
print_mean_median(yuanxia_gtc_onecut25, 'gtc', dilation_radii)
print_wilcoxon(yuanxia_dsc_onecut25, 'dsc', 0, 4)
print_wilcoxon(yuanxia_gtc_onecut25, 'gtc', 0, 4)
print_pop_normality(yuanxia_dsc_onecut25, 'dsc')
print_pop_normality(yuanxia_gtc_onecut25, 'gtc')
print_friedman(yuanxia_dsc_onecut25, 'dsc', dilation_radii)
print_friedman(yuanxia_gtc_onecut25, 'gtc', dilation_radii)

print('\nYuaxia\'s points (time pressure 40):')
print_mean_median(yuanxia_dsc_onecut40, 'dsc', dilation_radii)
print_mean_median(yuanxia_gtc_onecut40, 'gtc', dilation_radii)
print_wilcoxon(yuanxia_dsc_onecut40, 'dsc', 0, 4)
print_wilcoxon(yuanxia_gtc_onecut40, 'gtc', 0, 4)
print_pop_normality(yuanxia_dsc_onecut40, 'dsc')
print_pop_normality(yuanxia_gtc_onecut40, 'gtc')
print_friedman(yuanxia_dsc_onecut40, 'dsc', dilation_radii)
print_friedman(yuanxia_gtc_onecut40, 'gtc', dilation_radii)