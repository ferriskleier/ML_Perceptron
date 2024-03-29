#!/usr/bin/env python3
### Training a two-layer MLP in Python
# In order to run this script, Python 3 and Numpy must be installed.
# See: https://numpy.org/install/

####################################################################
import numpy as np

### The XOR example dataset.
# note the prepended constant 1s 
xs = np.array([
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0],
    [1, 0, 0, 1, 1],
    [1, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [1, 0, 1, 1, 0],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 0, 0],
    [1, 1, 0, 0, 1],
    [1, 1, 0, 1, 0],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 0, 0],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
])
cs = [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]

### Initialization
def initialize_random_weights(p, l, k):
    """Initialize the weight matrices of a two-layer MLP.

    Args:
        p (int): number of input attributes
        l (int): number of hidden layer features
        k (int): number of output classes

    Returns:
        W_h (ndarray): l-by-(p+1) matrix
        W_o (ndarray): k-by-(l+1) matrix
    """
    W_h = np.random.normal(size=(l, p+1))
    W_o = np.random.normal(size=(k, l+1))
    return W_h, W_o


### Threshold function
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


### Function for printing weights and predictions
def print_weights_and_predictions(W_h, W_o):
    print(f"W_h = {W_h.round(2)}")
    print(f"W_o = {W_o.round(2)}")
    print()
    # The network's predictions for the entire training dataset
    y = sigmoid(W_o @ np.vstack([np.ones(len(xs)), sigmoid(W_h @ xs.T)]))
    print(f"Predictions: {y.flatten().round(2)}")
    print(f"      Truth: {cs}")


########################################################################
### IGD Algorithm.
## (the corresponding line numbers from the pseudocode are noted below)

tmax = 2000   # number of epochs
eta = 0.5  # learning rate

## (1) Initialization
# Note: the number of hidden units l can be changed to an arbitrary value here,
# but p and k must match the training dataset used.

np.random.seed(1)
W_h, W_o = initialize_random_weights(p=4, l=4, k=1)

print("Initialized network:")
print_weights_and_predictions(W_h, W_o)

## (2) Outer loop (over epochs)
for t in range(tmax):
    ## (4) Inner loop (over training examples)
    for x, c in zip(xs, cs):
        # (x as a column vector)
        x = np.reshape(x, (len(x), 1))

        ## (5) Forward propagation
        y_h = np.vstack([1, sigmoid(W_h @ x)])
        y = sigmoid(W_o @ y_h)

        ## (6) Calculation of residual vector
        delta = c - y

        ## (7a) Backpropagation
        delta_o = delta * y * (1 - y)
        delta_h = ((W_o.T @ delta_o) * y_h * (1 - y_h))[1:]

        ## (7b) Weight update
        # note: with the dyadic product operator ⊗ as written in the pseudocode,
        # the transpose of the second operand is implicit. Numpy uses the same
        # @-operator for dyadic products as for matrix multiplications, so we
        # have to transpose explicitly.
        delta_W_h = eta * (delta_h @ x.T)
        delta_W_o = eta * (delta_o @ y_h.T)

        ## (8) Weight update (cont'd)
        W_h += delta_W_h
        W_o += delta_W_o

########################################################################
### Show results of training.

print(50*'*')
print(f"After {tmax} epochs:")
print_weights_and_predictions(W_h, W_o)
