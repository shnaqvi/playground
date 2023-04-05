import json, sys, os, re
import numpy as np

def pos_to_label(positions, join_char=''):
    if isinstance(positions, dict):
        return join_char.join(["{0}{1}{2}".format(key, ('n', 'p')[value >= 0], abs(value)) for key, value in positions.items()])
    elif all(isinstance(item, tuple) for item in positions):
        return join_char.join(["{0}{1}{2}".format(key, ('n', 'p')[value >= 0], abs(value)) for key, value in positions])
    elif isinstance(positions, list) or isinstance(positions, set):
        return join_char.join(["{0}{1}".format(('n', 'p')[value >= 0], abs(value)) for value in positions])
    else:
        raise Exception("Expected a dict or list/set of 3 xyz name-value tuples e.g. [('x',1), ...], or list of 3 xyz positions e.g. [1,2,3]")


if __name__ == "__main__":
    # Load FATP sequence file and change folder names
    sequence_pevt = json.load(open('/Volumes/flamingo_data-1/_Salman/_calibration/Jan23_loft/sequence-dense-pevt.json'))
    positions = sequence_pevt['positions']
    for i, pos in enumerate(positions):
        positions[i][4] = re.sub('NEMOL/', 'l-', pos[4])
        positions[i][5] = ''
        # positions[i][:3] = (np.array(pos[:3]) * np.array([-1, -1, 1])).tolist()

    sequence_sparse = json.load(open('/Volumes/flamingo_data-1/_Salman/_calibration/Jan23_loft/sequence-sparse.json'))
    sequence_sparse['positions'] = positions
    json.dump(sequence_sparse, open('/Volumes/flamingo_data-1/_Salman/_calibration/Jan23_loft//sequence-dense.json', 'w'),
              indent=4, separators=(',', ': '))


    # # Load sequence file and change pattern numbers
    # sequence = json.load(open('/Volumes/flamingo_data-1/_Salman/_calibration/Jan23_loft/dataset_feb24/p0p0p0_p0p0p0/captures/sequence.json'))
    # positions = sequence['positions']
    # for i, pos in enumerate(positions):
    #     positions[i][3] = 1
    # sequence['positions'] = positions
    # json.dump(sequence, open('/Volumes/flamingo_data-1/_Salman/_calibration/Jan23_loft/dataset_feb24/p0p0p0_p0p0p0/captures/sequence.json', 'w'),
    #           indent=4, separators=(',', ': '))
