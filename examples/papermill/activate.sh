#!/bin/bash
# Papermill Environment Setup Script
# This script activates the virtual environment and provides access to Jupyter and Papermill tools

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/venv"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Papermill Environment Setup${NC}"
echo

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    python -m bash_kernel.install
    echo -e "${GREEN}✅ Virtual environment created and packages installed${NC}"
else
    echo -e "${GREEN}✅ Virtual environment found${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}🔄 Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${GREEN}🎯 Environment ready!${NC}"
echo
echo -e "${BLUE}Available commands:${NC}"
echo "  papermill        - Execute notebooks with parameters"
echo "  jupyter lab      - Launch JupyterLab"
echo "  jupyter notebook - Launch classic Jupyter Notebook"
echo
echo -e "${BLUE}Example usage:${NC}"
echo "  papermill input.ipynb output.ipynb -p parameter_name parameter_value"
echo "  jupyter lab --port 8888"
echo
echo -e "${YELLOW}💡 To deactivate: type 'deactivate'${NC}"
echo

# Keep shell active with virtual environment
exec "$SHELL"