from IPython.display import HTML, display
import numpy as np
from matplotlib import pyplot
import inspect

def set_background(color):    
    script = (
        "var cell = this.closest('.jp-CodeCell');"
        "var editor = cell.querySelector('.jp-Editor');"
        "editor.style.background='{}';"
        "this.parentNode.removeChild(this)"
    ).format(color)
    
    display(HTML('<img src onerror="{}" style="display:none">'.format(script)))

def mapFeature(X1, X2, degree=8):
    """
    Maps the two input features to quadratic features

    Returns a new feature array with more features, comprising of
    X1, X2, X1.^2, X2.^2, X1*X2, X1*X2.^2, etc.
    Note that by this we can also model dependencies between feature dimensions.

    Parameters
    ----------
    X1 : array_like
        A vector of shape (m, 1), containing one feature for all examples.

    X2 : array_like
        A vector of shape (m, 1), containing a second feature for all examples.
        Inputs X1, X2 must be the same size.

    degree: int, optional
        The polynomial degree.

    Returns
    -------
    : array_like
        A matrix of of m rows, and columns depend on the degree of polynomial.
    """

    if X1.ndim > 0:
        out = [np.ones(X1.shape[0])]
    else:
        out = [np.float64(1)]

    for i in range(1, degree + 1):
        for j in range(i + 1):
            poly = (X1 ** (i - j)) * (X2 ** j)
            out.append(poly)

    if X1.ndim > 0:
        return np.stack(out, axis=1)
    else:
        return out


def plotDecisionBoundary(plotData, w, X, y):
    """
    Plots the data points X and y into a new figure with the decision boundary defined by theta.
    Plots the data points with * for the positive examples and o for  the negative examples.

    Parameters
    ----------
    plotData : func
        A function reference for plotting the X, y data.

    w : array_like
        Parameters for logistic regression. A vector of shape (n+1, ).

    X : array_like
        The input dataset. X is assumed to be  a either:
            1) Mx3 matrix, where the first column is an all ones column for the intercept.
            2) MxN, N>3 matrix, where the first column is all ones.

    y : array_like
        Vector of data labels of shape (m, ).
    """
    # make sure w is a numpy array
    w = np.array(w)

    # Plot Data (remember first column in X is the intercept)
    plotData(X[:, 1:3], y)

    if X.shape[1] <= 3:
        # Only need 2 points to define a line, so choose two endpoints
        plot_x = np.array([np.min(X[:, 1]) - 2, np.max(X[:, 1]) + 2])

        # Calculate the decision boundary line
        plot_y = (-1. / w[2]) * (w[1] * plot_x + w[0])

        # Plot, and adjust axes for better viewing
        pyplot.plot(plot_x, plot_y)

        # Legend, specific for the exercise
        pyplot.legend(['Admitted', 'Not admitted', 'Decision Boundary'])
        #pyplot.xlim([30, 100])
        #pyplot.ylim([30, 100])
    else:
        # Here is the grid range
        u = np.linspace(-1, 1.5, 50)
        v = np.linspace(-1, 1.5, 50)

        z = np.zeros((u.size, v.size))
        # Evaluate z = w*x over the grid
        for i, ui in enumerate(u):
            for j, vj in enumerate(v):
                z[i, j] = np.dot(mapFeature(ui, vj), w)
                #z[i, j] = 1 / (1 + np.exp(-z[i, j]))
                

        z = z.T  # important to transpose z before calling contour
        # print(z)

        # Plot z = 0
        pyplot.contour(u, v, z, levels=[0], linewidths=2, colors='g')
        pyplot.contourf(u, v, z, levels=[np.min(z), 0, np.max(z)], cmap='Greens', alpha=0.4)

class Grader():
    grader = None
    token = ""

    def __init__(self):
        self.grader =    { 
        "data": { 
                'assignment_nr':"2",
                'assignment_code':"7be2db82",
                'computeCost': {'name':'Cost lin regr', 'score':0, 'maxscore':20,'func_str':'', 'feedback':''},
                'normalEqn': {'name':'Normal Eq', 'score':0,'maxscore':15, 'func_str':'', 'feedback':''},
                'gradientDescent': {'name':'GD lin regr', 'score':0,'maxscore':20, 'func_str':'', 'feedback':''},
                'sigmoid': {'name':'Sigmoid', 'score':0,'maxscore':5, 'func_str':'', 'feedback':''},
                'costFunctionLog': {'name':'Cost log regr.', 'score':0,'maxscore':20, 'func_str':'', 'feedback':''},
                'gradientDescentLog': {'name':'GD log regr', 'score':0,'maxscore':15, 'func_str':'', 'feedback':''},
                'predict': {'name':'Predict', 'score':0,'maxscore':5, 'func_str':'', 'feedback':''},
            }
        }

    def setFunc(self, id, func):
        code_str = inspect.getsource(func)
        self.grader["data"][id]["func_str"]=code_str

    def setToken(self, token):
        self.token = token

    def grade(self):
        
        
        print('\nSubmitting Solutions | Programming Exercise')

        # Evaluate the different parts of exercise

        # get results from remote
        result = self.submit()

        # Print the grading table
        if not result:
            return

        reachedScore = 0
        maxScore = 0
        for id, part in result.items():
            if "assignment_" in id:
                continue 
            score = '%d / %3d' % (part["score"], part["maxscore"])
            print('%43s | %9s | %-s' % (part["name"], score, part["feedback"]))
            reachedScore += part["score"]
            maxScore += part["maxscore"]
        total_score = '%d / %d' % (reachedScore,maxScore)
        print('                                  --------------------------------')
        print('%43s | %9s | %-s\n' % ("", total_score, ""))


    def submit(self):
        import requests
        import json

        
        url = "http://evalml.da.private.hm.edu/result_receiver/"
        
        head = {'Authorization': 'token {}'.format(self.token)}
        
        response = requests.post(url, json=self.grader, headers=head)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return False