#!/bin/bash

# Quick Deployment Script for Railway & Vercel

echo "🚀 Real Estate Chatbot - Deployment Helper"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if remote exists
if ! git remote | grep -q "origin"; then
    echo ""
    echo "⚠️  No GitHub remote found."
    echo "Please create a GitHub repository and run:"
    echo "   git remote add origin <your-github-repo-url>"
    echo ""
    read -p "Enter your GitHub repository URL (or press Enter to skip): " repo_url
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote added"
    fi
fi

echo ""
echo "📝 Preparing files for deployment..."

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    echo "Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
venv/
ENV/
env/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Environment variables
.env
.env.local
.env.production.local

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# React
build/
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
EOF
    echo "✅ .gitignore created"
fi

echo ""
echo "🔧 Next Steps:"
echo ""
echo "1️⃣  BACKEND (Railway):"
echo "   • Go to https://railway.app"
echo "   • Create new project from GitHub repo"
echo "   • Select 'backend' directory"
echo "   • Add environment variables:"
echo "     - DJANGO_SECRET_KEY=<generate-new-key>"
echo "     - DEBUG=False"
echo "     - GEMINI_API_KEY=AIzaSyAGDPv0HAlwfS1vKdidtB_yg1XN84STbNE"
echo "     - ALLOWED_HOSTS=.railway.app,.vercel.app"
echo ""
echo "2️⃣  FRONTEND (Vercel):"
echo "   • Go to https://vercel.com"
echo "   • Import your GitHub repository"
echo "   • Select 'frontend' directory"
echo "   • Add environment variable:"
echo "     - REACT_APP_API_URL=<your-railway-backend-url>"
echo ""
echo "3️⃣  UPDATE CORS:"
echo "   • After Vercel deployment, add to Railway:"
echo "     - CORS_ALLOWED_ORIGINS=<your-vercel-frontend-url>"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"
echo ""

read -p "Ready to commit and push? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "💾 Committing changes..."
    git add .
    git commit -m "Prepare for deployment to Railway and Vercel"
    
    echo ""
    echo "📤 Pushing to GitHub..."
    git push -u origin main || git push -u origin master
    
    echo ""
    echo "✅ Done! Your code is pushed to GitHub."
    echo ""
    echo "Now deploy:"
    echo "  • Railway: https://railway.app"
    echo "  • Vercel: https://vercel.com"
else
    echo ""
    echo "ℹ️  Skipped. When ready, run:"
    echo "   git add ."
    echo "   git commit -m 'Prepare for deployment'"
    echo "   git push"
fi

echo ""
echo "🎉 Good luck with your deployment!"
