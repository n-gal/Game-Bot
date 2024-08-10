from PIL import Image
import numpy as np

temperature = 0.1

def softmax(x, temperature):
    e_x = np.exp(x / temperature)
    return e_x / e_x.sum(axis=0)

def predict(model, X):
    """
    This function will make a prediction based on the input data.
    :param model: Which model to use.
    :param X: input data.
    :return: y_pred: prediction.
    """
    # resize it with PIL, because scipy.misc.imresize is deprecated.
    X_resized = Image.fromarray(X).resize((150, 150), resample=Image.BICUBIC)
    X_resized = np.array(X_resized)
    logits = model.predict(X_resized.reshape(1, 150, 150, 3))
    
    probabilities = softmax(logits[0], temperature)
    y = np.random.choice(len(probabilities), p=probabilities)
    return y

