# A study in the effects of stroke radius on semi-automatic image segmentation
This is the code for a study that was aimed at determining if the width of strokes in a label image
had significant impact on the resulting segmentation's accuracy and reproducibility.

## Study data
The data from this study comes from two previous studies, run by Steven Rau and Yuanxia Li. These
studies used images from the [Berkeley Segmentation Data Set and Benchmarks 500 image set](
https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/resources.html). They then
created label images for where participants labeled given areas of the image as foreground or background.
These label images are then used by semi-automatic image segmentation algorithms (as seed points)
to assist with segmentation. One study used points in addition to strokes.

The study data must be downloaded separately (due to being large and having many files). See the
releases in this repo to download.

## Explaining this repo
The files in this repo require some explanation, as there's no obvious point to dive in. The files
are mostly stand alone scripts that each perform a specialized task. These can be run sequentially
to build up all the data and results of the study, but there's some caveats.

1. `dilate.py`: This script contains the functionality to dilate a single image. There's two methods
of dilation. One is straightforward and the other avoid introducing *new* errors over the ground truth.
Which is arguably cheat-y since it requires knowing the ground truth, but it's used with the assumption
that users would be less likely to make such mistakes if they could visually see the dilation.

2. `run_dilation.py`: This file dilates all the label images, creating new images for each dilation
radius. The output folders for this need to exist. This won't overwrite files, so if you need to start
from scratch, delete the old output files.

3. `segment.py`: This file runs the segmentation programs (located in the `segmentation_programs`
folder) on all dilated images, producing a binary segmentated image for each dilated label image.
This file has a catch, and that's that one segmentation program is a Linux binary and the other is
a Windows binary. Hence, the script has a switch to flip depending on which segmentation program you
want to run. This also means you'd have to run this on two different OSes to get all the files. This
can take a while to run. The output folders for this need to exist. This also doesn't overwrite files.
Note the hardcoded foreground label of 29 and background label of 149.

4. `analysis.py`: This script performs an analysis of Dice Similarity Coefficient (DSC) and
Generalized Tanimoto Coefficient (GTC) for each image. This measures accuracy and reproducibility of
segmentation, respectively. The input and output folders need to exist (but need not contain files).
The results are placed in the analysis folder (which will be created if it doesn't already exist).
This is the only output that isn't placed with the data, as it's tab delimited files and not images.

5. `stats.py`: This script interprets the analysis files and comes up with various statistics, including
the means and medians of measures for each study, Wilicoxon test, normality test, and Friedman chi
test. The result is printed to the console.

## The image data folders
Not in this repo, but included with the releases is the image data, which has a certain organization.
Firstly, things are divided into the `rau` and `yuanxia` folders, splitting by study.

* `rau/originals` - colour originals (as JPG)
* `rau/ground_truth` - binary ground truths (as PNG)
* `rau/points` - User label images where the user entered points (as TIF)
* `rau/strokes` - User label images where the user entered strokes (as TIF)
* `rau/dilated_points` - The dilated versions of the files in `rau/points` (rest as PNG)
* `rau/dilated_strokes` - The dilated versions of the files in `rau/strokes`
* `rau/segmented_points` - The Boykov segmented versions of the files in `rau/dilated_points`
* `rau/segmented_strokes` - The Boykov segmented versions of the files in `rau/dilated_strokes`
* `rau/segmented_points_onecut` - The OneCut segmented versions of the files in `rau/dilated_points`
* `rau/segmented_strokes_onecut` - The OneCut segmented versions of the files in `rau/dilated_strokes`
* `yuanxia/originals` - colour originals (as JPG)
* `yuanxia/ground_truth` - binary ground truths (as PNG)
* `yuanxia/points` - User label images where the user entered points (as PNG)
* `yuanxia/dilated` - The dilated versions of the files in `yuanxia/points` (rest as PNG)
* `yuanxia/segmented` - The Boykov segmented versions of the files in `rau/dilated`
* `yuanxia/segmented_onecut` - The OneCut segmented versions of the files in `rau/dilated`

These folders also have scripts that were used to move the files into the structures from the format
they were provided in from Dr Mark Eramian (that is, from the format the study authors had them in).
The files have a consistent and flat naming scheme:

    <user id>-<file id>-<time pressure>-<dilation radius>-<type>.png

* `<user id>` - A numeric ID given to the user. Note that not all user IDs were used.
* `<file id>` - The ID of the file in the BSDS 500.
* `<time pressure>` - Number of seconds that users had to complete the segmentation. Only used in
the Yuanxia study.
* `<dilation radius>` - The radius, in pixels, that the image was dilated.
* `<type>` - An internal classification of the type of the image, such as `point`, `segmented`, `dilate`,
etc.

Attributes are excluded where they don't exist. Eg, a dilated image in the Rau study might have a file
name like `1-6046-3-dilate.png`. That fits the pattern `<user id>-<file id>-<dilation radius>-<type>.png`.
The originals just have a file ID. Ground truths are named `<file id>-GT.png`. These IDs are used
consistently throughout the study.

## Segmentation programs
This study uses two segmentation programs. One which was created by Dr Mark Eramian utilizing a
[graph cut algorithm from Boykov](http://vision.csd.uwo.ca/code/#Max-flow.2Fmin-cut). The other
algorithm utilizes the [One Cut Algorithm implemented by Lena Gorelick](http://vision.csd.uwo.ca/code/#OneCut_with_Seeds).
That executable is actually a modified version [of my own](https://github.com/KatrinaHoffert/OneCut-cli).

## Licensing
The images are all public domain. The segmentation programs have their own licenses that must be
considered separately. Finally, the various python files are my work and licensed under the
BSD license:

    Copyright (c) 2017, Katrina Hoffert
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this
       list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
