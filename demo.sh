#!/bin/bash

# Agentic Workflows - Automated Demo Script
# For Competition Judges

set -e

echo "🚀 Agentic Workflows - Competition Demo Setup"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running in correct directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}Error: Please run this script from the agentic-workflows directory${NC}"
    exit 1
fi

echo -e "${BLUE}Step 1/5: Checking prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.11+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed. Please install Node.js 18+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}npm is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ npm found: $(npm --version)${NC}"

echo ""
echo -e "${BLUE}Step 2/5: Setting up Python backend...${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate || source .venv/Scripts/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements-full.txt

echo -e "${GREEN}✓ Backend dependencies installed${NC}"

echo ""
echo -e "${BLUE}Step 3/5: Setting up React frontend...${NC}"

cd ui

# Install Node dependencies
echo "Installing Node dependencies..."
npm install --silent

echo -e "${GREEN}✓ Frontend dependencies installed${NC}"

echo ""
echo -e "${BLUE}Step 4/5: Running tests...${NC}"

# Run type check
echo "Type checking..."
npm run type-check

# Run unit tests
echo "Running unit tests..."
npm run test -- --run

echo -e "${GREEN}✓ All tests passed${NC}"

echo ""
echo -e "${BLUE}Step 5/5: Building application...${NC}"

# Build frontend
echo "Building frontend..."
npm run build

echo -e "${GREEN}✓ Build successful${NC}"

cd ..

echo ""
echo -e "${GREEN}=============================================="
echo "✨ Setup Complete!"
echo "==============================================

${NC}"

echo ""
echo -e "${YELLOW}📋 Next Steps:${NC}"
echo ""
echo "1. Start the backend server:"
echo -e "   ${BLUE}python -m agentic_workflows.api.server${NC}"
echo ""
echo "2. In a new terminal, start the frontend:"
echo -e "   ${BLUE}cd ui && npm run dev${NC}"
echo ""
echo "3. Open your browser:"
echo -e "   ${BLUE}http://localhost:3000${NC}"
echo ""
echo -e "${YELLOW}🎬 Demo Flow:${NC}"
echo "   1. Register a new account"
echo "   2. Explore the dashboard"
echo "   3. Run a workflow"
echo "   4. View AI agents"
echo "   5. Check audit logs"
echo "   6. Visualize DAG"
echo ""
echo -e "${YELLOW}📚 Documentation:${NC}"
echo "   - README.md - Project overview"
echo "   - SUBMISSION.md - Competition guide"
echo "   - ARCHITECTURE.md - Technical details"
echo ""
echo -e "${GREEN}Good luck with the demo! 🚀${NC}"
echo ""

# Optional: Start servers automatically
read -p "Would you like to start the servers now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${BLUE}Starting backend server...${NC}"
    python -m agentic_workflows.api.server &
    BACKEND_PID=$!
    
    echo -e "${BLUE}Waiting for backend to start...${NC}"
    sleep 5
    
    echo -e "${BLUE}Starting frontend server...${NC}"
    cd ui
    npm run dev &
    FRONTEND_PID=$!
    
    echo ""
    echo -e "${GREEN}Servers started!${NC}"
    echo -e "Backend PID: ${BACKEND_PID}"
    echo -e "Frontend PID: ${FRONTEND_PID}"
    echo ""
    echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"
    echo ""
    
    # Wait for Ctrl+C
    trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
    wait
fi
