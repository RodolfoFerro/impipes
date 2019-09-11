# -*- coding: utf-8 -*-
"""
Created on Tue May 28 01:53:49 2019

@author: Lukasz Kaczmarek, Rodolfo Ferro, and Ramon Ontiveros
"""

import numpy as np
import cv2
from scipy.ndimage.filters import median_filter


class Filter(object):

    def __init__(self, image=None):
        if image is not None:
            self.setImage(image)
        self.filteredImage = None

    def setImage(self, image):
        if isinstance(image, str):
            try:
                self.image = cv2.imread(image)
            except IOError as error:
                print(error)
        elif isinstance(image, np.ndarray):
            self.image = image

    def run(self):
        return self.filteredImage


class Gamma(Filter):
    """Adjusts gamma value on input image.

    Parameters
    ----------
    image : numpy.ndarray or path to an image file
            A NumPy's ndarray from cv2.imread as an input or path to an
            image file to be opened with cv2.imread.
    gamma : float (optional)
            A float containing the gamma value to be adjusted.
            By default it is set to 1.0.

    Returns
    -------
    numpy.ndarray
            A NumPy's ndarray of an image with gamma modified.
    """

    def __init__(self, image=None, gamma=1.0):
        if image is not None:
            self.setImage(image)
        self.filteredImage = None

        self.gamma = gamma

    def run(self):
        if self.image is not None:
            power = (1.0 / self.gamma)
            table = [((i / 255.0) ** power) * 255.0 for i in np.arange(0, 256)]
            table = np.array([table]).astype("uint8")
            self.filteredImage = cv2.LUT(self.image, table)
        return self.filteredImage


class Kernel(Filter):
    """Slides a kernel over an input image.

    Parameters
    ----------
    image : numpy.ndarray
            A NumPy's ndarray from cv2.imread as an input.
    kernel : 2 dimensional table of floats (optional)
            Contains the kernel to be slided.
            By default it is set to [[1,1,1],[1,20,1],[1,1,1]] which
            provides sharpening.

    Returns
    -------
    numpy.ndarray
            A NumPy's ndarray of an image with gamma modified.
    """

    def __init__(self, image=None, kernel=[[1, 1, 1], [1, 20, 1], [1, 1, 1]]):
        if image is not None:
            self.setImage(image)
        self.filteredImage = None

        self.kernel = kernel

    def run(self):
        if self.image is not None:
            kernel = np.matrix(self.kernel).tolist() \
                if type(self.kernel) is str \
                else self.kernel or [[1, 1, 1], [1, 20, 1], [1, 1, 1]]
            kernel_sum = 0
            for line in kernel:
                kernel_sum += sum(line)
            kernel = np.array(kernel).astype("float32") / kernel_sum
            self.filteredImage = cv2.filter2D(self.image, -1, kernel)

        return self.filteredImage


class Denoise(Filter):
    """Non Local Means Denosing based on OpenCV built in method.

    Parameters
    ----------
    image : numpy.ndarray
            A NumPy's ndarray from cv2.imread as an input.
    strength : integer (optional)
            defines strength of denoising operation.

    Returns
    -------
    numpy.ndarray
            A NumPy's ndarray of an image with gamma modified.
    """

    def __init__(self, image=None, strength=10):
        if image is not None:
            self.setImage(image)
        self.filteredImage = None

        self.strength = strength

    def run(self):
        if self.image is not None:
            self.filteredImage = \
                cv2.fastNlMeansDenoisingColored(self.image, None,
                                                self.strength, self.strength,
                                                7, 21)
        return self.filtereImage


