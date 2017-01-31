import numpy as np
import skimage.io, os, os.path, re, sys, enum, itertools
from common import Study

def gtc(files):
    '''
    Takes in a list of files to calculate the generalized tanimoto coefficient (GTC).
    The files must be binary images representing the same segmentation. There must be
    at least two files.

    The GTC is defined as the sum of the intersect over the sum of the union of all
    segmented areas.

    files: A list of files (as string paths) to calculate the GTC on.
    returns: generalized tanimoto coefficient for all files. Will be in range [0, 1],
    where 0 indicates no consistency in segmentations and 1 indicates perfect consistency.
    '''
    intersect_sum = 0
    union_sum = 0

    # Applies to all combinations pairs of files. This is the cleanest approach for
    # that as it lets us minimize loading without having to load everything at once.
    for i in range(len(files)):
        segmentation1 = skimage.io.imread(files[i]).astype('bool')
        for j in range(i+1, len(files)):
            segmentation2 = skimage.io.imread(files[j]).astype('bool')
            intersect_sum += np.sum(np.minimum(segmentation1, segmentation2))
            union_sum += np.sum(np.maximum(segmentation1, segmentation2))

    return intersect_sum / union_sum

def dsc(segmented_image, ground_truth_image):
    '''
    Calculates the Dice similarity coefficient (DSC) of an image.

    The DSC is defined as: (2 * | S intersect G |) / ( | S | + | G | )

    segmented_image: Path to the segmented image (must be binary).
    ground_truth_image: Path to that image's ground truth (must be binary).
    returns: The DSC of the segmented image.
    '''
    segmented_matrix = skimage.io.imread(segmented_image).astype('bool')
    ground_truth_matrix = skimage.io.imread(ground_truth_image).astype('bool')

    intersection = np.logical_and(segmented_matrix, ground_truth_matrix)
    area_segmented = np.sum(segmented_matrix)
    area_ground_truth = np.sum(ground_truth_matrix)
    area_intersect = np.sum(intersection)

    return 2 * area_intersect / (area_segmented + area_ground_truth)

def run_dsc(study, ground_truth_loc, segmented_loc, output_file):
    '''
    Calculates the DSC for all segmented files, spitting out a tab delimited file
    that contains all the file name columns and the GTC.

    study: The study that this is running on, so we can get the naming right.
    ground_truth_loc: Folder containing all the ground truth files.
    segmented_loc: Folder containing all the segmented files.
    output_file: The name of the output file to create.
    '''
    # Create output path if needed
    output_file_dirs = os.path.dirname(output_file)
    if not os.path.exists(output_file_dirs):
        os.makedirs(output_file_dirs)

    with open(output_file, 'w') as output:
        # Create header
        output.write('participant_id')
        output.write('\t')
        output.write('file_id')
        output.write('\t')
        if study == Study.Yuanxia:
            output.write('time_pressure')
            output.write('\t')
        output.write('dilation_radius')
        output.write('\t')
        output.write('dsc')
        output.write('\n')

        i = 0
        files = os.listdir(segmented_loc)
        for file in files:
            i += 1
            print('\rProcessing file', i, 'of', len(files), end='')
            sys.stdout.flush()

            # Extract data from file name
            if study == Study.Rau:
                file_re = re.search('(\d+)-(\d+)-(\d+)', file)
            else:
                file_re = re.search('(\d+)-(\d+)-(\d+)-(\d+)', file)
            if file_re == None: continue

            participant_id = file_re.group(1)
            file_id = file_re.group(2)
            if study == Study.Yuanxia:
                time_pressure = file_re.group(3)
                dilation_radius = file_re.group(4)
            else:
                dilation_radius = file_re.group(3)

            ground_truth_file = ground_truth_loc + '/' + file_id + '-GT.png'
            calculated_dsc = dsc(segmented_loc + '/' + file, ground_truth_file)

            output.write(participant_id)
            output.write('\t')
            output.write(file_id)
            output.write('\t')
            if study == Study.Yuanxia:
                output.write(time_pressure)
                output.write('\t')
            output.write(dilation_radius)
            output.write('\t')
            output.write(str(calculated_dsc))
            output.write('\n')

