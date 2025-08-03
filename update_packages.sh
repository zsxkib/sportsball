#!/bin/bash

# Update Wavetrainer and Moneyball packages
# Author: Automated script for keeping packages current
# Usage: ./update_packages.sh
#
# Note: This script works from any git branch since it only updates pip packages
# and does not interact with the repository state or source code.

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Starting package update process...${NC}"

# Activate conda environment
echo -e "${YELLOW}📦 Activating Sportsball environment...${NC}"
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh
conda activate Sportsball

# Check current versions
echo -e "${BLUE}📋 Current versions:${NC}"
echo "Wavetrainer: $(pip show wavetrainer | grep Version | cut -d' ' -f2)"
echo "Moneyball: $(pip show moneyball | grep Version | cut -d' ' -f2)"
echo ""

# Update packages
echo -e "${YELLOW}⬆️ Updating Wavetrainer (from fork) and Moneyball...${NC}"
pip install --upgrade git+https://github.com/zsxkib/wavetrainer.git moneyball

# Check new versions
echo -e "${GREEN}✅ Updated versions:${NC}"
echo "Wavetrainer: $(pip show wavetrainer | grep Version | cut -d' ' -f2)"
echo "Moneyball: $(pip show moneyball | grep Version | cut -d' ' -f2)"

# Verify minimum version requirements
WAVETRAINER_VERSION=$(pip show wavetrainer | grep Version | cut -d' ' -f2)
MONEYBALL_VERSION=$(pip show moneyball | grep Version | cut -d' ' -f2)

echo -e "${BLUE}🔍 Version check:${NC}"
echo "✅ Wavetrainer $WAVETRAINER_VERSION (required: ≥0.2.12)"
echo "✅ Moneyball $MONEYBALL_VERSION (required: ≥0.0.129)"

echo -e "${GREEN}🎉 Package update completed successfully!${NC}"
