"""
Neural Network Core Implementation
Supports multiple architectures and activation functions
"""
import numpy as np
from typing import List, Tuple, Callable


class ActivationFunctions:
    """Collection of activation functions and their derivatives"""
    
    @staticmethod
    def relu(x):
        return np.maximum(0, x)
    
    @staticmethod
    def relu_derivative(x):
        return (x > 0).astype(float)
    
    @staticmethod
    def sigmoid(x):
        # Clip values to prevent overflow
        x = np.clip(x, -500, 500)
        return 1 / (1 + np.exp(-x))
    
    @staticmethod
    def sigmoid_derivative(x):
        s = ActivationFunctions.sigmoid(x)
        return s * (1 - s)
    
    @staticmethod
    def tanh(x):
        return np.tanh(x)
    
    @staticmethod
    def tanh_derivative(x):
        return 1 - np.tanh(x) ** 2
    
    @staticmethod
    def leaky_relu(x, alpha=0.01):
        return np.where(x > 0, x, alpha * x)
    
    @staticmethod
    def leaky_relu_derivative(x, alpha=0.01):
        return np.where(x > 0, 1, alpha)
    
    @staticmethod
    def linear(x):
        return x
    
    @staticmethod
    def linear_derivative(x):
        return np.ones_like(x)
    
    @staticmethod
    def softmax(x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)


class NeuralNetwork:
    """
    Flexible Neural Network implementation supporting various architectures
    """
    
    def __init__(self, layer_sizes: List[int], activation_functions: List[str], 
                 learning_rate: float = 0.01, seed: int = None):
        """
        Initialize neural network
        
        Args:
            layer_sizes: List of integers representing neurons in each layer
            activation_functions: List of activation function names for each layer
            learning_rate: Learning rate for gradient descent
            seed: Random seed for reproducibility
        """
        if seed is not None:
            np.random.seed(seed)
        
        self.layer_sizes = layer_sizes
        self.num_layers = len(layer_sizes)
        self.learning_rate = learning_rate
        self.activation_names = activation_functions
        
        # Initialize weights and biases
        self.weights = []
        self.biases = []
        
        for i in range(self.num_layers - 1):
            # Xavier/He initialization
            if activation_functions[i] in ['relu', 'leaky_relu']:
                # He initialization for ReLU
                w = np.random.randn(layer_sizes[i], layer_sizes[i + 1]) * np.sqrt(2.0 / layer_sizes[i])
            else:
                # Xavier initialization for other activations
                w = np.random.randn(layer_sizes[i], layer_sizes[i + 1]) * np.sqrt(1.0 / layer_sizes[i])
            
            b = np.zeros((1, layer_sizes[i + 1]))
            self.weights.append(w)
            self.biases.append(b)
        
        # Storage for forward pass
        self.activations = []
        self.z_values = []
        
        # Training history
        self.loss_history = []
        self.weight_history = []
        self.gradient_history = []
    
    def get_activation_function(self, name: str) -> Tuple[Callable, Callable]:
        """Get activation function and its derivative"""
        activations = ActivationFunctions()
        
        if name == 'relu':
            return activations.relu, activations.relu_derivative
        elif name == 'sigmoid':
            return activations.sigmoid, activations.sigmoid_derivative
        elif name == 'tanh':
            return activations.tanh, activations.tanh_derivative
        elif name == 'leaky_relu':
            return activations.leaky_relu, activations.leaky_relu_derivative
        elif name == 'linear':
            return activations.linear, activations.linear_derivative
        elif name == 'softmax':
            return activations.softmax, activations.linear_derivative
        else:
            raise ValueError(f"Unknown activation function: {name}")
    
    def forward(self, X: np.ndarray, store_intermediates: bool = True) -> np.ndarray:
        """
        Forward propagation
        
        Args:
            X: Input data of shape (batch_size, input_features)
            store_intermediates: Whether to store intermediate values for visualization
        
        Returns:
            Output of the network
        """
        if store_intermediates:
            self.activations = [X]
            self.z_values = []
        
        current_activation = X
        
        for i in range(self.num_layers - 1):
            # Linear transformation
            z = np.dot(current_activation, self.weights[i]) + self.biases[i]
            
            # Apply activation function
            activation_func, _ = self.get_activation_function(self.activation_names[i])
            current_activation = activation_func(z)
            
            if store_intermediates:
                self.z_values.append(z)
                self.activations.append(current_activation)
        
        return current_activation
    
    def backward(self, X: np.ndarray, y: np.ndarray) -> List[np.ndarray]:
        """
        Backward propagation
        
        Args:
            X: Input data
            y: True labels
        
        Returns:
            List of gradients for weights
        """
        m = X.shape[0]
        
        # Initialize gradients
        weight_gradients = []
        bias_gradients = []
        
        # Calculate output layer error
        output_error = self.activations[-1] - y
        
        # Backpropagate through layers
        delta = output_error
        
        for i in range(self.num_layers - 2, -1, -1):
            # Calculate gradients
            dW = np.dot(self.activations[i].T, delta) / m
            db = np.sum(delta, axis=0, keepdims=True) / m
            
            weight_gradients.insert(0, dW)
            bias_gradients.insert(0, db)
            
            if i > 0:
                # Calculate error for previous layer
                delta = np.dot(delta, self.weights[i].T)
                
                # Apply activation derivative
                _, activation_derivative = self.get_activation_function(self.activation_names[i - 1])
                delta = delta * activation_derivative(self.z_values[i - 1])
        
        # Store gradient information for visualization
        self.gradient_history.append({
            'weight_gradients': [g.copy() for g in weight_gradients],
            'bias_gradients': [g.copy() for g in bias_gradients]
        })
        
        return weight_gradients, bias_gradients
    
    def update_weights(self, weight_gradients: List[np.ndarray], 
                       bias_gradients: List[np.ndarray]):
        """Update weights using gradient descent"""
        for i in range(len(self.weights)):
            self.weights[i] -= self.learning_rate * weight_gradients[i]
            self.biases[i] -= self.learning_rate * bias_gradients[i]
    
    def train_step(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Perform one training step
        
        Args:
            X: Input data
            y: True labels
        
        Returns:
            Loss value
        """
        # Forward pass
        predictions = self.forward(X, store_intermediates=True)
        
        # Calculate loss (Mean Squared Error)
        loss = np.mean((predictions - y) ** 2)
        
        # Backward pass
        weight_grads, bias_grads = self.backward(X, y)
        
        # Update weights
        self.update_weights(weight_grads, bias_grads)
        
        # Store for history
        self.loss_history.append(loss)
        self.weight_history.append([w.copy() for w in self.weights])
        
        return loss
    
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100, 
              verbose: bool = True) -> List[float]:
        """
        Train the neural network
        
        Args:
            X: Training data
            y: Training labels
            epochs: Number of training epochs
            verbose: Whether to print progress
        
        Returns:
            List of loss values for each epoch
        """
        losses = []
        
        for epoch in range(epochs):
            loss = self.train_step(X, y)
            losses.append(loss)
            
            if verbose and (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss:.6f}")
        
        return losses
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        return self.forward(X, store_intermediates=False)
    
    def get_network_state(self) -> dict:
        """Get current state of the network for visualization"""
        return {
            'weights': [w.copy() for w in self.weights],
            'biases': [b.copy() for b in self.biases],
            'activations': [a.copy() for a in self.activations] if self.activations else [],
            'z_values': [z.copy() for z in self.z_values] if self.z_values else [],
            'layer_sizes': self.layer_sizes,
            'activation_names': self.activation_names
        }
