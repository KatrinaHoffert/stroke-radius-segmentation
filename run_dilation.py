import os, re, sys, enum
from dilate import no_error_dilate

class Study(enum.Enum):
    Rau = 1
    Yuanxia = 2

def dilate(study, strokes_loc, ground_truth_loc, output_loc, radius_range):
    '''
    Dilates all files.

    study: The Study used, which determines naming scheme.
    strokes_loc: Folder location for where the stroke files are.
    ground_truth_loc: Folder location for where the ground truth files are.
    output_loc: Folder location to save the dilated files in.
    radius_range: A generator yielding the radiuses to dilate each image for.
    '''
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

        # Run the dilation for all files with all dilation radius values
        for radius in radius_range:
            i += 1
            print('\rProcessing file', i, 'of', len(files) * len(radius_range), end='')
            sys.stdout.flush()

            background_label = 149
            foreground_label = 29
            input_image = strokes_loc + '/' + file
            ground_truth_image = ground_truth_loc + '/' + file_id + '-GT.png'

            if study == Study.Rau:
                output_image = output_loc + '/' + participant_id + '-' + file_id + '-' + str(radius)  + '-dilate.png'
            else:
                output_image = output_loc + '/' + participant_id + '-' + file_id + '-' + time_pressure + '-' + str(radius)  + '-dilate.png'

            # Skip files that have already been dilated
            if os.path.exists(output_image): continue

            no_error_dilate(input_image, ground_truth_image, output_image, radius, foreground_label, background_label)

print('Processing Rau\'s strokes')
dilate(Study.Rau, './rau/strokes', './rau/ground_truth', './rau/dilated_strokes', range(0, 5))

print('\nProcessing Rau\'s points')
dilate(Study.Rau, './rau/points', './rau/ground_truth', './rau/dilated_points', range(0, 5))

print('\nProcessing Yuanxia\'s points')
dilate(Study.Yuanxia, './yuanxia/points', './yuanxia/ground_truth', './yuanxia/dilated', range(0, 5))
print()