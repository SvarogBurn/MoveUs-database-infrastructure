#!/bin/bash

# MoveUs Django Model Graph Generator
# This script generates visual diagrams of your Django models

echo "🎨 Generating Django Model Graphs..."
echo "======================================"

# Basic relationship diagram
echo ""
echo "📊 Creating basic model relationships..."
docker-compose exec -T web python manage.py graph_models \
  users activities events locations \
  --output /app/model_graph.png \
  --group-models \
  --arrow-shape normal \
  --theme django2018 \
  --verbose-names \
  --color-code-deletions

# Detailed version with all fields
echo ""
echo "📊 Creating detailed diagram with all fields..."
docker-compose exec -T web python manage.py graph_models \
  users activities events locations \
  --output /app/model_graph_detailed.png \
  --all-fields \
  --group-models \
  --arrow-shape normal \
  --theme django2018 \
  --verbose-names

# Compact version
echo ""
echo "📊 Creating compact diagram..."
docker-compose exec -T web python manage.py graph_models \
  users activities events locations \
  --output /app/model_graph_compact.png \
  --group-models \
  --arrow-shape normal \
  --theme django2018 \
  --verbose-names \
  --exclude-models AbstractUser,AbstractBaseUser,PermissionsMixin \
  --hide-edge-labels

# SVG format
echo ""
echo "🌐 Creating SVG format..."
docker-compose exec -T web python manage.py graph_models \
  users activities events locations \
  --output /app/model_graph.svg \
  --group-models \
  --arrow-shape normal \
  --theme django2018 \
  --verbose-names

# DOT file
echo ""
echo "📝 Creating DOT source file..."
docker-compose exec -T web python manage.py graph_models \
  users activities events locations \
  --output /app/model_graph.dot \
  --group-models \
  --arrow-shape normal \
  --verbose-names

echo ""
echo "======================================"
echo "✅ Graph generation complete!"
echo "======================================"
echo ""
echo "Generated files:"
echo "  📊 model_graph.png - Basic relationships"
echo "  📊 model_graph_detailed.png - With all fields"
echo "  📊 model_graph_compact.png - Compact version"
echo "  🌐 model_graph.svg - SVG format"
echo "  📝 model_graph.dot - DOT source"
echo ""
echo "To view files:"
echo "  docker-compose exec web ls -lh /app/model_graph*"
echo ""
echo "To copy to your local machine:"
echo "  docker cp \$(docker-compose ps -q web):/app/model_graph.png ."
echo "  docker cp \$(docker-compose ps -q web):/app/model_graph_detailed.png ."
echo "  docker cp \$(docker-compose ps -q web):/app/model_graph.svg ."
echo ""