#!/bin/bash

# Deployment script for Crypto Scraper API
# This script automates the deployment process to Vercel and GitHub

set -e

echo "🚀 Crypto Scraper - Deployment Script"
echo "========================================"
echo ""

# Check if Git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo ""
fi

# Check git status
echo "📝 Current Git status:"
git status --short
echo ""

# Prompt for commit message
read -p "📌 Enter commit message: " commit_message

# Add and commit changes
echo "💾 Committing changes..."
git add .
git commit -m "$commit_message" || echo "ℹ️  Nothing to commit"
echo ""

# Check for remote
if ! git remote get-url origin &> /dev/null; then
    echo "🔗 No GitHub remote found"
    read -p "Enter GitHub repository URL (or press Enter to skip): " repo_url
    
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote added: $repo_url"
    else
        echo "⚠️  Skipping GitHub push (no remote URL)"
        exit 0
    fi
fi

# Get remote URL
remote_url=$(git remote get-url origin)
echo "📡 Pushing to GitHub: $remote_url"
git push -u origin main 2>/dev/null || git push origin main
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found!"
    echo "Install with: npm i -g vercel"
    exit 1
fi

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
echo "Note: If this is your first deployment, follow the interactive prompts"
echo ""

vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Go to your Vercel dashboard and set environment variables"
echo "2. Configure external scheduler for hourly scraping"
echo "3. Test API endpoints at your Vercel domain"
echo "4. (Optional) Set up PostgreSQL for production use"
echo ""
echo "For more details, see DEPLOYMENT.md"
