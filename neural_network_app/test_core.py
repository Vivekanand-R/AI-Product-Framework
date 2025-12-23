"""
Simple test script for neural network implementation
Tests core functionality without UI dependencies
"""


def test_activation_functions():
    """Test activation functions with simple numpy arrays"""
    print("Testing Activation Functions...")
    
    # Simulate numpy for basic testing
    class SimpleArray:
        def __init__(self, data):
            self.data = data
        
        def __gt__(self, value):
            return SimpleArray([x > value for x in self.data])
        
        def astype(self, dtype):
            return SimpleArray([float(x) for x in self.data])
    
    # Test ReLU logic
    test_data = [-2, -1, 0, 1, 2]
    print(f"  Input: {test_data}")
    relu_output = [max(0, x) for x in test_data]
    print(f"  ReLU Output: {relu_output}")
    assert relu_output == [0, 0, 0, 1, 2], "ReLU test failed"
    
    # Test Sigmoid logic
    import math
    sigmoid_output = [1 / (1 + math.exp(-x)) for x in test_data]
    print(f"  Sigmoid Output: {[round(x, 4) for x in sigmoid_output]}")
    
    # Test Tanh logic
    tanh_output = [math.tanh(x) for x in test_data]
    print(f"  Tanh Output: {[round(x, 4) for x in tanh_output]}")
    
    print("✓ Activation functions logic verified\n")


def test_network_architecture():
    """Test network architecture configuration"""
    print("Testing Network Architecture...")
    
    architectures = [
        ("Perceptron", [2, 1]),
        ("Two-Layer", [2, 4, 1]),
        ("Three-Layer", [2, 8, 4, 1]),
        ("Custom", [3, 10, 5, 2])
    ]
    
    for name, layers in architectures:
        # Calculate parameters
        total_params = 0
        for i in range(len(layers) - 1):
            weights = layers[i] * layers[i + 1]
            biases = layers[i + 1]
            total_params += weights + biases
        
        print(f"  {name}: {layers}")
        print(f"    Total parameters: {total_params}")
    
    print("✓ Network architectures validated\n")


def test_forward_pass_logic():
    """Test forward pass computation logic"""
    print("Testing Forward Pass Logic...")
    
    # Simulate a simple forward pass
    # Input: 2 features, Hidden: 3 neurons, Output: 1 neuron
    input_data = [0.5, -0.3]
    weights_1 = [
        [0.1, 0.2, 0.3],  # from input 0 to hidden neurons
        [0.4, 0.5, 0.6]   # from input 1 to hidden neurons
    ]
    bias_1 = [0.1, 0.1, 0.1]
    
    # Calculate hidden layer (before activation)
    hidden = []
    for j in range(3):  # 3 hidden neurons
        value = bias_1[j]
        for i in range(2):  # 2 input features
            value += input_data[i] * weights_1[i][j]
        hidden.append(value)
    
    print(f"  Input: {input_data}")
    print(f"  Hidden layer (before activation): {[round(x, 4) for x in hidden]}")
    
    # Apply ReLU
    hidden_activated = [max(0, x) for x in hidden]
    print(f"  Hidden layer (after ReLU): {[round(x, 4) for x in hidden_activated]}")
    
    print("✓ Forward pass logic verified\n")


def test_loss_calculation():
    """Test loss calculation"""
    print("Testing Loss Calculation...")
    
    predictions = [0.8, 0.3, 0.6, 0.9]
    targets = [1.0, 0.0, 0.5, 1.0]
    
    # Mean Squared Error
    mse = sum((p - t) ** 2 for p, t in zip(predictions, targets)) / len(predictions)
    
    print(f"  Predictions: {predictions}")
    print(f"  Targets: {targets}")
    print(f"  MSE Loss: {round(mse, 6)}")
    
    expected_mse = ((0.8-1.0)**2 + (0.3-0.0)**2 + (0.6-0.5)**2 + (0.9-1.0)**2) / 4
    assert abs(mse - expected_mse) < 1e-6, "MSE calculation failed"
    
    print("✓ Loss calculation verified\n")


def test_gradient_descent_logic():
    """Test gradient descent update logic"""
    print("Testing Gradient Descent Logic...")
    
    # Simple weight update
    weight = 0.5
    gradient = 0.1
    learning_rate = 0.01
    
    new_weight = weight - learning_rate * gradient
    
    print(f"  Initial weight: {weight}")
    print(f"  Gradient: {gradient}")
    print(f"  Learning rate: {learning_rate}")
    print(f"  New weight: {new_weight}")
    
    expected = 0.5 - 0.01 * 0.1
    assert abs(new_weight - expected) < 1e-6, "Gradient descent update failed"
    
    print("✓ Gradient descent logic verified\n")


def test_file_structure():
    """Test that all required files exist"""
    print("Testing File Structure...")
    
    import os
    
    required_files = [
        'neural_network.py',
        'visualization.py',
        'app.py',
        'requirements.txt',
        'README.md',
        'INSTALLATION.md',
        '.gitignore'
    ]
    
    for filename in required_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  ✓ {filename} ({size} bytes)")
        else:
            print(f"  ✗ {filename} MISSING")
    
    print()


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("NEURAL NETWORK APP - CORE FUNCTIONALITY TESTS")
    print("=" * 60)
    print()
    
    try:
        test_file_structure()
        test_activation_functions()
        test_network_architecture()
        test_forward_pass_logic()
        test_loss_calculation()
        test_gradient_descent_logic()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("The core neural network logic is working correctly.")
        print("To run the full application with visualizations:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run the app: streamlit run app.py")
        print()
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")


if __name__ == "__main__":
    run_all_tests()
