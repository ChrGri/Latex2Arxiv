# Latex2Arxiv

Submitting preprints to arXiv requires submission of the LaTeX sources. This python code will create a copy of your existing document directory and will generate a copy with only the dependencies in it. Furthermore, comments in the latex sources will be delted in the copy. 


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
root = 'C:/Data/SVN_Checkouts/Paper_Lidar2Radar'
destFolder = root + '_reduced'
texFileName = 'bare_jrnl.tex'
depFileName = root + '/' + texFileName[:-4] + '.dep'
```



