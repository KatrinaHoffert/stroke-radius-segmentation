'''
Counts how many images would differ from textbook_dilation.
'''

import os, re, sys, enum
from dilate import check_no_error_dilate
from common import Study

def error_count(study, strokes_loc, ground_truth_loc):
    '''
    Dilates all files.

    study: The Study used, which determines naming scheme.
    strokes_loc: Folder location for where the stroke files are.
    ground_truth_loc: Folder location for where the ground truth files are.
    output_loc: Folder location to save the dilated files in.
    '''
    num_errors = 0
    i = 0
    files = os.listdir(strokes_loc)
    for file in files:
        # Extract data from file name
        if study == Study.Rau:
            file_re = re.search('(\d+)-(\d+)', file)
        else:
            file_re = re.search('(\d+)-(\d+)-(\d+)', file)
        if file_re == None: continue

        participant_id = file_re.group(1)
        file_id = file_re.group(2)
        if study == Study.Yuanxia: time_pressure = file_re.group(3)

        i += 1
        print('\rProcessing file', i, 'of', len(files), end='')
        sys.stdout.flush()

        background_label = 149
        foreground_label = 29
        input_image = strokes_loc + '/' + file
        ground_truth_image = ground_truth_loc + '/' + file_id + '-GT.png'

        num_errors += int(check_no_error_dilate(input_image, ground_truth_image, foreground_label, background_label))

    print('\nFound', num_errors, 'files with errors in', i, 'files total')

print('Processing Rau\'s strokes')
error_count(Study.Rau, './rau/strokes', './rau/ground_truth')

print('\nProcessing Rau\'s points')
error_count(Study.Rau, './rau/points', './rau/ground_truth')

print('\nProcessing Yuanxia\'s points')
error_count(Study.Yuanxia, './yuanxia/points', './yuanxia/ground_truth')
print()