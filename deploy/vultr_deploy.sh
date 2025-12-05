#!/bin/bash
# Vultr deployment script for Silent Signal

echo "🚀 Deploying Silent Signal to Vultr..."

# Variables
APP_NAME="silent-signal"
VULTR_INSTANCE_IP="${VULTR_INSTANCE_IP}"
SSH_KEY="${SSH_KEY_PATH:-~/.ssh/id_rsa}"

# Build and deploy
echo "📦 Building application..."
cd ..
docker build -t $APP_NAME:latest .

echo "📤 Pushing to Vultr instance..."
docker save $APP_NAME:latest | ssh -i $SSH_KEY root@$VULTR_INSTANCE_IP docker load

echo "🔄 Restarting services..."
ssh -i $SSH_KEY root@$VULTR_INSTANCE_IP << 'EOF'
cd /opt/silent-signal
docker-compose down
docker-compose up -d
EOF

echo "✅ Deployment complete!"
echo "🌐 Application available at: http://$VULTR_INSTANCE_IP:8000"
