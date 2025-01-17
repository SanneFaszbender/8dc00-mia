"""
Registration project code.
"""

import numpy as np
import matplotlib.pyplot as plt
import registration as reg
from IPython.display import display, clear_output


def intensity_based_registration_demo():

    # read the fixed and moving images
    # change these in order to read different images
    I = plt.imread('../data/image_data/1_1_t1.tif')
    Im = plt.imread('../data/image_data/1_1_t1_d.tif')

    # initial values for the parameters
    # we start with the identity transformation
    # most likely you will not have to change these
    x = np.array([0., 0., 0.])

    # NOTE: for affine registration you have to initialize
    # more parameters and the scaling parameters should be
    # initialized to 1 instead of 0

    # the similarity function
    # this line of code in essence creates a version of rigid_corr()
    # in which the first two input parameters (fixed and moving image)
    # are fixed and the only remaining parameter is the vector x with the
    # parameters of the transformation
    fun = lambda x: reg.rigid_corr(I, Im, x)

    # the learning rate
    mu = 0.003

    # number of iterations
    num_iter = 200

    iterations = np.arange(1, num_iter+1)
    similarity = np.full((num_iter, 1), np.nan)

    fig = plt.figure(figsize=(14,6))

    # fixed and moving image, and parameters
    ax1 = fig.add_subplot(121)

    # fixed image
    im1 = ax1.imshow(I)
    # moving image
    im2 = ax1.imshow(I, alpha=0.7)
    # parameters
    txt = ax1.text(0.3, 0.95,
        np.array2string(x, precision=5, floatmode='fixed'),
        bbox={'facecolor': 'white', 'alpha': 1, 'pad': 10},
        transform=ax1.transAxes)

    # 'learning' curve
    ax2 = fig.add_subplot(122, xlim=(0, num_iter), ylim=(0, 1))

    learning_curve, = ax2.plot(iterations, similarity, lw=2)
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Similarity')
    ax2.grid()

    # perform 'num_iter' gradient ascent updates
    for k in np.arange(num_iter):

        # gradient ascent
        g = reg.ngradient(fun, x)
        x += g*mu

        # for visualization of the result
        S, Im_t, _ = fun(x)

        clear_output(wait = True)

        # update moving image and parameters
        im2.set_data(Im_t)
        txt.set_text(np.array2string(x, precision=5, floatmode='fixed'))

        # update 'learning' curve
        similarity[k] = S
        learning_curve.set_ydata(similarity)

        display(fig)

# ------------------------------------------------------------------#
# TODO: Eigen code om poin-based registration uit te voeren
import registration_util as util

def my_point_based_registration():
    I = '../data/image_data/3_2_t1.tif'
    I_d = '../data/image_data/3_2_t1_d.tif'
    I_plt = plt.imread('../data/image_data/3_2_t1.tif')
    I_d_plt = plt.imread('../data/image_data/3_2_t1_d.tif')

    X, Xm = util.my_cpselect(I, I_d)
    affine_transformation = reg.ls_affine(X, Xm)
    transformed_moving_image, transformed_vector  = reg.image_transform(I_d_plt, affine_transformation)

    fig = plt.figure(figsize = (12,5))
    ax1 = fig.add_subplot(131)
    Im1 = ax1.imshow(I_plt)     # Fixed image or Transformed image
    Im2 = ax1.imshow(transformed_moving_image, alpha=0.7)   # Transformed image or Fixed image
    #return transformed_moving_image


def my_point_based_registration_2():

    I2 = '../data/image_data/3_2_t1.tif'                    # Tweede opdracht T1 slide
    I_d_2 = '../data/image_data/3_2_t2.tif'                 # T2 slice
    I_plt_2 = plt.imread('../data/image_data/3_2_t1.tif')
    I_d_plt_2 = plt.imread('../data/image_data/3_2_t1_d.tif')

    X2, Xm2 = util.my_cpselect(I2, I_d_2)
    affine_transformation_2 = reg.ls_affine(X2, Xm2)
    transformed_moving_image_2, transformed_vector_2  = reg.image_transform(I_d_plt_2, affine_transformation_2)

    fig = plt.figure(figsize = (12,5))
    ax1 = fig.add_subplot(131)
    Im1 = ax1.imshow(I_plt_2)     # Fixed image or Transformed image, Je mag wisselen
    Im2 = ax1.imshow(transformed_moving_image_2, alpha=0.7)   # Transformed image or Fixed image  Mag wisselen
    
