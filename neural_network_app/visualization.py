"""
Visualization utilities for neural network
"""
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def create_network_architecture_plot(layer_sizes, activation_names, weights=None, 
                                     neuron_activations=None, title="Neural Network Architecture"):
    """
    Create an interactive visualization of the neural network architecture
    
    Args:
        layer_sizes: List of layer sizes
        activation_names: List of activation function names
        weights: Optional weight matrices for connection visualization
        neuron_activations: Optional activation values for neurons
        title: Plot title
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    # Calculate positions for neurons
    max_neurons = max(layer_sizes)
    layer_spacing = 2.0
    neuron_spacing = 1.0
    
    neuron_positions = []
    neuron_values = []
    neuron_labels = []
    
    # Position neurons
    for layer_idx, num_neurons in enumerate(layer_sizes):
        x = layer_idx * layer_spacing
        offset = (max_neurons - num_neurons) * neuron_spacing / 2
        
        for neuron_idx in range(num_neurons):
            y = offset + neuron_idx * neuron_spacing
            neuron_positions.append((x, y))
            
            # Get neuron activation value if available
            if neuron_activations and layer_idx < len(neuron_activations):
                if len(neuron_activations[layer_idx].shape) == 1:
                    value = neuron_activations[layer_idx][neuron_idx]
                else:
                    value = neuron_activations[layer_idx][0, neuron_idx]
                neuron_values.append(value)
                neuron_labels.append(f"L{layer_idx}N{neuron_idx}<br>Value: {value:.3f}")
            else:
                neuron_values.append(0)
                neuron_labels.append(f"Layer {layer_idx}<br>Neuron {neuron_idx}")
    
    # Draw connections (edges)
    if weights is not None:
        edge_traces = []
        current_neuron = 0
        
        for layer_idx in range(len(layer_sizes) - 1):
            num_current = layer_sizes[layer_idx]
            num_next = layer_sizes[layer_idx + 1]
            
            weight_matrix = weights[layer_idx]
            
            # Normalize weights for color mapping
            w_min, w_max = weight_matrix.min(), weight_matrix.max()
            w_range = w_max - w_min if w_max != w_min else 1
            
            for i in range(num_current):
                for j in range(num_next):
                    src_idx = current_neuron + i
                    dst_idx = current_neuron + num_current + j
                    
                    x0, y0 = neuron_positions[src_idx]
                    x1, y1 = neuron_positions[dst_idx]
                    
                    weight = weight_matrix[i, j]
                    normalized_weight = (weight - w_min) / w_range
                    
                    # Color based on weight magnitude
                    if weight > 0:
                        color = f'rgba(0, 100, 255, {0.1 + 0.4 * normalized_weight})'
                    else:
                        color = f'rgba(255, 0, 0, {0.1 + 0.4 * normalized_weight})'
                    
                    # Line width based on absolute weight
                    width = 0.5 + 2 * abs(normalized_weight)
                    
                    fig.add_trace(go.Scatter(
                        x=[x0, x1],
                        y=[y0, y1],
                        mode='lines',
                        line=dict(color=color, width=width),
                        hoverinfo='text',
                        text=f'Weight: {weight:.3f}',
                        showlegend=False
                    ))
            
            current_neuron += num_current
    
    # Draw neurons
    x_coords = [pos[0] for pos in neuron_positions]
    y_coords = [pos[1] for pos in neuron_positions]
    
    # Color neurons based on activation values
    if neuron_activations:
        colors = neuron_values
        colorscale = 'RdYlBu'
    else:
        colors = ['lightblue'] * len(neuron_positions)
        colorscale = None
    
    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers',
        marker=dict(
            size=30,
            color=colors,
            colorscale=colorscale if colorscale else None,
            showscale=True if neuron_activations else False,
            colorbar=dict(title="Activation") if neuron_activations else None,
            line=dict(color='black', width=2)
        ),
        text=neuron_labels,
        hoverinfo='text',
        showlegend=False
    ))
    
    # Add layer labels
    for layer_idx, num_neurons in enumerate(layer_sizes):
        x = layer_idx * layer_spacing
        y = -0.5
        
        if layer_idx == 0:
            label = f"Input Layer<br>({num_neurons} neurons)"
        elif layer_idx == len(layer_sizes) - 1:
            label = f"Output Layer<br>({num_neurons} neurons)"
        else:
            label = f"Hidden Layer {layer_idx}<br>({num_neurons} neurons)<br>{activation_names[layer_idx - 1]}"
        
        fig.add_annotation(
            x=x, y=y,
            text=label,
            showarrow=False,
            font=dict(size=10),
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='black',
            borderwidth=1
        )
    
    fig.update_layout(
        title=title,
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        height=max(400, max_neurons * 60),
        margin=dict(l=20, r=20, t=60, b=60)
    )
    
    return fig


def create_loss_plot(loss_history, title="Training Loss Over Time"):
    """Create a plot showing loss over training epochs"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(range(len(loss_history))),
        y=loss_history,
        mode='lines',
        name='Loss',
        line=dict(color='red', width=2)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Epoch",
        yaxis_title="Loss (MSE)",
        hovermode='x',
        height=400
    )
    
    return fig


