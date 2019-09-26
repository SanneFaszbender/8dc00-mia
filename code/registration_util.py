"""
Utility functions for registration.
"""

import numpy as np
from cpselect.cpselect import cpselect


def test_object(centered=True):
    # Generate an F-like test object.
    # Input:
    # centered - set the object centroid to the origin
    # Output:
    # X - coordinates of the test object

    X = np.array([[4, 4, 4.5, 4.5, 6, 6, 4.5, 4.5, 7, 7, 4], [10, 4, 4, 7, 7, 7.5, 7.5, 9.5, 9.5, 10, 10]])

    if centered:
        X[0, :] = X[0, :] - np.mean(X[0, :])
        X[1, :] = X[1, :] - np.mean(X[1, :])

    return X


def c2h(X):
    # Convert cartesian to homogeneous coordinates.
    # Input:
    # X - cartesian coordinates
    # Output:
    # Xh - homogeneous coordinates

    n = np.ones([1,X.shape[1]])
    Xh = np.concatenate((X,n))

    return Xh


def t2h(T, t):
    # Convert a 2D transformation matrix to homogeneous form.
    # Input:
    # T - 2D transformation matrix
    # t - 2D translation vector
    # Output:
    # Th - homogeneous transformation matrix

    #------------------------------------------------------------------#
    # TODO: Implement conversion of a transformation matrix and a translation vector to homogeneous transformation matrix.
    #pass
    #print(T)
    #print(t)
    t = t[np.newaxis, :]    #nette manier om extra [ ] omheen te zetten
    Th = np.concatenate((T,np.transpose(t)), 1)     #transpose t omdat deze anders aan de onderkant komt
    Th = np.concatenate((Th, np.array([[0,0,1]])),0)    #hier staat gewoon extra [ ] omheen
    return Th

    #------------------------------------------------------------------#

def plot_object(ax, X):
    # Plot 2D object.

    # Input:
    # X - coordinates of the shape
    ax.plot(X[0,:], X[1,:], linewidth=2)

def my_cpselect(I_path, Im_path):
    # Wrapper around cpselect that returns the point coordinates
    # in the expected format (coordinates in rows).
    # Input:
    # I - fixed image
    # Im - moving image
    # Output:
    # X - control points in the fixed image
    # Xm - control points in the moving image

    #------------------------------------------------------------------#
    # TODO: Call cpselect and modify the returned point coordinates.

    # Using cpselect to receive coordinates points

    controlpointlist = cpselect(I_path, Im_path)  # List of dictionary with control points

    # For loop over the selected points and storing in list
    x_1 = []
    y_1 = []
    x_2 = []
    y_2 = []

    # For-loop
    for dict in controlpointlist:
        x_1.append(dict['img1_x'])
        y_1.append(dict['img1_y'])
        x_2.append(dict['img2_x'])
        y_2.append(dict['img2_y'])

    # Turning lists into arrays

    x_1 = np.asarray(x_1)
    y_1 = np.asarray(y_1)
    x_2 = np.asarray(x_2)
    y_2 = np.asarray(y_2)

    X = np.concatenate(([x_1], [y_1]))
    Xm = np.concatenate(([x_2], [y_2]))

    ones = np.zeros_like(x_1)
    ones[:] = 1

    Matrix_X = np.concatenate((X, [ones]), 0)
    Matrix_Xm = np.concatenate((Xm, [ones]), 0)

    #print("Matrix_X = " + str(Matrix_X))
    #print("Matrix_Xm = " + str(Matrix_Xm))


    #------------------------------------------------------------------#

    return Matrix_X, Matrix_Xm