class Dehaze(Filter):
    """Dehazing of an image based on Dark Channel Prior method.

    Parameters
    ----------
    image : numpy.ndarray
            A NumPy's ndarray from cv2.imread as an input.
    strength : integer (optional)
            defines strength of dehazing operation.

    Returns
    -------
    numpy.ndarray
            A NumPy's ndarray with the dahazed image.
    """

    def __init__(self, image=None, strength=10):
        if image is not None:
            self.setImage(image)
        self.filteredImage = None

    def _get_dark_channel(self, img):
        """Internal method called from _get_transmission() method
        (not to be used out of Dehaze class) provides dark channel of
        an RGB image (1 layer image composed of darkests of RGB pixels).

        Parameters
        ----------
        img : numpy.ndarray
                A NumPy's ndarray from cv2.imread as an input.

        Returns
        -------
        numpy.ndarray
                A NumPy's ndarray of an image containing the dark channel.
        """
        blue, green, red = cv2.split(img)
        dark = cv2.min(cv2.min(blue, green), red)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))

        # Erode filter will remove small white elements from the
        # dark channel (probably noise)
        return cv2.erode(dark, kernel)

    def _get_atmospheric_light(self, img, dark):
        """Internal method called from run() method (not to be used out
        of Dehaze class). Provides estimation of the atmosferic light (A)
        for an image.

        Parameters
        ----------
        img : numpy.ndarray
                A NumPy's ndarray from cv2.imread as an input.
        dark : numpy.ndarray
                A NumPy's ndarray containing the dark channel of img
                image (output of get_dark_channel function).

        Returns
        -------
        numpy.ndarray
                A NumPy's ndarray [1,3] containg BGR values for the
                estimated atmospheric light.
        """
        img_size = img.shape[0] * img.shape[1]
        dark = dark.reshape(img_size, 1)
        sorted_indexes = np.argsort(dark, 0)
        # 10% of brightest pixels in the dark channel
        sorted_indexes = sorted_indexes[int(0.9 * img_size)::]
        blue, green, red = cv2.split(img)
        gray = (0.299 * red + 0.587 * green +
                0.114 * blue)  # Convert RGB to grey
        gray = gray.reshape(img_size, 1)

        # Localize brightest grey pixels over lightest dark channel spots
        position = np.where(gray == max(gray[sorted_indexes]))
        position = position[0][0]  # Position of the lightest grey pixel
        img_vec = img.reshape(img_size, 3)

        # Return RGB values corresponding to the brightest grey pixel
        # It is assumed it is the atmospheric light
        return (np.array(img_vec[position])).reshape(1, 3)

    def _get_transmission(self, img, A):
        """Subfunction for dehaze function (not to be used out of dehaze)
        provides map of estimated transmission for an image.

        Parameters
        ----------
        img : numpy.ndarray
                A NumPy's ndarray from cv2.imread as an input.
        A : numpy.ndarray
                A NumPy's ndarray [1,3] containg BGR values for the
                atmospheric light.

        Returns
        -------
        numpy.ndarray
                A NumPy's ndarray containg map of estimated transmission.
        """
        img_t = np.empty(img.shape, img.dtype)
        for layer in range(3):
            img_t[:, :, layer] = img[:, :, layer] / A[0, layer]

        return 1 - 0.95 * self._get_dark_channel(img_t)

    def _refine_transmission(self, img, t_est):
        """Subfunction for dehaze function (not to be used out of dehaze)
        refines map of estimated transmission with soft matting method.

        Parameters
        ----------
        img : numpy.ndarray
                A NumPy's ndarray from cv2.imread as an input.
        t_est : numpy.ndarray
                A NumPy's ndarray with map of estimated transmission
                (output of get_transmission function).

        Returns
        -------
        numpy.ndarray
                A NumPy's ndarray containg refined map of transmission.
        """
        r = 50
        eps = 0.0001
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = np.float64(gray) / 255
        mean_I = cv2.boxFilter(gray, cv2.CV_64F, (r, r))
        mean_p = cv2.boxFilter(t_est, cv2.CV_64F, (r, r))
        mean_Ip = cv2.boxFilter(gray * t_est, cv2.CV_64F, (r, r))
        cov_Ip = mean_Ip - mean_I * mean_p
        mean_II = cv2.boxFilter(gray * gray, cv2.CV_64F, (r, r))
        var_I = mean_II - mean_I * mean_I
        a = cov_Ip / (var_I + eps)
        b = mean_p - a * mean_I
        mean_a = cv2.boxFilter(a, cv2.CV_64F, (r, r))
        mean_b = cv2.boxFilter(b, cv2.CV_64F, (r, r))

        return mean_a * gray + mean_b

    def _recover(self, img, t, A):
        """Subfunction for dehaze function (not to be used out of dehaze)
        recovers dehazed image for a hazed one.

        Parameters
        ----------
        img : numpy.ndarray
                A NumPy's ndarray from cv2.imread as an input.
        t : numpy.ndarray
                A NumPy's ndarray with map of transmission (output
                refine_transmission function).
        A : numpy.ndarray
                A NumPy's ndarray [1,3] containg BGR values for the
                atmospheric light.

        Returns
        -------
        numpy.ndarray
                A NumPy's ndarray containg dehazed BGR image.
        """
        img_t = np.empty(img.shape, img.dtype)
        t = cv2.max(t, 0.1)  # Make sure that transmission is not 0

        for layer in range(3):
            img_t[:, :, layer] = (img[:, :, layer] - A[0, layer])
            img_t[:, :, layer] /= t + A[0, layer]

        img_t[img_t < 0] = 0

        return img_t

    def run(self):

        if self.image is not None:
            img_norm = self.image.astype('float64') / 255
            dark_channel = self._get_dark_channel(img_norm)
            A = self._get_atmospheric_light(img_norm, dark_channel)
            t_est = self._get_transmission(img_norm, A)
            t = self._refine_transmission(self.image, t_est)
            modified_64 = self._recover(img_norm, t, A)
            self.filteredImage = (modified_64 * 255).astype('uint8')

        return self.filteredImage


