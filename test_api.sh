#!/bin/bash
# Quick test script to verify API works

echo "Testing Crypto Scraper API..."
echo ""

# Test root
echo "🧪 Testing GET /"
curl -s http://localhost:3000/ | jq . || echo "Not running locally"
echo ""

# Test health
echo "🧪 Testing GET /api/health"
curl -s http://localhost:3000/api/health | jq .
echo ""

# Test stats
echo "🧪 Testing GET /api/stats"
curl -s http://localhost:3000/api/stats | jq .
echo ""

# Test results
echo "🧪 Testing GET /api/results"
curl -s http://localhost:3000/api/results | jq '.count'
echo ""

echo "✅ All tests completed!"
