"""
This will train the model.
Author: Arda Mavi
"""
import os
import numpy as np

from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard

from get_dataset import get_dataset
from get_model import get_model, save_model

epochs = 15
batch_size = 32


def train_model(model, x, x_test, y, y_test):
    """
    This will train the model.
    :param model: Which model to train
    :param x: x
    :param x_test: x_test
    :param y: y
    :param y_test: y_test
    :return: model
    """
    if not os.path.exists('Data/Checkpoints/'):
        os.makedirs('Data/Checkpoints/')

    checkpoints = [ModelCheckpoint(
        'Data/Checkpoints/best_weights.h5',
        monitor='val_loss',
        verbose=0,
        save_best_only=True,
        save_weights_only=True,
        mode='auto',
        period=1,
), TensorBoard(log_dir='Data/Checkpoints/./logs', histogram_freq=0, write_graph=True, write_images=False)]

    # Reshape y and y_test to match the output shape of your model
    y = y.reshape(y.shape[0], -1)
    y_test = y_test.reshape(y_test.shape[0], -1)

    # If your model expects a different shape, adjust the numbers accordingly
    expected_shape = 541
    y = y[:,:expected_shape]
    y_test = y_test[:,:expected_shape]


    model.fit(x, y, batch_size=batch_size, epochs=epochs, validation_data=(x_test, y_test), shuffle=True,
              callbacks=checkpoints)

    return model


def main():
    """
    The main function.
    :return: model
    """
    x, x_test, y, y_test, action_total = get_dataset()
    print(action_total)
    model = get_model(action_total)
    model = train_model(model, x, x_test, x, x_test)
    save_model(model)
    return model


if __name__ == '__main__':
    main()
