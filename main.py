import os, sys
import glob
import shutil
import re
from PIL import Image

# use package \RequirePackage{snapshot} in you latex sources in order to generate a *.dep file with all the dependencies
# https://tex.stackexchange.com/questions/24542/create-list-of-all-external-files-used-by-master-latex-document


# parametrization
root = 'C:/Data/SVN_Checkouts/Paper'
destFolder = root + '_reduced'
texFileName = 'bare_jrnl.tex'
depFileName = root + '/' + texFileName[:-4] + '.dep'

# create destination folder
def mkdirs(newdir,mode=777):
    try:
        os.makedirs(newdir, mode)
    except OSError as err:
        return err

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
for line in Lines:
    t = line.find('*{file}')
    if t >= 0:
        fileName = line[t + 7:]
        start = fileName.find('{')
        end = fileName.find('}')

        fileName = fileName[start+1:end]

        src = root + '/' + fileName
        dst = destFolder + '/' + fileName

        try:
            mkdirs(os.path.dirname(dst), mode=0o777)
            shutil.copyfile(src, dst)#
        except:
            print('Error')




# ToDo:
# remove comments from all tex files
# perform image compression

# find all image files in directory and subdirectories
# types = ('*.png', '*.jpg')
# imageFiles = []
# for files in types:
#     imageFiles = [f for f in glob.glob(destFolder + "/**/" + files, recursive=True)]
#     for f in imageFiles:
#         #b = f.objects.get(title='Into the wild')
#         image = Image.open(f)
#         image.save(f,quality=10,optimize=True)
#         tmp = 5






