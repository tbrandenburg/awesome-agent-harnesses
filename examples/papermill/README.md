# Papermill Environment

A complete Jupyter notebook execution environment with Papermill for parameterized notebook execution.

## Quick Start

### 1. Activate Environment
```bash
cd examples/papermill
./activate.sh
```
This will:
- Create/activate the virtual environment
- Install all required packages
- Install the bash kernel for Jupyter
- Open a new shell with the environment active

### 2. Alternative Manual Setup
```bash
cd examples/papermill

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install packages
pip install -r requirements.txt

# Install bash kernel
python -m bash_kernel.install
```

## What's Included

### Core Tools
- **Papermill** - Parameterize and execute Jupyter notebooks
- **JupyterLab** - Modern web-based interactive development environment
- **Jupyter Notebook** - Classic notebook interface
- **nbclient** - Programmatic notebook execution

### Kernels
- **Python kernel** (ipykernel) - Default Python execution
- **Bash kernel** - Execute shell commands in notebooks

### Additional Libraries
- **matplotlib** - Plotting and visualization
- **pandas** - Data analysis and manipulation
- **numpy** - Numerical computing
- **ipywidgets** - Interactive widgets for notebooks

## Usage Examples

### Basic Papermill Execution
```bash
# Execute a notebook with parameters
papermill input_notebook.ipynb output_notebook.ipynb \
  -p parameter_name "parameter_value" \
  -p number_param 42

# Execute with parameters from a YAML file
papermill input_notebook.ipynb output_notebook.ipynb \
  -f parameters.yaml
```

### Launch Jupyter Environment
```bash
# Start JupyterLab (recommended)
jupyter lab

# Or start classic Jupyter Notebook
jupyter notebook

# Specify port and host
jupyter lab --port 8888 --ip 0.0.0.0
```

### Programmatic Usage
```python
import papermill as pm

# Execute notebook programmatically
pm.execute_notebook(
    'input_notebook.ipynb',
    'output_notebook.ipynb',
    parameters={'param1': 'value1', 'param2': 42}
)
```

## Environment Management

### Activate Environment
```bash
source venv/bin/activate  # Manual activation
# or
./activate.sh            # Use setup script
```

### Deactivate Environment
```bash
deactivate
```

### Update Packages
```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## Jupyter Kernels Available

After setup, you'll have access to:
- **Python 3** - Standard Python kernel
- **Bash** - Execute shell commands and scripts

## Papermill Features

- ✅ **Parameter injection** - Pass parameters to notebooks
- ✅ **Multiple output formats** - HTML, PDF, notebook
- ✅ **Error handling** - Continue execution or stop on errors
- ✅ **Progress tracking** - Monitor notebook execution
- ✅ **Integration ready** - Use in CI/CD pipelines

## Common Use Cases

1. **Report Generation** - Parameterized reports with different data
2. **Model Training** - Run ML experiments with different parameters
3. **Data Analysis** - Automated analysis workflows
4. **CI/CD Integration** - Automated notebook testing and execution
5. **Batch Processing** - Execute multiple notebooks with different configs

## Troubleshooting

### Virtual Environment Issues
```bash
# Remove and recreate environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Kernel Issues
```bash
# Reinstall kernels
source venv/bin/activate
python -m ipykernel install --user --name papermill-env
python -m bash_kernel.install
```

### Port Conflicts
```bash
# Use different port
jupyter lab --port 8889
```

## Directory Structure
```
papermill/
├── venv/              # Virtual environment
├── requirements.txt   # Package dependencies
├── activate.sh       # Environment setup script
└── README.md         # This file
```