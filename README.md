# Latex2Arxiv

Submitting preprints to arXiv requires submission of the LaTeX sources. This python code will create a copy of your existing document containing only the necessary depenedencies to build the project. Furthermore, comments in the latex sources will be deleted in the copy. 


### Prerequisites in the latex main document
In order to read the dependencies, you need to add the Snapshot package to you latex main document.
```
\RequirePackage{snapshot}
```
After compiling your latex document a new *.dep file should have been created listing all the dependencies.

### Prerequisites in the latex main document
In the main.py document you need to parametrize 

* the source directory
* the destination directory
* the name of the main latex document.
```
root = 'C:/Data/SOURCE_DIRECTORY'
destFolder = root + '_reduced'
texFileName = 'bare_jrnl.tex'
depFileName = root + '/' + texFileName[:-4] + '.dep'
```


### Additional operation
Python code to reduce file size of all images in the destination directory has been added to the main.py file. This file compression has been deactivated by default and must be activated by removing the line comments:

```
# find all image files in directory and subdirectories
types = ('*.png', '*.jpg')
imageFiles = []
for files in types:
    imageFiles = [f for f in glob.glob(destFolder + "/**/" + files, recursive=True)]
    for f in imageFiles:
        #b = f.objects.get(title='Into the wild')
        image = Image.open(f)
        image.save(f,quality=10,optimize=True)
```






