import os, sys
import glob
import shutil
import re
from PIL import Image
import numpy as np

from pdf2image import convert_from_path
#import fitz
from pdfrw import PdfReader

import pdf_compressor as pc

import site
site.addsitedir(r"...pathToPDFTron\PDFNetWrappersWin32\PDFNetC\Lib")


# use package \RequirePackage{snapshot} in you latex sources in order to generate a *.dep file with all the dependencies
# https://tex.stackexchange.com/questions/24542/create-list-of-all-external-files-used-by-master-latex-document


COMPRESS_IMAGES = True
COMPRESS_PDFS = True


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

    if lineCtr == 283:
        tmp = 5

    if t >= 0:
        fileName = line[t + 7:]
        start = fileName.find('{')
        end = fileName.find('}')

        fileName = fileName[start+1:end]

        src = root + '/' + fileName
        dst = destFolder + '/' + fileName

        # sometimes syte files aren't copied as they are missing file extensions in the dep file

        # if ~os.path.isfile(src):
        #     tmp = 5
        #
        #     for file in os.listdir(src):
        #         if file.endswith(".tex"):
        #             src += ".tex"
        #             dst += ".tex"


        try:
            mkdirs(os.path.dirname(dst), mode=0o777)
            shutil.copyfile(src, dst)
            continue
        except:
            print('Error')

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

            # check number of image pixels and reduce in case of too large
            nmbImagePixelsSrc = image.size[0] * image.size[0]
            nmbImagePixelsTarget = 2000000
            if (nmbImagePixelsSrc > nmbImagePixelsTarget):
                image.thumbnail( ( image.width * nmbImagePixelsTarget / nmbImagePixelsSrc, image.height * nmbImagePixelsTarget / nmbImagePixelsSrc), Image.ANTIALIAS)

            #image.save(f,quality=10,optimize=True)
            image.save(f)



if COMPRESS_PDFS:
    print("Starting pdf compression")
    # reduce pdf file size
    # use pdf compressor from https://github.com/theeko74/pdfc?tab=readme-ov-file
    # 1) install ghostscript
    # 2) download the project and copy the "pdf_compressor.py" to this folder
    types = "*.pdf"
    imageFiles = []

    imageFiles = [f for f in glob.glob(destFolder + "/**/" + types, recursive=True)]
    fileCntr = 0
    for f in imageFiles:
        fileCntr+=1
        print("Progress: " + str( fileCntr/len(imageFiles) * 100) + "%")

        f_out_0 = f[0:-4] + "_red_0.pdf"
        f_out_1 = f[0:-4] + "_red_1.pdf"
        f_out_2 = f[0:-4] + "_red_2.pdf"

        fileNameArray = [f_out_0, f_out_1, f_out_2]

        pc.compress(f, f_out_1, 2)

        # check if file size is under certain limit, otherwise try compression via PDF->PNG->PDF conversion
        fileSize_uncompressed = os.path.getsize(f)
        fileSize_compression_method_1 = os.path.getsize(f_out_1)
        if fileSize_compression_method_1 > 0 * 1e6:

            # extract pdf page size
            # see https://stackoverflow.com/questions/6230752/extracting-page-sizes-from-pdf-in-python
            #doc = fitz.open(f)
            #page = doc[0]
            #print(page.rect.width, page.rect.height)




            pages = convert_from_path(f, 500)
            pages[0].save( f_out_2, "PDF", resolution=100.0, save_all=True, append_images=pages[1:] )

            pdf = PdfReader(f)
            pdf2 = PdfReader(f_out_2)

            # pdf paper dimension correction
            origWidth = float(pdf.pages[0].MediaBox[2])
            newWidth = float(pdf2.pages[0].MediaBox[2])
            widthCorrectionFactor = newWidth / origWidth * 100

            pages[0].save(f_out_2, "PDF", resolution=widthCorrectionFactor, save_all=True, append_images=pages[1:])



            # when original compression method has less file size than image based compression method, use orogonal method, since it typically has better results
            #if fileSize_compression_method_2 >= fileSize_compression_method_1:
            #    pc.compress(f, f_out, 2)
            #tmp = 5

        fileSize_compression_method_2 = os.path.getsize(f_out_2)
        t = np.argmin( [fileSize_uncompressed, fileSize_compression_method_1, fileSize_compression_method_2] )

        shutil.copyfile(f, f_out_0)

        # delete old file
        os.remove(f)

        # copy new file
        shutil.copyfile(fileNameArray[t], f)

        # rename new file
        #os.rename(f_out, f, src_dir_fd=None, dst_dir_fd=None)

        for i in range(3):
            os.remove(fileNameArray[i])








