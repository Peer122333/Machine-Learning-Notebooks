from cgi import test
import matplotlib.pyplot as plt
import os
import pickle
import numpy as np
import cv2
import helpers

from sklearn.model_selection import train_test_split

helpers.set_logging_level()


class AbstractDataLoader(object):
    """
        Abstract Data Loader class
    """
    def __init__(self):
        self.data_loaded = False
        self.dataset_splits = False

    def is_data_loaded(self):
        return self.data_loaded

    def has_dataset_splits(self):
        return self.dataset_splits

    def loadDataset(self):
        raise NotImplementedError()

    def get_label_names_from_id(self, id_arr):
        indices_in_dict = [list(self.include.values()).index(value) for value in id_arr]
        return [list(self.include.keys())[ind] for ind in indices_in_dict]
    
    def get_id_from_label_names(self, name_arr):
        return [self.include.get(key, None) for key in name_arr] 


class AnimalFacesDataLoader(AbstractDataLoader):

    def __init__(self, width=80, height=None):
        """
        AnimalFaces Data Loader
        Input:
           width -- Scaled image width in dataset
           height -- Scaled image height in dataset; if Nore height=width
        """
        super().__init__()
        self.base_name = 'animal_faces'
        self.src= "Data/AnimalFaces"
        self.width = width
        self.data = None
        self.labels = None
        if height:
            self.height = height
        else:
            self.height = width

        self.include_dogcats = {
                'CatHead':0,
                'DogHead':1
                }

        self.include_all = {
                'BearHead':0,
                'CatHead':1,
                'ChickenHead':2,
                'CowHead':3,
                'DeerHead':4,
                'DogHead':5,
                'DuckHead':6,
                'EagleHead':7,
                'ElephantHead':8,
                'HumanHead':9,
                'LionHead':10,
                'MonkeyHead':11,
                'MouseHead':12,
                'Natural':13,
                'PandaHead':14,
                'PigHead':15,
                'PigeonHead':16,
                'RabbitHead':17,
                'SheepHead':18,
                'TigerHead':19,
                'WolfHead':20
                }
        self.label_names = self.include_all.keys()

    def get_label_names(self):
        """
        Output:
           label_names -- list of label names (str)
        """
        return self.label_names

    def loadDataset(self, all=True, jitter_samples = False):
        """
        load images from path, resize them and write them as arrays to a dictionary, 
        together with labels and metadata. The dictionary is written to a pickle file 
        named 'AnimalFaces__{self.width}x{self.height}px.pkl'.
        
        Input:
            src --- str path to data
            jitter_samples --- if True Training samples get jittered additionally
        """

        saved_dataset_path = "AnimalFaces_{}x{}px.pkl".format(self.width, self.height)
        
        if os.path.isfile(saved_dataset_path):
            with open(saved_dataset_path, 'rb') as file:
                dataset = pickle.load(file) # Reloading not implemented
        else:

            labels = []
            data = []

            if all:
                self.include = self.include_all
                self.label_names = self.include_all.keys()
            else:
                self.include = self.include_dogcats
                self.label_names = self.include_dogcats.keys()

            # read all images in PATH, resize and write to DESTINATION_PATH
            dir_list = os.listdir(self.src)
            for subdir in np.sort(dir_list):
                if subdir in self.include.keys():
                    current_path = os.path.join(self.src, subdir)
                    for file in os.listdir(current_path):
                        if file[-3:] in {'jpg', 'png'}:
                            im = cv2.imread(os.path.join(current_path, file))
                            im = cv2.resize(im, (self.width, self.height))
                            labels.append(self.include[subdir])
                            data.append(im)

        self.data = data
        self.labels = labels
        return data, labels

    ## visualization functions
    def show_plot_data_statistics(self):
        """
        Shows data stats of loaded dataset and splits
        """
        if self.data == None:
            self.loadDataset()
        plt.set_loglevel("info") 
        plt.suptitle('number of images')
        helpers.plot_bar(self.get_label_names_from_id(self.labels), loc=-0.0)
        plt.legend([
            '{0} images (complete)'.format(len(self.labels)), 
        ])
        plt.show()


        