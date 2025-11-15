# Installation Guide

## Quick Start

### Option 1: Using pip (Recommended)

```bash
# Navigate to the app directory
cd neural_network_app

# Install dependencies
pip install streamlit numpy matplotlib plotly pandas scikit-learn

# Run the app
streamlit run app.py
```

### Option 2: Using a Virtual Environment (Best Practice)

```bash
# Navigate to the app directory
cd neural_network_app

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Option 3: Using Conda

```bash
# Navigate to the app directory
cd neural_network_app

# Create conda environment
conda create -n neural_viz python=3.10

# Activate environment
conda activate neural_viz

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Troubleshooting

### Issue: pip install fails

**Solution 1**: Try installing packages individually:
```bash
pip install streamlit
pip install numpy
pip install matplotlib
pip install plotly
pip install pandas
pip install scikit-learn
```

**Solution 2**: Update pip first:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Solution 3**: Use conda for scientific packages:
```bash
conda install numpy matplotlib pandas scikit-learn
pip install streamlit plotly
```

### Issue: Streamlit doesn't start

**Check if Streamlit is installed**:
```bash
streamlit --version
```

**If not installed, install it**:
```bash
pip install streamlit
```

### Issue: Module not found errors

Make sure all dependencies are installed:
```bash
pip list | grep -E "streamlit|numpy|matplotlib|plotly|pandas|scikit"
```

If any are missing, install them:
```bash
pip install <missing-package>
```

### Issue: Permission denied

Use the `--user` flag:
```bash
pip install --user -r requirements.txt
```

## System Requirements

- **Python**: 3.8 or higher (3.10+ recommended)
- **RAM**: Minimum 2GB, 4GB+ recommended
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)
- **Internet**: Required for initial package installation

## Verifying Installation

Run this command to verify all packages are installed:

```bash
python -c "import streamlit, numpy, matplotlib, plotly, pandas, sklearn; print('✓ All packages installed successfully!')"
```

## Running the Application

Once installed, start the app with:

```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

## First Time Setup

1. The first time you run Streamlit, you may see a prompt about usage statistics
2. You can choose to opt-in or opt-out
3. The app should then load automatically

## Performance Tips

- For best performance, use Python 3.10 or 3.11
- Close other resource-intensive applications
- Use a modern browser with JavaScript enabled
- For large networks, be patient with visualization rendering

## Getting Help

If you encounter issues:

1. Check the [Streamlit documentation](https://docs.streamlit.io/)
2. Verify Python version: `python --version`
3. Verify package versions: `pip list`
4. Try creating a fresh virtual environment
5. Check the console for error messages

## Docker Installation (Advanced)

If you prefer Docker:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t neural-viz .
docker run -p 8501:8501 neural-viz
```

## Cloud Deployment

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

### Other Platforms
- **Heroku**: Use the provided requirements.txt
- **AWS/Azure/GCP**: Deploy as a container or web app
- **DigitalOcean**: Use App Platform with Python runtime

---

**Need more help?** Open an issue in the repository or consult the documentation in the app itself (see the "Learn More" tab).
