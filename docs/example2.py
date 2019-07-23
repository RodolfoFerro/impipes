# -*- coding: utf-8 -*-
"""
Example 2:
    filtering all images stored in files in a folder and storing modified ones in files in a folder
"""

import pipes                                #import impipes modules
import filters

pipeline = pipes.Pipeline()                 #create an instance of Pipeline()
pipeline.addInputFolder(r"c:/users/lukasz.kaczmarek/source/python/australia/test")      #set a folder with images to be processed
pipeline.setPrefix("filtered_")             #sets a prefix to be added at the beginning file names with modified image
pipeline.setSufix("")                       #sets a sufix to be added at the end of file names with modified images
pipeline.setOutputFileType("tif")           #modified images shall be stored as tif files
pipeline.setOutputPath(r"c:/users/lukasz.kaczmarek/source/python/australia/test")       #sets a path to a folder where modified images are to be stored

pipeline.add(filters.EdgeEnhance())         #add EdgeEnhance filter to the pipeline
pipeline.add(filters.Gamma(gamma = 1.8))    #add Gamma filter with gamma factor 1.8 to the pipeline
pipeline.add(filters.CLAHE())               #add CLAHE filter to the pipeline

pipeline.run(save_files=True)               #process all images in selected folder with the defined sequence of filters. Filtered image would be stored (save_files=True) 