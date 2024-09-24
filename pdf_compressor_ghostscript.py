import os, sys
import glob
import shutil
import re
from PIL import Image
import numpy as np

# install pdf2image https://pypi.org/project/pdf2image/
from pdf2image import convert_from_path
#import fitz
from pdfrw import PdfReader

import pdf_compressor as pc

import site
site.addsitedir(r"...pathToPDFTron\PDFNetWrappersWin32\PDFNetC\Lib")

COMPRESS_PDFS = True

if COMPRESS_PDFS:

    f = "C:\Data\Paper_in.pdf"
    f_out_1 = "C:\Data\Paper_in.pdf"



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




        pages = convert_from_path(f, 800)
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







