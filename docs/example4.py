# -*- coding: utf-8 -*-
"""
Example 4:
    filtering all images stored in files in a folder for further processing - without storing modified ones in a folder
"""

import pipes                                #import impipes modules
import filters

pipeline = pipes.Pipeline()                 #create an instance of Pipeline()
pipeline.addInputFolder(r"c:/users/lukasz.kaczmarek/source/python/australia/test")  #set a folder with images to be processed

pipeline.add(filters.EdgeEnhance())         #add EdgeEnhance filter to the pipeline
pipeline.add(filters.Gamma(gamma = 1.8))    #add Gamma filter with gamma factor 1.8 to the pipeline
pipeline.add(filters.CLAHE())               #add CLAHE filter to the pipeline

modified_images = pipeline.run(save_files=False, return_list=True)      #process all images in a selected folder with the defined sequence of filters. Filtered images would not be stored (save_files=False) but will be returned as a list of numpy.ndarrays (return_list = True)

for image in modified_images:
    pipeline.show(image)                    #displays filtered images