def run_gtc(study, segmented_loc, output_file):
    '''
    Creates a file with GTCs for each file ID (ie, each type of file) for each
    dilation radius. Compares across users.

    study: The study that this is running on, so we can get the naming right
    segmented_loc: Folder containing the segmented files. Should all be binary images.
    output_file: Where to place the output file, which will be tab delimited and
    contain the GTC for each file and dilation radius.
    '''
    # Create output path if needed
    output_file_dirs = os.path.dirname(output_file)
    if not os.path.exists(output_file_dirs):
        os.makedirs(output_file_dirs)

    # Figure out all pieces of info
    participant_ids = set()
    file_ids = set()
    time_pressures = set()
    dilation_radi = set()

    files = os.listdir(segmented_loc)
    for file in files:
        # Extract data from file name
        if study == Study.Rau:
            file_re = re.search('(\d+)-(\d+)-(\d+)', file)
        else:
            file_re = re.search('(\d+)-(\d+)-(\d+)-(\d+)', file)
        if file_re == None: continue

        participant_ids.add(file_re.group(1))
        file_ids.add(file_re.group(2))
        if study == Study.Yuanxia:
            time_pressures.add(file_re.group(3))
            dilation_radi.add(file_re.group(4))
        else:
            dilation_radi.add(file_re.group(3))

    # Now use the collected info so that we can group by the appropriate factors
    # (namely file ID and dilation radius -- might want to factor in time pressure
    # in the future).
    participant_ids = list(participant_ids)
    file_ids = list(file_ids)
    time_pressures = list(time_pressures)
    dilation_radi = list(dilation_radi)
    participant_ids = sorted(participant_ids, key=int)
    file_ids = sorted(file_ids, key=int)
    time_pressures = sorted(time_pressures, key=int)
    dilation_radi = sorted(dilation_radi, key=int)

    # Dummy value so that we can actually take the product of this
    if study == Study.Rau: time_pressures.insert(0, None)

    with open(output_file, 'w') as output:
        # Create header
        output.write('file_id')
        output.write('\t')
        if study == Study.Yuanxia:
            output.write('time_pressure')
            output.write('\t')
        output.write('dilation_radius')
        output.write('\t')
        output.write('gtc')
        output.write('\n')

        i = 0
        for file_id in file_ids:
            for dilation_radius in dilation_radi:
                for time_pressure in time_pressures:
                    file_list_for_gtc = []
                    for participant_id in participant_ids:
                        if time_pressure == None:
                            file_name = segmented_loc + '/' + participant_id + '-' + file_id + '-' + dilation_radius + '-segmented.png'
                        else:
                            file_name = segmented_loc + '/' + participant_id + '-' + file_id + '-' + time_pressure + '-' + dilation_radius + '-segmented.png'

                        # For the Yuanxia study, skip non-existant files (since they only exist for a
                        # certain time pressure)
                        if study == Study.Yuanxia and not os.path.exists(file_name): continue

                        file_list_for_gtc.insert(len(file_list_for_gtc), file_name)
                        i += 1

                    # Skip empty file lists for the Yuanxia study, since that occurs due to files not
                    # overlapping across time pressures
                    if study == Study.Yuanxia and len(file_list_for_gtc) == 0:
                        continue

                    print('\rProcessing file', i, 'of', len(files), end='')
                    sys.stdout.flush()
                    calculated_gtc = gtc(file_list_for_gtc)

                    output.write(file_id)
                    output.write('\t')
                    if study == Study.Yuanxia:
                        output.write(time_pressure)
                        output.write('\t')
                    output.write(dilation_radius)
                    output.write('\t')
                    output.write(str(calculated_gtc))
                    output.write('\n')

# Calculate all DSC
print('Processing Rau\'s strokes:')
run_dsc(Study.Rau, './rau/ground_truth', './rau/segmented_strokes', 'analysis/dsc/rau_strokes.txt')
run_gtc(Study.Rau, './rau/segmented_strokes', 'analysis/gtc/rau_strokes.txt')

print('\nProcessing Rau\'s points:')
run_dsc(Study.Rau, './rau/ground_truth', './rau/segmented_points', 'analysis/dsc/rau_points.txt')
run_gtc(Study.Rau, './rau/segmented_points', 'analysis/gtc/rau_points.txt')

print('\nProcessing Yuanxia\'s points:')
run_dsc(Study.Yuanxia, './yuanxia/ground_truth', './yuanxia/segmented', 'analysis/dsc/yuanxia.txt')
run_gtc(Study.Yuanxia, './yuanxia/segmented', 'analysis/gtc/yuanxia.txt')