def create_activation_heatmap(activations, layer_idx, title="Neuron Activations"):
    """Create heatmap of neuron activations"""
    if not activations or layer_idx >= len(activations):
        return None
    
    data = activations[layer_idx]
    if len(data.shape) == 1:
        data = data.reshape(1, -1)
    
    fig = go.Figure(data=go.Heatmap(
        z=data,
        colorscale='RdYlBu',
        text=np.round(data, 3),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Activation Value")
    ))
    
    fig.update_layout(
        title=f"{title} - Layer {layer_idx}",
        xaxis_title="Neuron Index",
        yaxis_title="Sample",
        height=200 + data.shape[0] * 30
    )
    
    return fig


def create_weight_heatmap(weights, layer_idx, title="Weight Matrix"):
    """Create heatmap of weight matrix"""
    if not weights or layer_idx >= len(weights):
        return None
    
    weight_matrix = weights[layer_idx]
    
    fig = go.Figure(data=go.Heatmap(
        z=weight_matrix.T,
        colorscale='RdBu',
        zmid=0,
        text=np.round(weight_matrix.T, 3),
        texttemplate='%{text}',
        textfont={"size": 8},
        colorbar=dict(title="Weight Value")
    ))
    
    fig.update_layout(
        title=f"{title} - Layer {layer_idx} to {layer_idx + 1}",
        xaxis_title=f"Neurons in Layer {layer_idx}",
        yaxis_title=f"Neurons in Layer {layer_idx + 1}",
        height=400
    )
    
    return fig


def create_gradient_plot(gradient_history, layer_idx=0, weight_idx=(0, 0)):
    """Create plot showing gradient changes over time"""
    if not gradient_history:
        return None
    
    gradients = []
    for grad_dict in gradient_history:
        if layer_idx < len(grad_dict['weight_gradients']):
            w_grad = grad_dict['weight_gradients'][layer_idx]
            if weight_idx[0] < w_grad.shape[0] and weight_idx[1] < w_grad.shape[1]:
                gradients.append(w_grad[weight_idx[0], weight_idx[1]])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(range(len(gradients))),
        y=gradients,
        mode='lines+markers',
        name='Gradient',
        line=dict(color='green', width=2)
    ))
    
    fig.update_layout(
        title=f"Gradient History - Weight [{weight_idx[0]}, {weight_idx[1]}] in Layer {layer_idx}",
        xaxis_title="Training Step",
        yaxis_title="Gradient Value",
        hovermode='x',
        height=300
    )
    
    return fig


def create_activation_function_plot(activation_name):
    """Create plot showing the activation function curve"""
    x = np.linspace(-5, 5, 200)
    
    from neural_network import ActivationFunctions
    act_funcs = ActivationFunctions()
    
    if activation_name == 'relu':
        y = act_funcs.relu(x)
        y_derivative = act_funcs.relu_derivative(x)
    elif activation_name == 'sigmoid':
        y = act_funcs.sigmoid(x)
        y_derivative = act_funcs.sigmoid_derivative(x)
    elif activation_name == 'tanh':
        y = act_funcs.tanh(x)
        y_derivative = act_funcs.tanh_derivative(x)
    elif activation_name == 'leaky_relu':
        y = act_funcs.leaky_relu(x)
        y_derivative = act_funcs.leaky_relu_derivative(x)
    elif activation_name == 'linear':
        y = act_funcs.linear(x)
        y_derivative = act_funcs.linear_derivative(x)
    else:
        return None
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(f"{activation_name.upper()} Function", 
                       f"{activation_name.upper()} Derivative")
    )
    
    fig.add_trace(
        go.Scatter(x=x, y=y, mode='lines', name='Function', 
                  line=dict(color='blue', width=2)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=x, y=y_derivative, mode='lines', name='Derivative',
                  line=dict(color='red', width=2)),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text="Input (x)", row=1, col=1)
    fig.update_xaxes(title_text="Input (x)", row=1, col=2)
    fig.update_yaxes(title_text="Output", row=1, col=1)
    fig.update_yaxes(title_text="Derivative", row=1, col=2)
    
    fig.update_layout(height=400, showlegend=False,
                     title_text=f"Activation Function: {activation_name.upper()}")
    
    return fig


def create_data_flow_animation(network_state, input_data):
    """Create animation showing data flow through network"""
    # This would create a more complex animation
    # For now, we'll use the static visualization
    pass
