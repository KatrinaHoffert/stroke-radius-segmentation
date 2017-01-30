import numpy as np

def gtc(segs):
    '''
    segs is a list of 2d numpy arrays, each array is a boolean image of a segmentation
    returns: generalized tanimoto coefficient in [0, 1]
    '''
    min_sum = 0
    max_sum = 0

    for j in range(len(segs)):
        for k in range(j+1, len(segs)):
            min_sum = min_sum + np.sum(np.minimum(segs[j], segs[k]))
            max_sum = max_sum + np.sum(np.maximum(segs[j], segs[k]))

    return min_sum / max_sum

# DSC = (2 * | S \cap G |) / ( | S | + | G | )
def dsc():
    # This is the segmentation (boolean array)
    binary_segmentation = skimage.io.imread(os.path.join(bs_path, bs_file)).astype('bool')

    # This is ground truth (another boolean image)
    gt_segmentation = gt[orig_file[:-4] + '-GT.png']

    # Get their intersection
    intersection = np.logical_and(binary_segmentation, gt_segmentation )

    # Area
    area_bs = np.sum(binary_segmentation)
    area_gt = np.sum(gt_segmentation)
    area_intersect = np.sum(intersection)

    DSC = 2*area_intersect/(area_bs + area_gt)