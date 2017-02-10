'''
This module contains common functionality that many of the other modules use.
'''

import enum

class Study(enum.Enum):
    '''
    Represents if the study is Rau's or Yuanxia's.
    '''
    Rau = 1
    Yuanxia = 2

# The dtypes are used so that numpy can read in the analysis files and understand
# their structure and how they're meant to be displayed. The names are the column
# names (which let us index by column in a readable way). The formats are the data
# types of the columns. The format string is the printf style character to use
# for formatting the output file (only used for sorting the files).
rau_dsc_dtype = {
    'names': ('participant_id', 'file_id', 'dilation_radius', 'dsc'),
    'formats': ('i4', 'i4', 'i4', 'f4'),
    'format_string': ['%d', '%d', '%d', '%f']
}
yuanxia_dsc_dtype = {
    'names': ('participant_id', 'file_id', 'time_pressure', 'dilation_radius', 'dsc'),
    'formats': ('i4', 'i4', 'i4', 'i4', 'f4'),
    'format_string': ['%d', '%d', '%d', '%d', '%f']
}
rau_gtc_dtype = {
    'names': ('file_id', 'dilation_radius', 'gtc'),
    'formats': ('i4', 'i4', 'f4'),
    'format_string': ['%d', '%d', '%f']
}
yuanxia_gtc_dtype = {
    'names': ('file_id', 'time_pressure', 'dilation_radius', 'gtc'),
    'formats': ('i4', 'i4', 'i4', 'f4'),
    'format_string': ['%d', '%d', '%d', '%f']
}

# The range of values to dilate.
dilation_radii = range(0, 5)