def intensity_based_registration_affine_cc(im1, im2):

    # read the fixed and moving images
    # change these in order to read different images
    I = plt.imread(im1)
    Im = plt.imread(im2)

    # initial values for the parameters
    # we start with the identity transformation
    # most likely you will not have to change these
    x = np.array([0., 1., 1., 0., 0., 0., 0.])

    # NOTE: for affine registration you have to initialize
    # more parameters and the scaling parameters should be
    # initialized to 1 instead of 0

    # the similarity function
    # this line of code in essence creates a version of rigid_corr()
    # in which the first two input parameters (fixed and moving image)
    # are fixed and the only remaining parameter is the vector x with the
    # parameters of the transformation
    fun = lambda x: reg.affine_corr(I, Im, x)

    # the learning rate
    #mu = 0.0004 
    mu = 0.0006 

    # number of iterations
    num_iter = 250

    iterations = np.arange(1, num_iter+1)
    similarity = np.full((num_iter, 1), np.nan)

    fig = plt.figure(figsize=(14,6))

    # fixed and moving image, and parameters
    ax1 = fig.add_subplot(121)

    # fixed image
    im1 = ax1.imshow(I)
    # moving image
    im2 = ax1.imshow(I, alpha=0.7)
    # parameters
    txt = ax1.text(0.3, 0.95,
        np.array2string(x, precision=5, floatmode='fixed'),
        bbox={'facecolor': 'white', 'alpha': 1, 'pad': 10},
        transform=ax1.transAxes)

    # 'learning' curve
    ax2 = fig.add_subplot(122, xlim=(0, num_iter), ylim=(0, 1))

    learning_curve, = ax2.plot(iterations, similarity, lw=2)
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Similarity')
    ax2.grid()

    # perform 'num_iter' gradient ascent updates
    for k in np.arange(num_iter):

        # gradient ascent
        g = reg.ngradient(fun, x)
        x += g*mu

        # for visualization of the result
        S, Im_t, _ = fun(x)

        clear_output(wait = True)

        # update moving image and parameters
        im2.set_data(Im_t)
        txt.set_text(np.array2string(x, precision=5, floatmode='fixed'))

        # update 'learning' curve
        similarity[k] = S
        learning_curve.set_ydata(similarity)

        display(fig)

def intensity_based_registration_affine_mi(im1, im2):

    # read the fixed and moving images
    # change these in order to read different images
    I = plt.imread(im1)
    Im = plt.imread(im2)

    # initial values for the parameters
    # we start with the identity transformation
    # most likely you will not have to change these
    x = np.array([0., 1., 1., 0., 0., 0., 0.])

    # NOTE: for affine registration you have to initialize
    # more parameters and the scaling parameters should be
    # initialized to 1 instead of 0

    # the similarity function
    # this line of code in essence creates a version of rigid_corr()
    # in which the first two input parameters (fixed and moving image)
    # are fixed and the only remaining parameter is the vector x with the
    # parameters of the transformation
    fun = lambda x: reg.affine_mi(I, Im, x)

    # the learning rate
    mu = 0.00006

    # number of iterations
    num_iter = 50

    iterations = np.arange(1, num_iter+1)
    similarity = np.full((num_iter, 1), np.nan)

    fig = plt.figure(figsize=(14,6))

    # fixed and moving image, and parameters
    ax1 = fig.add_subplot(121)

    # fixed image
    im1 = ax1.imshow(I)
    # moving image
    im2 = ax1.imshow(I, alpha=0.7)
    # parameters
    txt = ax1.text(0.3, 0.95,
        np.array2string(x, precision=5, floatmode='fixed'),
        bbox={'facecolor': 'white', 'alpha': 1, 'pad': 10},
        transform=ax1.transAxes)

    # 'learning' curve
    ax2 = fig.add_subplot(122, xlim=(0, num_iter), ylim=(0, 1))

    learning_curve, = ax2.plot(iterations, similarity, lw=2)
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Similarity')
    ax2.grid()

    # perform 'num_iter' gradient ascent updates
    for k in np.arange(num_iter):

        # gradient ascent
        g = reg.ngradient(fun, x)
        x += g*mu

        # for visualization of the result
        S, Im_t, _ = fun(x)

        clear_output(wait = True)

        # update moving image and parameters
        im2.set_data(Im_t)
        txt.set_text(np.array2string(x, precision=5, floatmode='fixed'))

        # update 'learning' curve
        similarity[k] = S
        learning_curve.set_ydata(similarity)

        display(fig)