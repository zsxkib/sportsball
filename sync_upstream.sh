#!/bin/bash

# Sync Sportsball and Wavetrainer repos with upstream (branch-agnostic)
# Author: Automated script for keeping repos current with upstream
# Usage: ./sync_upstream.sh

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Starting upstream sync process for Sportsball and Wavetrainer...${NC}"

# Ensure we're in the right directory
cd /Users/zsakib/Documents/sportsball

# Save the current branch name
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${BLUE}📍 Current branch: $CURRENT_BRANCH${NC}"

# Check current status
echo -e "${YELLOW}📍 Current repository status:${NC}"
git status --short
echo ""

# Fetch latest from upstream
echo -e "${YELLOW}📥 Fetching latest changes from upstream...${NC}"
git fetch upstream

# Update upstream-main branch (handle if currently checked out)
echo -e "${YELLOW}🔄 Updating upstream-main branch...${NC}"
if [ "$CURRENT_BRANCH" = "upstream-main" ]; then
    # If we're on upstream-main, merge upstream/main directly
    echo -e "${BLUE}📍 Currently on upstream-main, merging upstream/main directly...${NC}"
    git merge upstream/main --ff-only
else
    # If we're on a different branch, update upstream-main without switching
    git fetch upstream main:upstream-main
fi

# Get current commit hashes
if git show-ref --verify --quiet refs/heads/main; then
    LOCAL_MAIN=$(git rev-parse main)
else
    LOCAL_MAIN="(main branch does not exist locally)"
fi
UPSTREAM_MAIN=$(git rev-parse upstream-main)

echo -e "${BLUE}📊 Commit comparison:${NC}"
echo "Local main:        $LOCAL_MAIN"
echo "Upstream-main:     $UPSTREAM_MAIN"

if [ "$LOCAL_MAIN" = "$UPSTREAM_MAIN" ] && [ "$LOCAL_MAIN" != "(main branch does not exist locally)" ]; then
    echo -e "${GREEN}✅ Already up to date with upstream!${NC}"
    
    # Still reinstall sportsball to ensure latest code
    echo -e "${YELLOW}🔧 Reinstalling sportsball in development mode...${NC}"
    if command -v conda &> /dev/null; then
        source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh
        conda activate Sportsball
    fi
    pip install -e .
    
    # Show final version
    SPORTSBALL_VERSION=$(python -c "import sportsball; print(sportsball.__VERSION__)")
    echo -e "${GREEN}🎉 Sync completed! Sportsball version: $SPORTSBALL_VERSION${NC}"
    exit 0
fi

echo -e "${GREEN}✅ Successfully updated upstream-main branch!${NC}"
echo -e "${BLUE}💡 The upstream-main branch now contains the latest changes from upstream.${NC}"
echo -e "${BLUE}💡 You can merge these changes into your current branch when ready.${NC}"

# Reinstall sportsball in development mode to ensure latest code
echo -e "${YELLOW}🔧 Reinstalling sportsball in development mode...${NC}"
if command -v conda &> /dev/null; then
    source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh
    conda activate Sportsball
fi
pip install -e .

# Show final version
SPORTSBALL_VERSION=$(python -c "import sportsball; print(sportsball.__VERSION__)")
echo -e "${GREEN}🎉 Sportsball sync completed! Staying on branch: $CURRENT_BRANCH${NC}"
echo -e "${GREEN}🎉 Sportsball version: $SPORTSBALL_VERSION${NC}"

echo ""
echo -e "${BLUE}🔄 Now syncing Wavetrainer fork...${NC}"

# Sync wavetrainer if it exists
if [ -d "wavetrainer" ]; then
    cd wavetrainer
    
    # Check if upstream remote exists
    if git remote | grep -q "upstream"; then
        echo -e "${YELLOW}📥 Fetching latest changes from wavetrainer upstream...${NC}"
        git fetch upstream
        
        # Get current branch
        WAVETRAINER_BRANCH=$(git branch --show-current)
        echo -e "${BLUE}📍 Wavetrainer current branch: $WAVETRAINER_BRANCH${NC}"
        
        # Check if we have any local changes
        if ! git diff-index --quiet HEAD --; then
            echo -e "${YELLOW}⚠️ Local changes detected in wavetrainer, stashing...${NC}"
            git stash push -m "Auto-stash before upstream sync $(date)"
            STASHED=true
        else
            STASHED=false
        fi
        
        # Merge upstream changes
        echo -e "${YELLOW}🔄 Merging upstream changes into $WAVETRAINER_BRANCH...${NC}"
        git merge upstream/main --no-edit
        
        # Restore stashed changes if any
        if [ "$STASHED" = true ]; then
            echo -e "${YELLOW}📦 Restoring stashed changes...${NC}"
            git stash pop
        fi
        
        # Push changes to your fork
        echo -e "${YELLOW}📤 Pushing merged changes to your wavetrainer fork...${NC}"
        git push origin $WAVETRAINER_BRANCH
        
        echo -e "${GREEN}✅ Wavetrainer sync completed!${NC}"
    else
        echo -e "${YELLOW}⚠️ No upstream remote found for wavetrainer${NC}"
    fi
    
    cd ..
else
    echo -e "${YELLOW}⚠️ Wavetrainer directory not found, skipping sync${NC}"
fi

echo ""
echo -e "${GREEN}🎉 All repositories synced successfully!${NC}"
