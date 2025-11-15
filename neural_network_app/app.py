"""
Interactive Neural Network Visualization App
A user-friendly application to understand neural networks visually
"""
import streamlit as st
import numpy as np
import pandas as pd
from neural_network import NeuralNetwork
from visualization import (
    create_network_architecture_plot,
    create_loss_plot,
    create_activation_heatmap,
    create_weight_heatmap,
    create_gradient_plot,
    create_activation_function_plot
)
from sklearn.datasets import make_classification, make_regression, make_moons, make_circles
from sklearn.preprocessing import StandardScaler
import time


# Page configuration
st.set_page_config(
    page_title="Neural Network Visualizer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'network' not in st.session_state:
    st.session_state.network = None
if 'training_data' not in st.session_state:
    st.session_state.training_data = None
if 'training_labels' not in st.session_state:
    st.session_state.training_labels = None
if 'is_trained' not in st.session_state:
    st.session_state.is_trained = False
if 'current_epoch' not in st.session_state:
    st.session_state.current_epoch = 0


def generate_dataset(dataset_type, n_samples, noise):
    """Generate synthetic dataset for training"""
    if dataset_type == "Linear Regression":
        X, y = make_regression(n_samples=n_samples, n_features=2, noise=noise, random_state=42)
        y = y.reshape(-1, 1)
    elif dataset_type == "Binary Classification":
        X, y = make_classification(n_samples=n_samples, n_features=2, n_redundant=0, 
                                   n_informative=2, n_clusters_per_class=1, 
                                   random_state=42)
        y = y.reshape(-1, 1)
    elif dataset_type == "Moons (Non-linear)":
        X, y = make_moons(n_samples=n_samples, noise=noise/10, random_state=42)
        y = y.reshape(-1, 1)
    elif dataset_type == "Circles (Non-linear)":
        X, y = make_circles(n_samples=n_samples, noise=noise/10, factor=0.5, random_state=42)
        y = y.reshape(-1, 1)
    else:
        # Custom XOR problem
        X = np.random.randn(n_samples, 2)
        y = ((X[:, 0] > 0) != (X[:, 1] > 0)).astype(int).reshape(-1, 1)
    
    # Normalize features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    return X, y


def main():
    # Header
    st.markdown('<h1 class="main-header">🧠 Interactive Neural Network Visualizer</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <b>Welcome!</b> This interactive application helps you understand how neural networks work.
    You can configure network architecture, choose activation functions, train the network,
    and visualize the entire process in real-time.
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Network Configuration")
    
    # Network type selection
    network_type = st.sidebar.selectbox(
        "Select Network Type",
        ["Perceptron (Single Layer)", "Two-Layer Network", "Three-Layer Network", "Custom Architecture"],
        help="Choose the type of neural network architecture"
    )
    
    # Determine layer configuration based on network type
    if network_type == "Perceptron (Single Layer)":
        input_size = st.sidebar.number_input("Input Features", min_value=1, max_value=10, value=2)
        output_size = st.sidebar.number_input("Output Size", min_value=1, max_value=10, value=1)
        layer_sizes = [input_size, output_size]
        num_hidden_layers = 0
    
    elif network_type == "Two-Layer Network":
        input_size = st.sidebar.number_input("Input Features", min_value=1, max_value=10, value=2)
        hidden_size = st.sidebar.number_input("Hidden Layer Size", min_value=1, max_value=50, value=4)
        output_size = st.sidebar.number_input("Output Size", min_value=1, max_value=10, value=1)
        layer_sizes = [input_size, hidden_size, output_size]
        num_hidden_layers = 1
    
    elif network_type == "Three-Layer Network":
        input_size = st.sidebar.number_input("Input Features", min_value=1, max_value=10, value=2)
        hidden1_size = st.sidebar.number_input("Hidden Layer 1 Size", min_value=1, max_value=50, value=8)
        hidden2_size = st.sidebar.number_input("Hidden Layer 2 Size", min_value=1, max_value=50, value=4)
        output_size = st.sidebar.number_input("Output Size", min_value=1, max_value=10, value=1)
        layer_sizes = [input_size, hidden1_size, hidden2_size, output_size]
        num_hidden_layers = 2
    
    else:  # Custom
        input_size = st.sidebar.number_input("Input Features", min_value=1, max_value=10, value=2)
        num_hidden_layers = st.sidebar.number_input("Number of Hidden Layers", min_value=1, max_value=5, value=2)
        layer_sizes = [input_size]
        for i in range(num_hidden_layers):
            size = st.sidebar.number_input(f"Hidden Layer {i+1} Size", min_value=1, max_value=50, value=8, key=f"hidden_{i}")
            layer_sizes.append(size)
        output_size = st.sidebar.number_input("Output Size", min_value=1, max_value=10, value=1)
        layer_sizes.append(output_size)
    
    # Activation function selection
    st.sidebar.subheader("Activation Functions")
    activation_options = ["relu", "sigmoid", "tanh", "leaky_relu", "linear"]
    
    activation_functions = []
    for i in range(len(layer_sizes) - 1):
        if i < len(layer_sizes) - 2:
            default_activation = "relu"
            label = f"Hidden Layer {i+1} Activation"
        else:
            default_activation = "sigmoid"
            label = "Output Layer Activation"
        
        activation = st.sidebar.selectbox(
            label,
            activation_options,
            index=activation_options.index(default_activation),
            key=f"activation_{i}",
            help=f"Activation function for layer {i+1}"
        )
        activation_functions.append(activation)
    
    # Training parameters
    st.sidebar.subheader("Training Parameters")
    learning_rate = st.sidebar.slider("Learning Rate", 0.001, 1.0, 0.01, 0.001, 
                                      help="Step size for gradient descent")
    epochs = st.sidebar.slider("Training Epochs", 10, 1000, 100, 10,
                               help="Number of training iterations")
    
    # Dataset selection
    st.sidebar.subheader("Dataset")
    dataset_type = st.sidebar.selectbox(
        "Select Dataset",
        ["Linear Regression", "Binary Classification", "Moons (Non-linear)", 
         "Circles (Non-linear)", "XOR Problem"],
        help="Choose a dataset for training"
    )
    
    n_samples = st.sidebar.slider("Number of Samples", 50, 500, 200, 50)
    noise = st.sidebar.slider("Noise Level", 0.0, 20.0, 5.0, 1.0)
    
    # Custom input for prediction
    st.sidebar.subheader("Custom Input for Prediction")
    custom_inputs = []
    for i in range(layer_sizes[0]):
        val = st.sidebar.number_input(f"Input Feature {i+1}", value=0.0, format="%.3f", key=f"custom_input_{i}")
        custom_inputs.append(val)
    
    # Main content area with tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Network Architecture", 
        "🎯 Training", 
        "📈 Visualization", 
        "🔬 Detailed Analysis",
        "📚 Learn More"
    ])
    
    # Tab 1: Network Architecture
    with tab1:
        st.header("Network Architecture")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Current Configuration")
            st.write(f"**Network Type:** {network_type}")
            st.write(f"**Layer Sizes:** {' → '.join(map(str, layer_sizes))}")
            st.write(f"**Activation Functions:** {', '.join(activation_functions)}")
            st.write(f"**Learning Rate:** {learning_rate}")
            
            # Display activation function plots
            st.subheader("Activation Functions")
            for i, act_name in enumerate(set(activation_functions)):
                fig = create_activation_function_plot(act_name)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Network Summary")
            
            # Calculate total parameters
            total_params = 0
            for i in range(len(layer_sizes) - 1):
                weights = layer_sizes[i] * layer_sizes[i + 1]
                biases = layer_sizes[i + 1]
                total_params += weights + biases
            
            st.metric("Total Parameters", total_params)
            st.metric("Total Layers", len(layer_sizes))
            st.metric("Hidden Layers", num_hidden_layers)
            
            # Parameter breakdown
            st.subheader("Parameters per Layer")
            for i in range(len(layer_sizes) - 1):
                weights = layer_sizes[i] * layer_sizes[i + 1]
                biases = layer_sizes[i + 1]
                st.write(f"Layer {i} → {i+1}: {weights + biases}")
        
        # Initialize network button
        if st.button("🔧 Initialize Network", type="primary"):
            st.session_state.network = NeuralNetwork(
                layer_sizes=layer_sizes,
                activation_functions=activation_functions,
                learning_rate=learning_rate,
                seed=42
            )
            st.success("✅ Network initialized successfully!")
            st.session_state.is_trained = False
            st.session_state.current_epoch = 0
            
            # Generate training data
            X, y = generate_dataset(dataset_type, n_samples, noise)
            st.session_state.training_data = X
            st.session_state.training_labels = y
        
        # Visualize architecture
        if st.session_state.network is not None:
            st.subheader("Network Architecture Visualization")
            state = st.session_state.network.get_network_state()
            fig = create_network_architecture_plot(
                state['layer_sizes'],
                state['activation_names'],
                state['weights'],
                state['activations'] if state['activations'] else None
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Training
    with tab2:
        st.header("Training Process")
        
        if st.session_state.network is None:
            st.warning("⚠️ Please initialize the network first in the 'Network Architecture' tab.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Dataset Information")
                st.write(f"**Dataset Type:** {dataset_type}")
                st.write(f"**Number of Samples:** {n_samples}")
                st.write(f"**Input Shape:** {st.session_state.training_data.shape}")
                st.write(f"**Output Shape:** {st.session_state.training_labels.shape}")
                
                # Show sample data
                st.subheader("Sample Data Points")
                sample_df = pd.DataFrame(
                    st.session_state.training_data[:5],
                    columns=[f"Feature {i+1}" for i in range(st.session_state.training_data.shape[1])]
                )
                sample_df['Target'] = st.session_state.training_labels[:5].flatten()
                st.dataframe(sample_df)
            
            with col2:
                st.subheader("Training Controls")
                
                training_mode = st.radio(
                    "Training Mode",
                    ["Full Training", "Step-by-Step Training"],
                    help="Choose whether to train all epochs at once or step by step"
                )
                
                if training_mode == "Full Training":
                    if st.button("🚀 Start Training", type="primary"):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for epoch in range(epochs):
                            loss = st.session_state.network.train_step(
                                st.session_state.training_data,
                                st.session_state.training_labels
                            )
                            
                            progress = (epoch + 1) / epochs
                            progress_bar.progress(progress)
                            status_text.text(f"Epoch {epoch + 1}/{epochs} - Loss: {loss:.6f}")
                            
                        st.session_state.is_trained = True
                        st.session_state.current_epoch = epochs
                        st.success("✅ Training completed!")
                
                else:  # Step-by-step
                    if st.button("➡️ Train One Epoch"):
                        if st.session_state.current_epoch < epochs:
                            loss = st.session_state.network.train_step(
                                st.session_state.training_data,
                                st.session_state.training_labels
                            )
                            st.session_state.current_epoch += 1
                            st.info(f"Epoch {st.session_state.current_epoch}/{epochs} - Loss: {loss:.6f}")
                            
                            if st.session_state.current_epoch >= epochs:
                                st.session_state.is_trained = True
                                st.success("✅ Training completed!")
                        else:
                            st.warning("Training already completed!")
                    
                    st.write(f"**Current Epoch:** {st.session_state.current_epoch}/{epochs}")
            
            # Show training progress
            if st.session_state.network.loss_history:
                st.subheader("Training Progress")
                fig = create_loss_plot(st.session_state.network.loss_history)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show current loss
                current_loss = st.session_state.network.loss_history[-1]
                st.metric("Current Loss", f"{current_loss:.6f}")
    
    # Tab 3: Visualization
    with tab3:
        st.header("Real-Time Network Visualization")
        
        if st.session_state.network is None:
            st.warning("⚠️ Please initialize the network first.")
        else:
            # Perform forward pass with training data to get activations
            if st.session_state.training_data is not None:
                _ = st.session_state.network.forward(st.session_state.training_data[:1])
            
            state = st.session_state.network.get_network_state()
            
            # Network with activations
            st.subheader("Network with Neuron Activations")
            fig = create_network_architecture_plot(
                state['layer_sizes'],
                state['activation_names'],
                state['weights'],
                state['activations'] if state['activations'] else None,
                title="Neural Network with Activations"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Weight matrices
            st.subheader("Weight Matrices")
            num_weight_layers = len(state['weights'])
            cols = st.columns(min(3, num_weight_layers))
            
            for i in range(num_weight_layers):
                with cols[i % 3]:
                    fig = create_weight_heatmap(state['weights'], i)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            
            # Activation heatmaps
            if state['activations']:
                st.subheader("Neuron Activation Heatmaps")
                for i in range(len(state['activations'])):
                    fig = create_activation_heatmap(state['activations'], i)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: Detailed Analysis
    with tab4:
        st.header("Detailed Network Analysis")
        
        if st.session_state.network is None or not st.session_state.is_trained:
            st.warning("⚠️ Please initialize and train the network first.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Gradient Analysis")
                if st.session_state.network.gradient_history:
                    layer_to_analyze = st.selectbox(
                        "Select Layer",
                        range(len(st.session_state.network.weights)),
                        format_func=lambda x: f"Layer {x} → {x+1}"
                    )
                    
                    w_shape = st.session_state.network.weights[layer_to_analyze].shape
                    weight_i = st.slider("Weight Row", 0, w_shape[0]-1, 0)
                    weight_j = st.slider("Weight Column", 0, w_shape[1]-1, 0)
                    
                    fig = create_gradient_plot(
                        st.session_state.network.gradient_history,
                        layer_to_analyze,
                        (weight_i, weight_j)
                    )
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Custom Input Prediction")
                
                custom_input_array = np.array(custom_inputs).reshape(1, -1)
                
                if st.button("🔮 Make Prediction"):
                    prediction = st.session_state.network.predict(custom_input_array)
                    st.success(f"**Prediction:** {prediction[0, 0]:.4f}")
                    
                    # Show activations for this input
                    _ = st.session_state.network.forward(custom_input_array)
                    state = st.session_state.network.get_network_state()
                    
                    st.subheader("Network State for Custom Input")
                    fig = create_network_architecture_plot(
                        state['layer_sizes'],
                        state['activation_names'],
                        state['weights'],
                        state['activations'],
                        title="Network State for Custom Input"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Training statistics
            st.subheader("Training Statistics")
            if st.session_state.network.loss_history:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Initial Loss", f"{st.session_state.network.loss_history[0]:.6f}")
                with col2:
                    st.metric("Final Loss", f"{st.session_state.network.loss_history[-1]:.6f}")
                with col3:
                    improvement = (st.session_state.network.loss_history[0] - 
                                 st.session_state.network.loss_history[-1])
                    st.metric("Loss Reduction", f"{improvement:.6f}")
                with col4:
                    if len(st.session_state.network.loss_history) > 1:
                        percent_improvement = (improvement / st.session_state.network.loss_history[0]) * 100
                        st.metric("Improvement %", f"{percent_improvement:.2f}%")
    
    # Tab 5: Learn More
    with tab5:
        st.header("📚 Understanding Neural Networks")
        
        st.markdown("""
        ### What is a Neural Network?
        
        A neural network is a computational model inspired by biological neural networks. 
        It consists of interconnected nodes (neurons) organized in layers that process information.
        
        ### Key Components:
        
        #### 1. **Neurons (Nodes)**
        - The basic computational units
        - Each neuron receives inputs, applies weights, adds bias, and uses an activation function
        
        #### 2. **Layers**
        - **Input Layer**: Receives the initial data
        - **Hidden Layers**: Perform intermediate computations and feature extraction
        - **Output Layer**: Produces the final prediction
        
        #### 3. **Weights and Biases**
        - **Weights**: Control the strength of connections between neurons
        - **Biases**: Allow shifting the activation function
        - Both are learned during training
        
        #### 4. **Activation Functions**
        - **ReLU** (Rectified Linear Unit): f(x) = max(0, x) - Fast and effective for deep networks
        - **Sigmoid**: f(x) = 1/(1+e^(-x)) - Outputs between 0 and 1, good for probabilities
        - **Tanh**: f(x) = tanh(x) - Outputs between -1 and 1, zero-centered
        - **Leaky ReLU**: Allows small negative values, prevents "dying ReLU" problem
        - **Linear**: No transformation, used for regression outputs
        
        ### Training Process:
        
        #### 1. **Forward Propagation**
        - Input data flows through the network
        - Each layer transforms the data using weights, biases, and activation functions
        - Final output is the prediction
        
        #### 2. **Loss Calculation**
        - Measures how far predictions are from true values
        - Common loss: Mean Squared Error (MSE) = average of (prediction - truth)²
        
        #### 3. **Backpropagation**
        - Calculates gradients of loss with respect to each weight
        - Uses chain rule to propagate errors backward through the network
        
        #### 4. **Gradient Descent**
        - Updates weights to minimize loss
        - New weight = Old weight - Learning Rate × Gradient
        
        ### Network Types:
        
        #### **Perceptron (Single Layer)**
        - Simplest form, only input and output layers
        - Can only solve linearly separable problems
        
        #### **Multi-Layer Networks**
        - Include hidden layers
        - Can learn complex, non-linear patterns
        - More layers = deeper network = more expressive power
        
        ### Tips for Good Performance:
        
        1. **Learning Rate**: 
           - Too high: Training becomes unstable
           - Too low: Training is very slow
           - Typical range: 0.001 to 0.1
        
        2. **Network Architecture**:
           - Start simple, add complexity if needed
           - More neurons can capture more patterns but may overfit
        
        3. **Activation Functions**:
           - ReLU is usually a good default for hidden layers
           - Use sigmoid/softmax for classification outputs
           - Use linear for regression outputs
        
        4. **Training Data**:
           - More data generally leads to better learning
           - Data should be normalized/standardized
        
        ### Common Challenges:
        
        - **Overfitting**: Network memorizes training data but fails on new data
        - **Underfitting**: Network is too simple to capture patterns
        - **Vanishing Gradients**: Gradients become too small in deep networks
        - **Exploding Gradients**: Gradients become too large, causing instability
        
        ### Extensions and Future Customizations:
        
        This app can be extended to include:
        - Convolutional layers for image processing
        - Recurrent layers for sequence data
        - Dropout and regularization techniques
        - Different optimizers (Adam, RMSprop, etc.)
        - Batch normalization
        - More complex datasets
        - Model saving and loading
        - Real-time data input
        
        ### Try It Out!
        
        1. Go to the "Network Architecture" tab
        2. Configure your network
        3. Initialize it
        4. Switch to "Training" tab to train
        5. Watch the "Visualization" tab to see it learn!
        """)
        
        st.info("""
        💡 **Pro Tip**: Start with a simple two-layer network with 4-8 hidden neurons, 
        ReLU activation, and a learning rate of 0.01. Train for 100 epochs and observe 
        how the network learns!
        """)


if __name__ == "__main__":
    main()