class Unsharp(Filter):
    """Unsharp masking on input image.

    Parameters
    ----------
    image : numpy.ndarray
            A NumPy's ndarray from cv2.imread as an input.
    sigma : integer (optional)
            A integer containing the size of the footprint to apply to
            a median filter to the image.
            By default it is set to 5.
    ustrength : float (optional)
            A float containing the amount of the Laplacian version of
            the image to add or take.
            By default it is set to add 0.8.

    Returns
    -------
    numpy.ndarray
            A NumPy's ndarray of an image with gamma modified.
    """

    def __init__(self, image=None, sigma=8, ustrength=2):
        if image is not None:
            self.setImage(image)
        self.filteredImage = None

        self.sigma = sigma
        self.ustrength = ustrength

    def _unsharp_channel(self, chan, sigma, strength):
        """Unsharp masking on input image channel.

        Parameters
        ----------
        chan : numpy.ndarray
                A NumPy's ndarray from the channel to sharp.
        sigma : integer
                A integer containing the size of the footprint to apply to
                a median filter to the image.
        strength : float
                A float containing the amount of the Laplacian version of
                the image to add or take,

        Returns
        -------
        numpy.ndarray
                A NumPy's ndarray of a channel with gamma modified.
        """
        # Median filtering
        image_mf = median_filter(chan, sigma)

        # Calculate the Laplacian
        lap = cv2.Laplacian(image_mf, cv2.CV_64F)

        # Calculate the sharpened image
        sharp = chan - strength * lap

        # Saturate the pixels in either direction
        sharp[sharp > 255] = 255
        sharp[sharp < 0] = 0

        return sharp

    def run(self):
        if self.image is not None:
            sharp = np.zeros_like(self.image)
            for i in range(3):
                sharp[:, :, i] = self._unsharp_channel(self.img[:, :, i],
                                                       self.sigma,
                                                       self.ustrength)
            self.filteredImage = sharp

        return self.filteredImage


class CLAHE(Filter):
    """Contrast Limited Adaptive Histogram Equalization.

    Parameters
    ----------
    image : numpy.ndarray
        A NumPy's ndarray from cv2.imread as an input.
    clip_limit : float
        Clip threshold for CLAHE.
    tile_grid_size : int
        Size of the grid to perform CLAHE calculation.
    apply : int
        Set this if you want to reapply clahe to reduce the clip overshoot.

    Returns
    -------
    numpy.ndarray
        A NumPy's ndarray of an image.
    """

    def __init__(self, image=None, clip_limit=2.0, tile_grid_size=8, apply=1):
        if image is not None:
            self.setImage(image)
        self.filteredImage = None

        self.clip_limit = clip_limit
        self.tile_grid_size = tile_grid_size
        self.apply = apply

    def run(self):

        if self.image is not None:
            he = cv2.createCLAHE(clipLimit=self.clip_limit,
                                 tileGridSize=(self.tile_grid_size,
                                               self.tile_grid_size))
            lab = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
            lab_planes = cv2.split(lab)
            for _ in range(self.apply):
                lab_planes[0] = he.apply(lab_planes[0])  # Lightness component
                lab = cv2.merge(lab_planes)

            self.filteredImage = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return self.filteredImage
