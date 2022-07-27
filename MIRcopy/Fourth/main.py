import pickle

valid_languages = ['Java', 'Python', 'Shell', 'C++', 'Go']
CLASSIFICATION_PATH = 'Classification.pkl'
CLUSTER_PATH = 'Cluster.pkl'


def save_object(obj, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)


def load_object(file_name):
    with open(file_name, 'rb') as file:
        return pickle.load(file)
