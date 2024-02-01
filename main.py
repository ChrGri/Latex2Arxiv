import os, sys
import glob
import shutil
import re
from PIL import Image
import pdf_compressor as pc


# use package \RequirePackage{snapshot} in you latex sources in order to generate a *.dep file with all the dependencies
# https://tex.stackexchange.com/questions/24542/create-list-of-all-external-files-used-by-master-latex-document


COMPRESS_IMAGES = False
COMPRESS_PDFS = False


# parametrization
root = 'C:/Data/SOURCE_DIRECTORY'
destFolder = root + '_reduced'
texFileName = 'bare_jrnl.tex'
depFileName = root + '/' + texFileName[:-4] + '.dep'

# create destination folder
def mkdirs(newdir,mode=777):
    try:
        os.makedirs(newdir, mode)
    except OSError as err:
        return err


# remove target folder if exists
if os.path.exists(destFolder) and os.path.isdir(destFolder):
    shutil.rmtree(destFolder)

# make destination directory
mkdirs(destFolder,mode=0o777)

# copy tex file
src = root + '/' + texFileName
dst = destFolder + '/' + texFileName
shutil.copyfile(src, dst)

# remove comments from tex files
file1 = open(dst, 'r')
Lines = file1.readlines()
LinesClean = []
for line in Lines:

    matches = re.finditer('%', line)
    matches_positions = [match.start() for match in matches]

    # check whether match is a comment or not
    commentOccurance = len(line)
    for pos in reversed(matches_positions):

        if pos > 0:
            if line[pos-1] == '\\':
                # not a comment
                tmp = 5
            else:
                commentOccurance = pos
                continue
        else:
            commentOccurance = pos
            break

    if commentOccurance > 0:
        LinesClean.append(line[:commentOccurance])
outF = open(dst, "w")
for line in LinesClean:
    # write line to output file
    outF.write(line)
    #outF.write("\n")
outF.close()


# copy dependecies
file1 = open(depFileName, 'r')
Lines = file1.readlines()
lineCtr = 0
for line in Lines:
    t = line.find('*{file}')
    lineCtr+=1

    if lineCtr == 226:
        tmp = 5

    if t >= 0:
        fileName = line[t + 7:]
        start = fileName.find('{')
        end = fileName.find('}')

        fileName = fileName[start+1:end]

        src = root + '/' + fileName
        dst = destFolder + '/' + fileName

        # copy dependencies to dest folder
        try:
            mkdirs(os.path.dirname(dst), mode=0o777)
            shutil.copyfile(src, dst)
            continue
        except:
            print('Error')


        # sometimes syte files aren't copied as they are missing file extensions in the dep file
        # this was a good workaround so far
        try:
            src += ".tex"
            dst += ".tex"
            mkdirs(os.path.dirname(dst), mode=0o777)
            shutil.copyfile(src, dst)
            continue
        except:
            print('Error')








if COMPRESS_IMAGES:

    print("Starting image compression")
    # find all image files in directory and subdirectories
    types = ('*.png', '*.jpg')
    imageFiles = []
    for files in types:
        imageFiles = [f for f in glob.glob(destFolder + "/**/" + files, recursive=True)]
        for f in imageFiles:
            #b = f.objects.get(title='Into the wild')
            image = Image.open(f)
            image.save(f,quality=10,optimize=True)



if COMPRESS_PDFS:
    print("Starting pdf compression")
    # reduce pdf file size
    # use pdf compressor from https://github.com/theeko74/pdfc?tab=readme-ov-file
    # 1) Follow the installation instructions from aboves link
    # 2) download the project and copy the "pdf_compressor.py" to this folder
    types = "*.pdf"
    imageFiles = []

    imageFiles = [f for f in glob.glob(destFolder + "/**/" + types, recursive=True)]
    for f in imageFiles:

        f_out = f[0:-4] + "_red.pdf"
        pc.compress(f, f_out, 2 )

        # delete old file
        os.remove(f)

        # rename new file
        os.rename(f_out, f, src_dir_fd=None, dst_dir_fd=None)





