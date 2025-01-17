"""
Utility functions for segmentation.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy import ndimage

def ngradient(fun, x, h=1e-3):
    # Computes the derivative of a function with numerical differentiation.
    # Input:
    # fun - function for which the gradient is computed
    # x - vector of parameter values at which to compute the gradient
    # h - a small positive number used in the finite difference formula
    # Output:
    # g - vector of partial derivatives (gradient) of fun

    #------------------------------------------------------------------#
    # TODO: Implement the  computation of the partial derivatives of
    # the function at x with numerical differentiation.
    # g[k] should store the partial derivative w.r.t. the k-th parameter

    g = np.zeros_like(x)
    for k in range(x.size):
        xh1 = x.copy()
        xh2 = x.copy()
        xh1[k] = xh1[k] + h/2
        xh2[k] = xh2[k] - h/2
        a = fun(xh1)
        b = fun(xh2)
        if isinstance(a, tuple):
            g[k] = (a[0] -b[0])/h
        else:
            g[k] = (a - b)/h



    #originele code
    # g = np.zeros_like(x)
    #
    # for k in range(np.size(x)):
    #     x1 = np.copy(x)
    #     x2 = np.copy(x)
    #     x1[k] = x1[k] + (h / 2)
    #     x2[k] = x2[k] - (h / 2)
    #     fun1 = fun(x1)
    #     fun2 = fun(x2)
    #     if isinstance(fun1, tuple):
    #         fun1 = fun1[0]
    #         fun2 = fun2[0]
    #     g[k] = ((fun1 - fun2) / h)
    #------------------------------------------------------------------#

    return g

def scatter_data(X, Y, feature0=0, feature1=1, ax=None):
    # scatter_data displays a scatterplot of at most 1000 samples from dataset X, and gives each point
    # a different color based on its label in Y

    k = 1000
    if len(X) > k:
        idx = np.random.randint(len(X), size=k)
        X = X[idx,:]
        Y = Y[idx]

    class_labels, indices1, indices2 = np.unique(Y, return_index=True, return_inverse=True)
    if ax is None:
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111)
        ax.grid()

    colors = cm.rainbow(np.linspace(0, 1, len(class_labels)))
    for i, c in zip(np.arange(len(class_labels)), colors):
        idx2 = indices2 == class_labels[i]
        lbl = 'X, class '+str(i)
        ax.scatter(X[idx2,feature0], X[idx2,feature1], color=c, label=lbl)


    return ax


def create_dataset(image_number, slice_number, task):
    # create_dataset Creates a dataset for a particular subject (image), slice and task
    # Input:
    # image_number - Number of the subject (scalar)
    # slice_number - Number of the slice (scalar)
    # task        - String corresponding to the task, either 'brain' or 'tissue'
    # Output:
    # X           - Nxk feature matrix, where N is the number of pixels and k is the number of features
    # Y           - Nx1 vector with labels
    # feature_labels - kx1 cell array with descriptions of the k features

    #Extract features from the subject/slice
    X, feature_labels = extract_features(image_number, slice_number)

    #Create labels
    Y = create_labels(image_number, slice_number, task)

    return X, Y, feature_labels


def extract_features(image_number, slice_number):
    # extracts features for [image_number]_[slice_number]_t1.tif and [image_number]_[slice_number]_t2.tif
    # Input:
    # image_number - Which subject (scalar)
    # slice_number - Which slice (scalar)
    # Output:
    # X           - N x k dataset, where N is the number of pixels and k is the total number of features
    # features    - k x 1 cell array describing each of the k features

    base_dir = '../data/dataset_brains/'

    t1 = plt.imread(base_dir + str(image_number) + '_' + str(slice_number) + '_t1.tif')
    t2 = plt.imread(base_dir + str(image_number) + '_' + str(slice_number) + '_t2.tif')

    fig = plt.figure(figsize=(10,10))
    ax1  = fig.add_subplot(181)
    ax1.imshow(t1)
    ax2  = fig.add_subplot(182)
    ax2.imshow(t2)
    
    n = t1.shape[0]
    features = ()
    
    #display image
    t1f = t1.flatten().T.astype(float)
    t1f = t1f.reshape(-1, 1)
    t2f = t2.flatten().T.astype(float)
    t2f = t2f.reshape(-1, 1)

    X = np.concatenate((t1f, t2f), axis=1)

    features += ('T1 intensity',)
    features += ('T2 intensity',)

    #------------------------------------------------------------------#
    # TODO: Extract more features and add them to X.
    # Don't forget to provide (short) descriptions for the features
    
    #add blurred images to features
    t1b = ndimage.gaussian_filter(t1, sigma=2) #blurred t1
    t2b = ndimage.gaussian_filter(t2, sigma=2) #blurred t2
    
    #display altered images
    ax3 = fig.add_subplot(183)
    ax3.imshow(t1b)
    ax4 = fig.add_subplot(184)
    ax4.imshow(t2b)
    
    t1b = t1b.flatten().T.astype(float)
    t1b = t1b.reshape(-1, 1)
    t2b = t2b.flatten().T.astype(float)
    t2b = t2b.reshape(-1, 1)

    X = np.concatenate((X, t1b), axis=1)
    X = np.concatenate((X, t2b), axis=1)
    
    features += ('T1 blurred intensity',)
    features += ('T2 blurred intensity',)
    
    #minimum filter
    t1min = ndimage.minimum_filter(t1, size=5)
    t2min = ndimage.minimum_filter(t2, size=5)
    
    ax5 = fig.add_subplot(185)
    ax5.imshow(t1min)
    ax6 = fig.add_subplot(186)
    ax6.imshow(t2min)
    
    t1min = t1min.flatten().T.astype(float)
    t1min = t1min.reshape(-1, 1)
    t2min = t2min.flatten().T.astype(float)
    t2min = t2min.reshape(-1, 1)

    X = np.concatenate((X, t1min), axis=1)
    X = np.concatenate((X, t2min), axis=1)
    
    features += ('T1 minimum intensity',)
    features += ('T2 minimum intensity',)
    
    #maximum filter
    t1max = ndimage.maximum_filter(t1, size=5)
    t2max = ndimage.maximum_filter(t2, size=5)
    
    ax7 = fig.add_subplot(187)
    ax7.imshow(t1max)
    ax8 = fig.add_subplot(188)
    ax8.imshow(t2max)
    
    t1max = t1max.flatten().T.astype(float)
    t1max = t1max.reshape(-1, 1)
    t2max = t2max.flatten().T.astype(float)
    t2max = t2max.reshape(-1, 1)

    X = np.concatenate((X, t1max), axis=1)
    X = np.concatenate((X, t2max), axis=1)
    
    features += ('T1 maximum intensity',)
    features += ('T2 maximum intensity',)

    #gaussian gradient magnitude
    t1_ggm = ndimage.gaussian_gradient_magnitude(t1, sigma=2)
    t2_ggm = ndimage.gaussian_gradient_magnitude(t2, sigma=2)

    fig1 = plt.figure(figsize=(10, 10))
    ax9 = fig1.add_subplot(181)
    ax9.imshow(t1_ggm)
    ax10 = fig1.add_subplot(182)
    ax10.imshow(t2_ggm)

    t1_ggm = t1_ggm.flatten().T.astype(float)
    t1_ggm = t1_ggm.reshape(-1, 1)
    t2_ggm = t2_ggm.flatten().T.astype(float)
    t2_ggm = t2_ggm.reshape(-1, 1)

    X = np.concatenate((X, t1_ggm), axis=1)
    X = np.concatenate((X, t2_ggm), axis=1)

    features += ('T1 gaussian gradient magnitude intensity',)
    features += ('T2 gaussian gradient magnitude intensity',)

    #gaussian la place (second derivative)
    t1_glp = ndimage.gaussian_laplace(t1, sigma=1)
    t2_glp = ndimage.gaussian_laplace(t2, sigma=1)

    ax11 = fig1.add_subplot(183)
    ax11.imshow(t1_glp)
    ax12 = fig1.add_subplot(184)
    ax12.imshow(t2_glp)

    t1_glp = t1_glp.flatten().T.astype(float)
    t1_glp = t1_glp.reshape(-1, 1)
    t2_glp = t2_glp.flatten().T.astype(float)
    t2_glp = t2_glp.reshape(-1, 1)

    X = np.concatenate((X, t1_glp), axis=1)
    X = np.concatenate((X, t2_glp), axis=1)

    features += ('T1 gaussian la place intensity',)
    features += ('T2 gaussian la place intensity',)

    #median filter (smoothning filter)
    t1_median = ndimage.median_filter(t1, size=5)
    t2_median = ndimage.median_filter(t2, size=5)

    ax13 = fig1.add_subplot(185)
    ax13.imshow(t1_median)
    ax14 = fig1.add_subplot(186)
    ax14.imshow(t2_median)

    t1_median = t1_median.flatten().T.astype(float)
    t1_median = t1_median.reshape(-1, 1)
    t2_median = t2_median.flatten().T.astype(float)
    t2_median = t2_median.reshape(-1, 1)

    X = np.concatenate((X, t1_median), axis=1)
    X = np.concatenate((X, t2_median), axis=1)

    features += ('T1 median intensity',)
    features += ('T2 median intensity',)

    #sobel filter (edge detection, derivative filter, horizontal/vertical lines, some smoothning)
    t1_sobel = ndimage.sobel(t1)
    t2_sobel = ndimage.sobel(t2)

    ax15 = fig1.add_subplot(187)
    ax15.imshow(t1_sobel)
    ax16 = fig1.add_subplot(188)
    ax16.imshow(t2_sobel)

    t1_sobel = t1_sobel.flatten().T.astype(float)
    t1_sobel = t1_sobel.reshape(-1, 1)
    t2_sobel = t2_sobel.flatten().T.astype(float)
    t2_sobel = t2_sobel.reshape(-1, 1)

    X = np.concatenate((X, t1_sobel), axis=1)
    X = np.concatenate((X, t2_sobel), axis=1)

    features += ('T1 sobel intensity',)
    features += ('T2 sobel intensity',)

    # rank filter (smoothning filter)
    t1_rank = ndimage.rank_filter(t1, rank=30, size=10)
    t2_rank = ndimage.rank_filter(t2, rank=30, size=10)

    fig2 = plt.figure(figsize=(10,10))
    ax17 = fig2.add_subplot(181)
    ax17.imshow(t1_rank)
    ax18 = fig2.add_subplot(182)
    ax18.imshow(t2_rank)

    t1_rank = t1_rank.flatten().T.astype(float)
    t1_rank = t1_rank.reshape(-1, 1)
    t2_rank = t2_rank.flatten().T.astype(float)
    t2_rank = t2_rank.reshape(-1, 1)

    X = np.concatenate((X, t1_sobel), axis=1)
    X = np.concatenate((X, t2_sobel), axis=1)

    features += ('T1 rank intensity',)
    features += ('T2 rank intensity',)

    # prewitt filter (edge detection, derivative filter, horizontal/vertical lines, some smoothning)
    # looks like sobel filter but has different kernel, only horizonal or vertical lines
    t1_prewitt = ndimage.prewitt(t1)
    t2_prewitt = ndimage.prewitt(t2)

    ax19 = fig2.add_subplot(183)
    ax19.imshow(t1_prewitt)
    ax20 = fig2.add_subplot(184)
    ax20.imshow(t2_prewitt)

    t1_prewitt = t1_prewitt.flatten().T.astype(float)
    t1_prewitt = t1_prewitt.reshape(-1, 1)
    t2_prewitt = t2_prewitt.flatten().T.astype(float)
    t2_prewitt = t2_prewitt.reshape(-1, 1)

    X = np.concatenate((X, t1_prewitt), axis=1)
    X = np.concatenate((X, t2_prewitt), axis=1)

    features += ('T1 prewitt intensity',)
    features += ('T2 prewitt intensity',)

    #------------------------------------------------------------------#
    return X, features


def create_labels(image_number, slice_number, task):
    # Creates labels for a particular subject (image), slice and
    # task
    #
    # Input:
    # image_number - Number of the subject (scalar)
    # slice_number - Number of the slice (scalar)
    # task        - String corresponding to the task, either 'brain' or 'tissue'
    #
    # Output:
    # Y           - Nx1 vector with labels
    #
    # Original labels reference:
    # 0 background
    # 1 cerebellum
    # 2 white matter hyperintensities/lesions
    # 3 basal ganglia and thalami
    # 4 ventricles
    # 5 white matter
    # 6 brainstem
    # 7 cortical grey matter
    # 8 cerebrospinal fluid in the extracerebral space

    #Read the ground-truth image
    base_dir = '../data/dataset_brains/'

    I = plt.imread(base_dir + str(image_number) + '_' + str(slice_number) + '_gt.tif')
    
    I=I.flatten().T
    I=I.reshape(-1,1)
    Y=I
    
    if task == 'tissue':
        Y = I>0
    elif task == 'brain':
        white_matter = (I == 2) | (I == 5)
        gray_matter  = (I == 7) | (I == 3)
        csf         = (I == 4) | (I == 8)
        background  = (I == 0) |  (I == 1) | (I == 6)

        Y[background] = 0
        Y[white_matter] = 1
        Y[gray_matter] = 2
        Y[csf] = 3
    else:
        print(task)
        raise ValueError("Variable 'task' must be one of two values: 'brain' or 'tissue'")

    Y = Y.flatten().T
    Y = Y.reshape(-1,1)
    #print(Y)

    return Y


def dice_overlap(true_labels, predicted_labels, smooth=1.):
    # returns the Dice coefficient for two binary label vectors
    # Input:
    # true_labels         Nx1 binary vector with the true labels
    # predicted_labels    Nx1 binary vector with the predicted labels
    # smooth              smoothing factor that prevents division by zero
    # Output:
    # dice          Dice coefficient

    assert true_labels.shape[0] == predicted_labels.shape[0], "Number of labels do not match"

    t = true_labels.flatten()
    p = predicted_labels.flatten()

    #------------------------------------------------------------------#
    # TODO: Implement the missing functionality for Dice overlap
    noemer = (2*sum([1 if t[i]*p[i] == True else 0 for i in range(len(t))]))
    teller = (sum(t.flatten())+sum(p.flatten()))
    dice = noemer/teller

    #------------------------------------------------------------------#
    return dice


def dice_multiclass(true_labels, predicted_labels):
    #dice_multiclass.m returns the Dice coefficient for two label vectors with
    #multiple classses
    #
    # Input:
    # true_labels         Nx1 vector with the true labels
    # predicted_labels    Nx1 vector with the predicted labels
    #
    # Output:
    # dice_score          Dice coefficient

    all_classes, indices1, indices2 = np.unique(true_labels, return_index=True, return_inverse=True)

    dice_score = np.empty((len(all_classes), 1))
    dice_score[:] = np.nan

    #Consider each class as the foreground class
    for i in np.arange(len(all_classes)):
        idx2 = indices2 == all_classes[i]
        lbl = 'X, class '+ str(all_classes[i])
        temp_true = true_labels.copy()
        temp_true[true_labels == all_classes[i]] = 1  #Class i is foreground
        temp_true[true_labels != all_classes[i]] = 0  #Everything else is background

        temp_predicted = predicted_labels.copy();
        print(temp_predicted.dtype)
        temp_predicted[predicted_labels == all_classes[i]] = 1
        temp_predicted[predicted_labels != all_classes[i]] = 0
        dice_score[i] = dice_overlap(temp_true.astype(int), temp_predicted.astype(int))

    dice_score_mean = dice_score.mean()

    return dice_score_mean


def classification_error(true_labels, predicted_labels):
    # classification_error.m returns the classification error for two vectors
    # with labels
    #
    # Input:
    # true_labels         Nx1 vector with the true labels
    # predicted_labels    Nx1 vector with the predicted labels
    #
    # Output:
    # error         Classification error

    assert true_labels.shape[0] == predicted_labels.shape[0], "Number of labels do not match"

    t = true_labels.flatten()
    p = predicted_labels.flatten()

    #------------------------------------------------------------------#
    # TODO: Implement the missing functionality for classification error
    err = np.sum(t!=p)/len(t)
    #------------------------------------------------------------------#
    return err





