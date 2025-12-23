# Quick Reference Guide

## 🎯 Common Tasks

### Starting the App
```bash
cd neural_network_app
streamlit run app.py
```

### Creating Your First Network
1. Select "Two-Layer Network"
2. Input: 2, Hidden: 4, Output: 1
3. Activation: ReLU (hidden), Sigmoid (output)
4. Learning Rate: 0.01
5. Click "Initialize Network"

### Training
1. Select "XOR Problem" dataset
2. Choose training mode (Step-by-Step recommended first)
3. Click "Train One Epoch" or "Start Training"
4. Watch loss decrease!

## 🔧 Configuration Options

### Network Types
| Type | Layers | Best For |
|------|--------|----------|
| Perceptron | Input → Output | Linear problems |
| Two-Layer | Input → Hidden → Output | XOR, simple non-linear |
| Three-Layer | Input → Hidden₁ → Hidden₂ → Output | Complex patterns |
| Custom | User-defined | Any task |

### Activation Functions
| Function | Range | Best For |
|----------|-------|----------|
| ReLU | [0, ∞) | Hidden layers (default) |
| Sigmoid | (0, 1) | Binary classification output |
| Tanh | (-1, 1) | Hidden layers (zero-centered) |
| Leaky ReLU | (-∞, ∞) | Preventing dead neurons |
| Linear | (-∞, ∞) | Regression output |

### Learning Rates
| Rate | Effect | Use When |
|------|--------|----------|
| 0.001 - 0.01 | Stable, slow | Large networks, fine-tuning |
| 0.01 - 0.1 | Balanced | Most cases (recommended) |
| 0.1 - 1.0 | Fast, unstable | Small networks, experimentation |

### Datasets
| Dataset | Type | Difficulty | Neurons Needed |
|---------|------|------------|----------------|
| Linear Regression | Regression | Easy | 2-4 |
| Binary Classification | Classification | Easy | 2-4 |
| Moons | Classification | Medium | 4-8 |
| Circles | Classification | Medium | 4-8 |
| XOR | Classification | Medium | 4-8 |

## 📊 Interpreting Visualizations

### Network Architecture
- **Blue connections**: Positive weights
- **Red connections**: Negative weights
- **Thick lines**: Strong connections
- **Thin lines**: Weak connections
- **Colored neurons**: Activation values

### Loss Curve
- **Decreasing**: Network is learning ✓
- **Flat**: Stuck in local minimum
- **Increasing**: Learning rate too high
- **Oscillating**: Learning rate too high

### Weight Heatmaps
- **Blue**: Positive weights
- **Red**: Negative weights
- **White**: Near-zero weights
- **Intensity**: Weight magnitude

### Activation Heatmaps
- **Blue**: Low activation
- **Red**: High activation
- **Patterns**: What network "sees"

## 🎓 Learning Scenarios

### Scenario 1: Understanding Perceptron Limitations
```
Network: Perceptron (2 → 1)
Dataset: XOR Problem
Activation: Sigmoid
Epochs: 100
Expected: High final loss (can't solve XOR)
```

### Scenario 2: Solving XOR
```
Network: Two-Layer (2 → 4 → 1)
Dataset: XOR Problem
Activation: ReLU, Sigmoid
Learning Rate: 0.01
Epochs: 100
Expected: Low final loss (solves XOR)
```

### Scenario 3: Effect of Learning Rate
```
Try 3 runs with same network but different rates:
- 0.001: Very slow learning
- 0.01: Good balance
- 0.5: Unstable, oscillating
```

### Scenario 4: Activation Function Comparison
```
Same network, same dataset, different activations:
- ReLU: Fast, effective
- Sigmoid: Slower, can vanish
- Tanh: Middle ground
```

### Scenario 5: Network Depth
```
Same dataset, increasing depth:
- 2 → 1: Simple, may fail
- 2 → 4 → 1: Better
- 2 → 8 → 4 → 1: Best for complex patterns
```

## 🐛 Troubleshooting

### Problem: Loss not decreasing
**Solutions:**
- Increase learning rate
- Add more hidden neurons
- Try different activation function
- Train for more epochs
- Check if problem is solvable with current architecture

### Problem: Loss oscillating
**Solutions:**
- Decrease learning rate
- Use step-by-step training to observe
- Check network isn't too complex for data

### Problem: Training very slow
**Solutions:**
- Increase learning rate slightly
- Reduce network size
- Use ReLU instead of Sigmoid/Tanh
- Reduce number of epochs

### Problem: Network not learning anything
**Solutions:**
- Check activation functions (avoid all linear)
- Verify dataset is loaded correctly
- Try different initialization (re-initialize)
- Ensure learning rate isn't too small

## 💡 Tips & Best Practices

### General Tips
1. **Start simple**: Begin with 2-layer networks
2. **Visualize often**: Check visualizations after training
3. **Use step-by-step**: Understand gradual changes
4. **Compare**: Try different configurations
5. **Document**: Note what works and what doesn't

### For Learning
1. Start with Perceptron on linear data
2. Try Perceptron on XOR (see it fail)
3. Add hidden layer (see it succeed)
4. Experiment with all activation functions
5. Try different learning rates
6. Build custom networks

### For Teaching
1. Show forward propagation visually
2. Demonstrate backpropagation step-by-step
3. Compare activation functions side-by-side
4. Illustrate gradient descent
5. Use custom inputs for prediction

### For Development
1. Prototype architectures quickly
2. Test activation function choices
3. Understand gradient behavior
4. Debug training issues
5. Validate concepts

## 🔑 Keyboard Shortcuts (in Streamlit)

- `R`: Rerun app
- `C`: Clear cache
- `Ctrl+Enter`: Execute code cell (if any)

## 📝 Common Parameter Combinations

### Beginner-Friendly
```
Network: 2 → 4 → 1
Activations: relu, sigmoid
Learning Rate: 0.01
Dataset: XOR
Epochs: 100
```

### Intermediate
```
Network: 2 → 8 → 4 → 1
Activations: relu, relu, sigmoid
Learning Rate: 0.01
Dataset: Moons or Circles
Epochs: 200
```

### Advanced
```
Network: Custom (e.g., 3 → 16 → 8 → 2)
Activations: Mix of relu, tanh, leaky_relu
Learning Rate: Adjust based on performance
Dataset: Any
Epochs: Variable
```

## 📚 Further Reading

### In the App
- **Learn More Tab**: Comprehensive explanations
- **Network Architecture Tab**: Visual understanding
- **Training Tab**: Process details
- **Detailed Analysis Tab**: Advanced metrics

### External Resources
- Neural Networks and Deep Learning (Nielsen)
- Deep Learning (Goodfellow et al.)
- Coursera Deep Learning Specialization
- Fast.ai Practical Deep Learning

## 🎯 Success Criteria

### You're Ready When You Can:
- [ ] Explain what each layer does
- [ ] Choose appropriate activation functions
- [ ] Set reasonable learning rates
- [ ] Interpret loss curves
- [ ] Understand why network depth matters
- [ ] Debug common training issues
- [ ] Design custom architectures
- [ ] Explain backpropagation visually

---

**Need Help?** Check the full README.md or the "Learn More" tab in the app!
