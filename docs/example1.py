# -*- coding: utf-8 -*-
"""
Example 1:
    filtering a single image from a file and storing the modified one in a file
"""

import pipes                                #import impipes modules
import filters

pipeline = pipes.Pipeline()                 #create an instance of Pipeline()
pipeline.addImage(r"c:/users/lukasz.kaczmarek/source/python/australia/test/test.tif")       #set the file with image to be processed
pipeline.setPrefix("filtered_")             #sets a prefix to be added at the beginning file names with modified images
pipeline.setSufix("")                       #sets a sufix to be added at the end of file names with modified images
pipeline.setOutputFileType("tif")           #modified images shall be stored as tif files
pipeline.setOutputPath(r"c:/users/lukasz.kaczmarek/source/python/australia/test")           #sets a path to a folder where modified images are to be stored

pipeline.add(filters.EdgeEnhance())         #add EdgeEnhance filter to the pipeline
pipeline.add(filters.Gamma(gamma = 1.8))    #add Gamma filter with gamma factor 1.8 to the pipeline
pipeline.add(filters.CLAHE())               #add CLAHE filter to the pipeline

pipeline.run(save_files=True)               #process the selected image with the defined sequence of filters. Filtered image would be stored (save_files=True) 
