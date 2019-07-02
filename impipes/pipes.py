# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 13:54:03 2019

@author: Cristian Vargas, Lukasz Kaczmarek, and Rodolfo Ferro
"""

import os
import os.path
import filters
import matplotlib.pyplot as plt
import numpy
import wget
import cv2


class Pipeline(object):

    def __init__(self, pipeline=[]):

        self.images = []
        self.pipeline = pipeline
        self.outputPath = ''
        self.inputPath = ''
        self.outputFIleType = 'jpg'
        self.sufix = "_modified"
        self.prefix = ""

    def setSufix(self, sufix):
        """Sets sufix to be added at the end of file names while storing.

        Parameters
        ----------
        sufix : str
                A sufix to be added to file names with modified images at
                their ends.
        """

        if type(sufix) is str:
            self.sufix = sufix

    def setPrefix(self, prefix):
        """Sets prefix to be added at the beginning of file names while storing.

        Parameters
        ----------
        prefix : str
                A prefix to be added to file names with modified images at
                their beginning.
        """

        if type(prefix) is str:
            self.prefix = prefix

    def setOutputFileType(self, fileType='jpg'):
        """Sets format of files for storing modified images. Must be jpg,
        jpeg, png or tif.

        Parameters
        ----------
        fileType : str
                A str describing type of output format ("jpg", "jpeg",
                "png" or "tif").
        """

        if fileType in ('jpg', 'jpeg', 'png', 'tif'):
            self.outputFIleType = fileType
        else:
            print("File type must be jpg, jpeg, png or tif")

    def setOutputPath(self, path):
        """Sets path to a folder in which modifed images will be stored.
        If the folder does not exist it will be created.

        Parameters
        ----------
        path : str
                The path to the output folder like r"~/path/to/output/folder"
        """

        self.outputPath = path
        if not os.path.isdir(self.outputPath):
            try:
                os.mkdir(self.outputPath)
            except IOError as error:
                print(error)

    def addImage(self, imagePath):
        """Adds a raw image file to be proccessed to the pipeline.

        Parameters
        ----------
        imagePath : str
                The path to an image file like r"~/path/to/my/image.jpg"
        """

        self.images.append(imagePath)

    def addInputFolder(self, path):
        """Adds a folder with image files to be proccessed to the pipeline.
        Image files (jpg, jpeg, png or tif) are searched in the folder
        and its subfolders.

        Parameters
        ----------
        path : str
                The path to image files like r"~/path/to/image/files"
        """

        self.inputPath = path
        for root, dir, files in os.walk(self.inputPath):
            for name in files:
                extension = name.split('.')[-1]
                if extension in ['jpg', 'jpeg', 'png', 'tif']:
                    self.addImage(os.path.join(root, name))

    def add(self, item):
        """Adds a filter/image process to the pipeline.

        Parameters
        ----------
        item : files.Filter
                An instance of a filter class. For example Kernel(),
                CLAHE() or Dehaze() etc.
        """

        self.pipeline.append(item)

    def setPipeline(self, pipeline):
        """Sets a sequence of filters/image processes to be applied to raw images.

        Parameters
        ----------
        pipeline : list
                A list of instances of a filter classes.
                For example [Kernel(), CLAHE(), Dehaze()] etc.
        """

        self.pipeline = pipeline

    def saveModified(self, image, fileName):
        """Stores a modifed image in a file.

        Parameters
        ----------
        image : numpy.ndarray
                A NumPy's array containing an image.
        fileName : str
                Name of the image file.
        """

        filename = ''.join(fileName.split('.')[:-1])
        to_join_with = \
            self.prefix + filename + self.sufix + "." + self.outputFIleType
        outputPath = os.path.join(self.outputPath, to_join_with)
        try:
            cv2.imwrite(outputPath, image)
        except IOError as error:
            print(error)

    def show(self, image):
        """Displays an image.

        Parameters
        ----------
        image : numpy.ndarray
                A NumPy's array containing an image.
        """

        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.show()

    def process(self, image, display_steps=False):
        """Applies a seqence of filters/image processes defined with add() or
        setPipeline() to an image.

        Parameters
        ----------
        image : numpy.ndarray
                A NumPy's array containing an image.
        display_steps : bool
                If True image is displayed after each filter/image process
                is applied. Default is False.

        Return
        ----------
        numpy.ndarray
                A NumPy's array containing the modified image.
        """

        if isinstance(image, str):
            try:
                temp = cv2.imread(image)
            except IOError as error:
                print(error)
        elif isinstance(image, numpy.ndarray):
            temp = image

        for item in self.pipeline:
            if display_steps:
                self.show(temp)

            item.setImage(temp)
            temp = item.run()

        if display_steps:
            self.show(temp)

        return temp

    def run(self, save_files=True, display_steps=False, return_list=False):
        """Applies a seqence of filters/image processes defined with add() or
        setPipeline() to images defined with addImage() or addInputFolder().

        Parameters
        ----------
        display_steps : bool
                If True images are displayed after each filter/image
                process is applied. Default is False.
        save_files : bool
                If True modified imagea are saved in a folder set with
                setOutputPath() according to settings made with
                setOutputFileType(), setSufix() and setPrefix().
                Default is True.
        return_list : bool
                If True the method returns a list of modified images.
                Default is False.

        Return
        ----------
        list
                A list of NumPy's arrays containing modified images or
                empty list.
        """
        number = len(self.images)
        current = 0
        modified = []
        for image in self.images:
            current += 1
            print("Processing image ", current, "out of", number, "\n", image)
            temp = self.process(image, display_steps=display_steps)

            if save_files:
                fileName = os.path.split(image)[1]
                self.saveModified(temp, fileName)

            if return_list:
                modified.append(temp)

        return modified


def example():
    img_url = "https://rodolfoferro.xyz/assets/images/dog_original.jpeg"
    wget.download(img_url, out='dog.jpg')
    cwd = os.getcwd()
    print(cwd)

    pipeline = Pipeline()

    pipeline.add(filters.Dehaze())
    pipeline.add(filters.Gamma(gamma=1.8))
    pipeline.add(filters.Kernel(kernel=[[1, 1, 1], [1, 20, 1], [1, 1, 1]]))
    pipeline.add(filters.CLAHE())

    pipeline.addInputFolder(cwd)
    pipeline.setOutputPath(cwd)
    pipeline.setOutputFileType('jpg')
    pipeline.setSufix("_modified")

    modified_images = pipeline.run(save_files=True,
                                   return_list=True,
                                   display_steps=False)

    for image in modified_images:
        pipeline.show(image)


if __name__ == "__main__":
    example()
