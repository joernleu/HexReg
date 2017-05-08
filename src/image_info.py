#!/usr/bin/env python
# Get SEM image information, ResolutionX,ResolutionY, HFW, VFW, PixelWidth,PixelHeight 
def image_info(my_file):
    my_string1 = 'ResolutionX='
    my_string2 = 'ResolutionY='
    my_string3 = 'HFW='
    my_string4 = 'VFW='
    my_string5 = 'PixelWidth='
    my_string6 = 'PixelHeight='
    #infile = open(my_file).read()
    try:
        with open(my_file, errors="ignore") as infile:
            for line in infile:
                if my_string1 in line:
                    words = line.split('=')
                    ResX = int(words[1])
                elif my_string2 in line:
                    words = line.split('=')
                    ResY = int(words[1])
                elif my_string3 in line:
                    words = line.split('=')
                    HFW = float(words[1])
                elif my_string4 in line:
                    words = line.split('=')
                    VFW = float(words[1])
                elif my_string5 in line:
                    words = line.split('=')
                    PixelWidth = float(words[1])
                elif my_string6 in line:
                    words = line.split('=')
                    PixelHeight = float(words[1])
    except Exception:
        with open(my_file) as infile:
            for line in infile:
                if my_string1 in line:
                    words = line.split('=')
                    ResX = int(words[1])
                elif my_string2 in line:
                    words = line.split('=')
                    ResY = int(words[1])
                elif my_string3 in line:
                    words = line.split('=')
                    HFW = float(words[1])
                elif my_string4 in line:
                    words = line.split('=')
                    VFW = float(words[1])
                elif my_string5 in line:
                    words = line.split('=')
                    PixelWidth = float(words[1])
                elif my_string6 in line:
                    words = line.split('=')
                    PixelHeight = float(words[1])
        
        #infile.close()
    return ResX, ResY, HFW, VFW,PixelWidth,PixelHeight

if __name__ == '__main__':
    SEM_image = 'UTAM_test_image.TIF'
    info = SEM_image_info(SEM_image)
    print(info)
    