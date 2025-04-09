import sys
import numpy as np
from matplotlib import pyplot
import matplotlib as mpl

import inspect


def featureNormalize(X):

    mu = np.mean(X, axis=0)
    X_norm = X - mu

    sigma = np.std(X_norm, axis=0, ddof=1)
    X_norm /= sigma
    return X_norm, mu, sigma

    
def displayData(X, example_width=None, figsize=(10, 10)):

    if X.ndim == 2:
        m, n = X.shape
    elif X.ndim == 1:
        n = X.size
        m = 1
        X = X[None]  # Promote to a 2 dimensional array
    else:
        raise IndexError('Input X should be 1 or 2 dimensional.')

    example_width = example_width or int(np.round(np.sqrt(n)))
    example_height = int(n / example_width)

    # Compute number of items to display
    display_rows = int(np.floor(np.sqrt(m)))
    display_cols = int(np.ceil(m / display_rows))

    fig, ax_array = pyplot.subplots(display_rows, display_cols, figsize=figsize)
    fig.subplots_adjust(wspace=0.025, hspace=0.025)

    ax_array = [ax_array] if m == 1 else ax_array.ravel()

    for i, ax in enumerate(ax_array):
        ax.imshow(X[i].reshape(example_height, example_width, order='F'), cmap='gray')
        ax.axis('off')



def plotProgresskMeans(i, X, centroid_history, idx_history):

    K = centroid_history[0].shape[0]
    pyplot.gcf().clf()
    cmap = pyplot.cm.rainbow
    norm = mpl.colors.Normalize(vmin=0, vmax=2)

    for k in range(K):
        current = np.stack([c[k, :] for c in centroid_history[:i+1]], axis=0)
        pyplot.plot(current[:, 0], current[:, 1],
                    '-Xk',
                    mec='k',
                    lw=2,
                    ms=10,
                    mfc=cmap(norm(k)),
                    mew=2)

        pyplot.scatter(X[:, 0], X[:, 1],
                       c=idx_history[i],
                       cmap=cmap,
                       marker='o',
                       s=8**2,
                       linewidths=1,)
    pyplot.grid(False)
    pyplot.title('Iteration number %d' % (i+1))


class Grader():
    grader = None
    token = ""

    def __init__(self):
        self.grader =    { 
            "data": {
                'assignment_nr':"5",
                'assignment_code':"06c92c48",
                'identifyClosestCentroids': {'name':'Identify Closest Centroids', 'score':0,'maxscore':15, 'value': None, 'func_str':'', 'feedback':''},
                'computeCentroids': {'name':'Computed Centroid Means', 'score':0, 'maxscore':15,'value': None, 'func_str':'', 'feedback':''},
                'kMeans': {'name':'k-means algorithm', 'score':0,'maxscore':20, 'value': None, 'func_str':'', 'feedback':''},
                'pca': {'name':'Compute PCA', 'score':0,'maxscore':20, 'value': None, 'func_str':'', 'feedback':''},
                'projectData': {'name':'Project Data', 'score':0,'maxscore':15, 'value': None, 'func_str':'', 'feedback':''},
                'recoverData': {'name':'Recover Data', 'score':0,'maxscore':15, 'value': None, 'func_str':'', 'feedback':''},
            }
        }
       

    def setFunc(self, id, func):
        code_str = inspect.getsource(func)
        self.grader["data"][id]["func_str"]=code_str
    
    def setValue(self, id, value):
        self.grader["data"][id]["value"]=value

    def setToken(self, token):
        self.token = token


   # Evaluate the different parts of exercise
    def grade(self):

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
            