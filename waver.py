#_____________
# DESCRIPTION |
#``````````````
# waver
# Turns a mono .wav file (or the left channel of a stereo .wav file) into raw data and chucks the percentage value of the data into a .wtd file. The .wtd file format is used specifically for Midinous to read in as a wavetable, but it is stored as encoded plain text
#
# .wtd format:
#  line | description
#     1 | wavetable name (alphanumeric only, starting with an alpha character or underscore)
#     n | floating point wave data between -1 and 1, preferrably starting near 0 and ending near 0
#
# I wrote this helper script so that I could generate unique or basic waves for use in Midinous without having to resort to doing wave math every cycle for unique non-basic waves
#
# This script is otherwise very helpful for generating wavetables from a one-period wave file for use in audio engines.
#
# I recommend feeding the script a .wav file with the maximum possible sample rate. When Wavetables are read, they will naturally alias, so the more samples you have available, the less of an impa
#________________________________
# Author: Jae "Nornec" Rin, 2024

#________________
# INITIALIZATION |
#`````````````````

import sys, warnings
from scipy.io import wavfile
from pathlib import Path

#_____________
# DEFINITIONS |
#``````````````

MAX_INT = 2147483647


#_________
# UTILITY |
#``````````

def get_pct(num: int) -> float:
    """ Function to return the percent value of an integer value
    """
    if num > 0:
        return num/MAX_INT
    elif num < 0:
        return num/(MAX_INT+1)
    else:
        return 0


#________
# TASKS  |
#`````````

def get_data_from_wav(f: Path, data: list) -> list:
    """ Get the raw data values from a wave file using scipy
    """
    # Sometimes, a .wav will have header information that can't be converted or read from in this way. Suppress those warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        _, data = wavfile.read(f)

    return data


def write_output(filename: str, wavename: str, data: list):
    """ Write data values to the output file, formatted for 8 decimal places, then close the file
    """
    out_file = open(filename, "w")
    out_file.write(f"{wavename}\n")
    line_count = 0
    for v in data:
        if line_count == len(data) - 1:
            out_file.write(f'{get_pct(v):.8f}')
            out_file.close()
            return
        else:
            out_file.write(f"{get_pct(v):.8f}\n")
        line_count += 1
    out_file.close()


def execute():
    """ Checks to see if the input waveform is a .wav, then proceeds with other functions
    """
    data = []

    input_filename_short = input("Input wave file name (short):")
    input_filename = f"./input/{input_filename_short}.wav"

    input_path = Path(input_filename)
    if not input_path.is_file():
        print("Input file doesn't exist or format is not a .wav")
        sys.exit()
    else:
        data = get_data_from_wav(input_path, data)

    wavetable_name = input("Wavetable name:")
    while wavetable_name.strip()[0].isdigit():
        print("First character of wavetable name should be a letter...\n")
        wavetable_name = input("Wavetable name:")
    wavetable_name = wavetable_name.strip()
    wavetable_name = wavetable_name.replace(" ", "_")

    output_filename = f"./output/{input_filename_short}.wtd"

    write_output(output_filename, wavetable_name, data)
    print(f"Done! Find your file in the output directory: {output_filename}")


#_______
# MAIN |
#```````

if __name__ == "__main__":
    execute()
