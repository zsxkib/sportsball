#!/bin/bash

# Install local development version of wavetrainer
# Usage: ./install_dev_wavetrainer.sh

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Installing development version of wavetrainer...${NC}"

# Activate conda environment
echo -e "${YELLOW}📦 Activating Sportsball environment...${NC}"
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh
conda activate Sportsball

# Check if wavetrainer directory exists
if [ ! -d "wavetrainer" ]; then
    echo -e "${YELLOW}📥 Cloning wavetrainer fork...${NC}"
    git clone git@github.com:zsxkib/wavetrainer.git
fi

# Install in editable mode
echo -e "${YELLOW}⚙️ Installing wavetrainer in development mode...${NC}"
pip install -e ./wavetrainer

# Verify installation
echo -e "${GREEN}✅ Development installation complete:${NC}"
echo "Wavetrainer: $(pip show wavetrainer | grep Version | cut -d' ' -f2)"
echo "Location: $(pip show wavetrainer | grep Location | cut -d' ' -f2-)"

echo -e "${BLUE}📝 Note: Changes to ./wavetrainer will be immediately reflected without reinstalling${NC}"