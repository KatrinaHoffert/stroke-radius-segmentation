'''
Runs the segmentation program on all images, resulting in the creation of
binary segmentation images.
'''

import os, re, sys, subprocess
from common import Study

def segment(study, originals_loc, strokes_loc, output_loc, segmentation_program):
    '''
    Segments images using the segmenation program.

    study: The Study used, which determines naming scheme.
    originals_loc: Folder that the original files are in.
    strokes_loc: Folder that the stroke/point annoted files are in.
    output_loc: Folder that the output files should be placed in.
    segmentation_program: The segmentation application that is run on each image.
    '''
    i = 0
    files = os.listdir(strokes_loc)
    for file in files:
        # Extract data from file name
        if study == Study.Rau:
            file_re = re.search('(\d+)-(\d+)-(\d+)', file)
        else:
            file_re = re.search('(\d+)-(\d+)-(\d+)-(\d+)', file)
        if file_re == None: continue

        participant_id = file_re.group(1)
        file_id = file_re.group(2)

        if study == Study.Rau:
            dilation_radius = file_re.group(3)
        else:
            time_pressure = file_re.group(3)
            dilation_radius = file_re.group(4)

        # For all files, determine paths and run through segmentation program
        i += 1
        print('\rProcessing file', i, 'of', len(files), end='')
        sys.stdout.flush()

        original_image = originals_loc + '/' + file_id + '.jpg'
        stroke_image = strokes_loc + '/' + file

        if study == Study.Rau:
            output_image = output_loc + '/' + participant_id + '-' + file_id + '-' + dilation_radius + '-segmented.png'
        else:
            output_image = output_loc + '/' + participant_id + '-' + file_id + '-' + time_pressure + '-' + dilation_radius + '-segmented.png'

        # Skip files that have already been segmented
        if os.path.exists(output_image): continue

        # Note: Python 3.5+ this method is called "run"
        subprocess.call([segmentation_program, '--strokefglabel=29', '--strokebglabel=149',
            '--outputdir=' + output_loc, original_image, stroke_image])

        # Now move the created file to the right name and remove the contour file
        created_file_base = output_loc + '/' + file_id + '.jpg'
        os.rename(created_file_base + '.segmentation.tif', output_image)
        os.remove(created_file_base + '.contours.tif')

print('Processing Rau\'s strokes')
segment(Study.Rau, './rau/originals', './rau/dilated_strokes', './rau/segmented_strokes', './BoykovMaxFlowGeneric')

print('\nProcessing Rau\'s points')
segment(Study.Rau, './rau/originals', './rau/dilated_points', './rau/segmented_points', './BoykovMaxFlowGeneric')

print('\nProcessing Yuanxia\'s strokes')
segment(Study.Yuanxia, './yuanxia/originals', './yuanxia/dilated', './yuanxia/segmented', '../BoykovMaxFlowGeneric')
print()