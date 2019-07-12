# Pipeline 

``` python 
 class Pipeline def setPrefix(self, prefix) 
```

Sets sufix to be added at the end of file names while storing.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         sufix | str |                 A sufix to be added to file names with modified images at                their ends. | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| setOutputFileType | Sets format of files for storing modified images. Must be jpg. | 
| setOutputPath | Sets path to a folder in which modifed images will be stored. | 
| addImage | Adds a raw image file to be proccessed to the pipeline. | 
| addInputFolder | Adds a folder with image files to be proccessed to the pipeline. | 
| add | Adds a filter/image process to the pipeline. | 
| setPipeline | Sets a sequence of filters/image processes to be applied to raw images. | 
| saveModified | Stores a modifed image in a file. | 
| show | Displays an image. | 
| process | Applies a seqence of filters/image processes defined with add() o. | 
| run | Applies a seqence of filters/image processes defined with add() o. | 
 
 

### setOutputFileType

``` python 
    setOutputFileType(fileType='jpg') 
```


Sets format of files for storing modified images. Must be jpg.

jpeg, png or tif.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         fileType | str |                 A str describing type of output format ("jpg", "jpeg",                "png" or "tif"). | 


### setOutputPath

``` python 
    setOutputPath(path) 
```


Sets path to a folder in which modifed images will be stored.

If the folder does not exist it will be created.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         path | str |                 The path to the output folder like r"~/path/to/output/folder" | 


### addImage

``` python 
    addImage(imagePath) 
```


Adds a raw image file to be proccessed to the pipeline.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         imagePath | str |                 The path to an image file like r"~/path/to/my/image.jpg" | 


### addInputFolder

``` python 
    addInputFolder(path) 
```


Adds a folder with image files to be proccessed to the pipeline.

Image files (jpg, jpeg, png or tif) are searched in the foder
and its subfolders.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         path | str |                 The path to image files like r"~/path/to/image/files" | 


### add

``` python 
    add(item) 
```


Adds a filter/image process to the pipeline.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         item | files.Filter |                 An instance of a filter class. For example Kernel(),                CLAHE() or Dehaze() etc. | 


### setPipeline

``` python 
    setPipeline(pipeline) 
```


Sets a sequence of filters/image processes to be applied to raw images.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         pipeline | list |                 A list of instances of a filter classes.                For example [Kernel(), CLAHE(), Dehaze()] etc. | 


### saveModified

``` python 
    saveModified(image, fileName) 
```


Stores a modifed image in a file.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         image | numpy.ndarray |                 A NumPy's array containing an image. | 
|         fileName | str |                 Name of the image file. | 


### show

``` python 
    show(image) 
```


Displays an image.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         image | numpy.ndarray |                 A NumPy's array containing an image. | 


### process

``` python 
    process(image, display_steps=False) 
```


Applies a seqence of filters/image processes defined with add() o.

setPipeline() to an image.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         image | numpy.ndarray |                 A NumPy's array containing an image. | 
|         display_steps | bool |                 If True image is displayed after each filter/image process                is applied. Default is False. | 


### run

``` python 
    run(save_files=True, display_steps=False, return_list=False) 
```


Applies a seqence of filters/image processes defined with add() o.

setPipeline() to images defined with addImage() or addInputFolder().

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         display_steps | bool |                 If True images are displayed after each filter/image                process is applied. Default is False. | 
|         save_files | bool |                 If True modified imagea are saved in a folder set with                setOutputPath() according to settings made with                setOutputFileType(), setSufix() and setPrefix().                Default is True. | 
|         return_list | bool |                 If True the method returns a list of modified images.                Default is False. | 
