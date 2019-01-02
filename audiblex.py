#!/usr/bin/env python3

import argparse, subprocess, os, re, csv
from shutil import which
from enum import Enum

class Colors:
    BLUE   = '\033[94m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    FAIL   = '\033[91m'
    ENDC   = '\033[0m'

class Filetypes(Enum):
    M4B = 'M4B'
    M4A = 'M4A'
    MP3 = 'MP3'

cach_path = '/tmp/audiblex_cache'

sp = os.path.dirname(os.path.realpath(__file__))

def decrypt(filepath: str):
    with open(filepath, 'rb') as f:
        f.seek(653)
        checksum = f.read(20).hex()

        print(Colors.BLUE + '::' + Colors.ENDC, 'Audio book checksum:', checksum)
        print(Colors.BLUE + '::' + Colors.ENDC, 'Looking up activation bits for checksum...')

        cache = loadCache()
        cache_bits = cache.get(checksum, None)

        if cache_bits: 
            print(Colors.BLUE + '::' + Colors.ENDC, 'Activation bits in cache')
            return cache_bits

        process = subprocess.Popen(['./rcrack', 'tables', '-h', checksum], cwd=os.path.join(sp, 'bin/rcrack'), stdout=subprocess.PIPE)
        result = process.communicate()[0].decode('UTF-8')
        result = re.search(r'hex:([a-fA-F0-9]{8})', result)

        if result:
            bits = result.groups()[0]
            cache[checksum] = bits
            saveCache(cache)      

            return bits 
        else:
            return None

def convert(type: Filetypes, activation: str, filepath: str, single: bool):
    print(Colors.BLUE + '::' + Colors.ENDC, 'Starting to convert the audio book')

    cargs = [os.path.join(sp, 'bin/converters/AAXto' + type.value), activation, filepath];
    if single: args.append('--single')

    subprocess.run(cargs, stdout=subprocess.PIPE)

def loadCache():
    try:
        reader = csv.reader(open(cach_path, 'r'))
        return {rows[0]:rows[1] for rows in reader}
    except:
        return {}

def saveCache(ab: dict):
    try:
        writer = csv.writer(open(cach_path, 'w'))
        {writer.writerow([key, val]) for key, val in ab.items()}
    except:
        print(Colors.FAIL + '::' + Colors.ENDC, 'Faild to save activation bits cache')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert audible AAX files to M4B, M4A or MP4')
    parser.add_argument('file', help='The aax file to convert')
    parser.add_argument('-t', '--type', help='The destination filetype M4B, M4A or MP3', type=Filetypes)
    parser.add_argument('-a', '--activation', help='Define the activation bits to use')
    parser.add_argument('-s', '--single', help='Convert to a single file', action='store_true')
    parser.add_argument('-l', '--lookup', help='Lookup the activation bits in the rainbow table', action='store_true')
    parser.add_argument('-c', '--clear', help='Clear the activation bits cache', action='store_true')

    args = parser.parse_args()

    try:
        if not which('ffmpeg'):
            print(Colors.FAIL + '::' + Colors.ENDC, 'ffmpeg not found, not installed?')  
            exit(1)

        if args.clear:
            saveCache({})

        activation_bits = args.activation if args.activation and not args.lookup else decrypt(args.file)

        if len(activation_bits) != 8:
            print(Colors.FAIL + '::' + Colors.ENDC, 'Activation bits must be exactly 8 characters long')
        else:
            if activation_bits:
                print(Colors.GREEN + '::' + Colors.ENDC, 'Activation bits found:', activation_bits)

                if not args.lookup:
                    ftype = args.type if args.type else Filetypes.M4B
                    convert(ftype, activation_bits, args.file, args.single)
            else:
                print(Colors.FAIL + '::' + Colors.ENDC, 'Failed to find activation bits')  

    except FileNotFoundError as e:
        print(Colors.FAIL + '::' + Colors.ENDC, 'No such file:', '\'' + args.file + '\'')
    except:
        pass
