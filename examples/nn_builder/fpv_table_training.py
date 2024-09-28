import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, BatchNormalization, Dropout, Conv2D, Flatten, LeakyReLU, ELU, Activation
from tensorflow.keras.models import load_model
from tensorflow.keras.activations import sigmoid
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import pandas as pd
from tensorflow.keras.regularizers import l2
from sklearn.preprocessing import MinMaxScaler
import joblib
import os
import csv

dir = os.getcwd()
print(dir)

# # LOAD MODEL INTO CSV
# input_file = 'X_table'
# input_path = f"{dir}/{input_file}.npy"
# input_array = np.load(input_path)
# input_array = input_array.T
# input_array = input_array[:len(input_array),:]
# csv_input_path = os.path.join(os.path.dirname(input_path), f"{dir}/{input_file}.csv")
# np.savetxt(csv_input_path, input_array, delimiter=',') 
# #--
# output_file = 'Y_table'
# output_path = f"{dir}/{output_file}.npy"
# output_array = np.load(output_path)
# output_array = output_array.T
# output_array = output_array[:len(output_array),:]
# csv_output_path = os.path.join(os.path.dirname(output_path), f"{dir}/{output_file}.csv")
# np.savetxt(csv_output_path, output_array, delimiter=',') 

# # read in complete data
# complete_input_file = f"{dir}/{input_file}.csv"
# complete_output_file = f"{dir}/{output_file}.csv"
# complete_input = pd.read_csv(complete_input_file)
# complete_output = pd.read_csv(complete_output_file)

# generate random matrix of input and output
np.random.seed(42)  
n_samples = 100  
n_input_features = 10  
n_output_features = 5
input = np.random.rand(n_samples, n_input_features)
output = np.random.rand(n_samples, n_output_features)

# normalization
input_normalization = MinMaxScaler()
output_normalization = MinMaxScaler()
input = input_normalization.fit_transform(input)
output = output_normalization.fit_transform(output)
scaling_params = {
    'input_min': input_normalization.data_min_,
    'input_max': input_normalization.data_max_,
    'output_min': output_normalization.data_min_,
    'output_max': output_normalization.data_max_
}
with open('test_model_1.dat', 'w') as f:
    for key, value in scaling_params.items():
        value_str = ' '.join(map(str, value))
        f.write(f'{key}: [{value_str}]\n')

# batch size and learning rate iter
iter1 = np.array([ (2**(10)) ])
iter2 = np.array([ 0.001 ])
epochs = 2000

with open('training_loss_values.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([' Model Number', ' Batch Size', ' Learning Rate', ' Last Loss Value'])

    # loop through batch size and learning rate
    model_number = 1
    for batch_size in iter1:
        for learning_rate in iter2:
            
            model_complete = Sequential([
                Dense(8, input_shape=(input.shape[1],), activation='relu'),
                # BatchNormalization(),
                # Activation('relu'),
                # Dropout(0.2),

                Dense(16, activation='relu'),
                # BatchNormalization(),
                # Activation('sigmoid'),
                # Dropout(0.2),

                Dense(8, activation='relu'),
                # BatchNormalization(),
                # Activation('relu'),
                # Dropout(0.2),

                Dense(output.shape[1], activation='linear')
            ])
            model_complete.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), 
                                   loss='mean_squared_error')
            # early_stopping = EarlyStopping(monitor='val_loss', 
            #                                patience=500, 
            #                                restore_best_weights=True)
            # reduce_lr = ReduceLROnPlateau(monitor='val_loss', 
            #                               factor=0.5, 
            #                               patience=5, 
            #                               min_lr=1e-6)
            history = model_complete.fit(input, output, 
                            # validation_split=0.15, 
                            batch_size=batch_size, 
                            epochs=epochs, 
                            verbose=1
                            # callbacks=[early_stopping, reduce_lr]
                            )

            model_filename = f"test_model_{model_number}.h5"
            model_complete.save(model_filename)

            trained_model = load_model(model_filename)
            predicted_complete = trained_model.predict(input)

            last_loss = history.history['loss'][-1]
            print(f'Model {model_number} - Batch size: {batch_size}, Learning rate: {learning_rate}, Last Loss: {last_loss}')

            # save the loss value to CSV
            writer.writerow([model_number, batch_size, learning_rate, last_loss])

            # plot a single feature (e.g., first feature)
            plt.figure()
            plt.plot(output[:, 0], '-k', label=f'Actual Output')
            plt.plot(predicted_complete[:, 0], '--r', label=f'Predicted Output')
            plt.legend()
            plt.show()

            # increment the model number
            model_number += 1

