#!/bin/bash

echo "🔄 Adding changes..."
git add .

echo "📝 Commit message:"
read msg

git commit -m "$msg"

echo "🚀 Pushing to GitHub..."
git push origin main

echo "✅ Done!"