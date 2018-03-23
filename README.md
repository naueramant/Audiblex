# Audiblex
Audible aax audiobook to M4A, M4B and MP4 converter.

It works by extracting the audiobook checksum, looking up it's activation bits in a rainbow table and converting the to the specified format.

## Platform
The script is only tested on Linux. It will properly work on OSX and properly not on Windows..

## Requirements
* Python 3
* [ffmpeg](https://ffmpeg.org/) for converting

## Usage
```shell
positional arguments:
  file                  The aax file to convert

optional arguments:
  -h, --help            show this help message and exit
  -t TYPE, --type TYPE  The destination filetype M4B, M4A or MP3
  -a ACTIVATION, --activation ACTIVATION
                        Define the activation bits to use
  -s, --single          Convert to a single file
  -l, --lookup          Lookup the activation bits in the rainbow table
  -c, --clear           Clear the activation bits cache
```

## Thanks to
[r15ch13](https://github.com/r15ch13/audible-converter) for the rainbow table and [jostyee](https://github.com/jostyee/AAXtoM4B) for the file converters.