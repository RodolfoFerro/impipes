# -*- coding: utf-8 -*-
"""
Example 3:
    filtering a single image from a file for further processing - without storing the modified one
"""

import pipes  # import impipes modules
import filters

pipeline = pipes.Pipeline()  # create an instance of Pipeline()
# set the file with image to be processed
pipeline.addImage(
    r"c:/users/lukasz.kaczmarek/source/python/australia/test/test.tif")

pipeline.add(filters.EdgeEnhance())  # add EdgeEnhance filter to the pipeline
# add Gamma filter with gamma factor 1.8 to the pipeline
pipeline.add(filters.Gamma(gamma=1.8))
pipeline.add(filters.CLAHE())  # add CLAHE filter to the pipeline

# process the selected image with the defined sequence of filters. Filtered image would not be stored (save_files=False) but will be returned as a [numpy.ndarrays] (return_list = True)
modified_images = pipeline.run(save_files=False, return_list=True)

pipeline.show(modified_images[0])  # displays the filtered image
