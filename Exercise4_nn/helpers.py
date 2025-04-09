import itertools
import logging
import sys

import matplotlib.pyplot as plt
import numpy as np

# helper functions


def set_logging_level():
    """set logging level (hard_coded)"""
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


def plot_bar(y, loc=0.5, relative=False):
    """
    Bar plot
    Input:
        y -- data
        loc -- relative horizontal location of bar
        relative -- bars normalized if True
    """
    width = 0.35

    # calculate counts per type and sort, to ensure their order
    unique, counts = np.unique(y, return_counts=True)
    sorted_index = np.argsort(unique)
    unique = unique[sorted_index]

    if relative:
        # plot as a percentage
        counts = 100 * counts[sorted_index] / len(y)
        ylabel_text = "% count"
    else:
        # plot counts
        counts = counts[sorted_index]
        ylabel_text = "count"

    xtemp = np.arange(len(unique))

    plt.bar(xtemp + loc * width, counts, align="center", alpha=0.7, width=width)
    plt.xticks(xtemp, unique, rotation=90)
    plt.xlabel("Classes")
    plt.ylabel(ylabel_text)


def plot_confusion_matrix(
    cm, classes, normalize=True, title="Confusion matrix", cmap=plt.cm.Blues
):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    Input:
        cm -- confusion matrix
        normalize -- if True values are normalized
        title -- plot title
        cmap -- color map
    """
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print("Confusion matrix, without normalization")

    print(cm)

    fmt = ".2f" if normalize else "d"
    thresh = cm.max() / 2.0
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            j,
            i,
            format(cm[i, j], fmt),
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black",
        )

    plt.tight_layout()
    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    plt.show()


def get_classification_accuracy(labels, predictions):
    """
    Accuracy and time of classifier on complete test dataset
    Output:
       accuracy -- of classifier on test dataset
    """
    assert len(labels) == len(predictions)
    # in case we have (#smaple x #classes) we have a probability prediction,
    # so we need to find the label with max probability
    if predictions.ndim == 2:
        pred_max = np.argmax(predictions, axis=-1)
    else:
        pred_max = predictions
    accuracy = 100 * sum(a == b for a, b in zip(pred_max, labels)) / len(labels)

    return accuracy
