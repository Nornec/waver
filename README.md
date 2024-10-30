# waver
Turns a mono .wav file (or the left channel of a stereo .wav file) into raw data and chucks the percentage value of the data into a `.wtd` file. 
The `.wtd` file format is used specifically for Midinous to read in as a wavetable, but it is stored as encoded plain text

## `.wtd` format:
```
  line | description
     1 | wavetable name (alphanumeric only, starting with an alpha character or underscore)
     n | floating point wave data between -1 and 1, preferrably starting near 0 and ending near 0
```
I wrote this helper script so that I could generate unique or basic waves for use in Midinous without having to resort to doing wave math every cycle for unique non-basic waves

This script is otherwise very helpful for generating wavetables from a one-period wave file for use in audio engines.

I recommend feeding the script a .wav file with the maximum possible sample rate. 
When Wavetables are read, they will naturally alias, so the more samples you have available, the less of an impact the sample rate will have on the sampled input to the Midinous wavetable generator

# Requirements
- scipy
- pathlib
- python 3+ (probably, built on 3.12.7)
