import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, BatchNormalization
import os

# NAME OF MODEL
name_of_model = "test"

# Generate random matrix of input and output
np.random.seed(35)
n_samples = 100
n_input_features = 3
n_output_features = 10
input = np.random.rand(n_samples, n_input_features)
output = np.random.rand(n_samples, n_output_features)

# Batch size and learning rate iter
iter1 = np.array([2**5])
iter2 = np.array([0.001])
epochs = 1000

# Loop through batch size and learning rate
model_number = 1
for batch_size in iter1:
    for learning_rate in iter2:
        learning_rate = float(learning_rate)
        
        # Model definition
        model_complete = Sequential([
            Input(shape=(input.shape[1],)),  # Explicit Input layer
            Dense(8, activation='relu'),
            Dense(16, activation='relu'),
            BatchNormalization(),
            Dense(8, activation='relu'),
            Dense(output.shape[1], activation='linear')
        ])
        
        model_complete.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                               loss='mean_squared_error')
        
        # Train the model
        history = model_complete.fit(input, output,
                                     batch_size=batch_size,
                                     epochs=epochs,
                                     verbose=1)

        # Save the model
        model_filename = f"test_model_{model_number}.h5"
        model_complete.save(model_filename)

        # Increment the model number
        model_number += 1
