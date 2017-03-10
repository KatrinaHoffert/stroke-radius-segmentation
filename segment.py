'''
Runs the segmentation program on all images, resulting in the creation of
binary segmentation images.
'''

import os, re, sys, subprocess
from common import Study

# The Boykov segmentation program is only currently available as a Linux binary,
# but the OneCut segmentation program is only currently available as a Windows
# binary, so we have to flip by platform what we run...
platform = "windows"

def segment(study, originals_loc, strokes_loc, output_loc, run_segmentation_code):
    '''
    Segments images using the segmenation program.

    study: The Study used, which determines naming scheme.
    originals_loc: Folder that the original files are in.
    strokes_loc: Folder that the stroke/point annoted files are in.
    output_loc: Folder that the output files should be placed in.
    run_segmentation_code: Lambda that runs the actual segmentation program. Is
    given the file ID, the path to the original image, the path to the strokes file,
    an output folder, and a calculated output file name.
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

        run_segmentation_code(file_id, original_image, stroke_image, output_loc, output_image)

def run_boykov_segmentation(file_id, original_image, stroke_image, output_loc, output_image):
    # Note: Python 3.5+ this method is called "run"
    subprocess.call(['./segmentation_programs/BoykovMaxFlowGeneric', '--strokefglabel=29',
        '--strokebglabel=149', '--outputdir=' + output_loc, original_image, stroke_image])

    # Now move the created file to the right name and remove the contour file
    created_file_base = output_loc + '/' + file_id + '.jpg'
    os.rename(created_file_base + '.segmentation.tif', output_image)
    os.remove(created_file_base + '.contours.tif')

def run_onecut_segmentation(file_id, original_image, stroke_image, output_loc, output_image):
    # Note: Python 3.5+ this method is called "run"
    subprocess.call(['./segmentation_programs/OneCut', original_image, stroke_image,
        '--fg-label', '29', '--bg-label', '149', '--output', output_image], stdout=subprocess.DEVNULL)

if platform == "linux":
    print('Segmenting with Boykov\'s graph cut:')
    print('Processing Rau\'s strokes')
    segment(Study.Rau, './rau/originals', './rau/dilated_strokes', './rau/segmented_strokes', run_boykov_segmentation)

    print('\nProcessing Rau\'s points')
    segment(Study.Rau, './rau/originals', './rau/dilated_points', './rau/segmented_points', run_boykov_segmentation)

    print('\nProcessing Yuanxia\'s strokes')
    segment(Study.Yuanxia, './yuanxia/originals', './yuanxia/dilated', './yuanxia/segmented', run_boykov_segmentation)
    print()
else:
    print('Segmenting with OneCut:')
    print('Processing Rau\'s strokes')
    segment(Study.Rau, './rau/originals', './rau/dilated_strokes', './rau/segmented_strokes_onecut', run_onecut_segmentation)

    print('\nProcessing Rau\'s points')
    segment(Study.Rau, './rau/originals', './rau/dilated_points', './rau/segmented_points_onecut', run_onecut_segmentation)

    print('\nProcessing Yuanxia\'s strokes')
    segment(Study.Yuanxia, './yuanxia/originals', './yuanxia/dilated', './yuanxia/segmented_onecut', run_onecut_segmentation)
    print()