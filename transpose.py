import sys
import pdb
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def transpose_input(f, out = None, reading_offset = 25):
    '''
    Transposes some kinda lame science data into some other kind of lame science data

    Parameters
    ----------
    f : string
        Path to csv file
    reading_offset : float, optional
        constant value to add to all Reading values. Defaults to 25
    out  : string
        Path to transposed output file. Defaults to None, in which case
        the new file name is identical to the input, with "_transposed"
        appended to the end
    '''


    # read excel file, strip header, and set first row as column names
    print('reading input at {}'.format(f))
    data = pd.ExcelFile(f).parse().tail(-6)
    data.columns = data.iloc[0].tolist()
    data = data.drop(data.index[0])
    print('foud {} cols, {} rows'.format(data.shape[1], data.shape[0]))

    # replace NaN's with zeros, and populate nupy arrays
    data['ROX'] = data['ROX'].fillna(0)
    rox = data['ROX'].values
    reading = data['Reading '].values + reading_offset
    well = data['Well'].values
    
    # get transposed column names
    well2d = well.reshape(70, 96)
    columns = np.hstack([['Reading'], well2d[0]])

    # get ROX values, append each row with the corresponding Reading
    print('transposing values')
    rox2d = rox.reshape(70, 96)
    reading_rox = np.zeros((70, 97))
    for i in range(len(rox2d)): 
        reading_rox[i] = np.hstack([[reading[i*96]], rox2d[i]])

    # output to xlsx
    if(out is None): out_file = '{}_transposed.xlsx'.format(f.split('.')[-2])
    else : out_file = f
    print('writing out at {}'.format(out_file))
    out_data = pd.DataFrame(reading_rox, columns=columns)
    out_data.to_excel(out_file, index=False)


if __name__ == '__main__':
   
    # usage: python transpose.py {input filename} {reading offset} {output filename}
    out, reading_offset = None, 25 
    f = sys.argv[1]
    if(len(sys.argv) == 3): reading_offset = float(sys.argv[3])
    if(len(sys.argv) == 4): out = sys.argv[2]
    transpose_input(f, out, reading_offset)
    




