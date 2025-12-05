# Deployment Guide

## Vultr Deployment

### 1. Create Vultr Instance

```bash
# Create instance via Vultr dashboard or API
# Recommended: Ubuntu 22.04, 2GB RAM, 1 CPU
```

### 2. Configure Server

```bash
# SSH into server
ssh root@your-vultr-ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Create app directory
mkdir -p /opt/silent-signal
cd /opt/silent-signal
```

### 3. Deploy Application

```bash
# From local machine
cd deploy
./vultr_deploy.sh
```

### 4. Configure Environment

```bash
# On server
cd /opt/silent-signal
nano .env
# Add production environment variables
```

### 5. Start Services

```bash
docker-compose up -d
```

---

## Netlify Deployment (Frontend)

### 1. Install Netlify CLI

```bash
npm install -g netlify-cli
```

### 2. Build Frontend

```bash
cd frontend
npm run build:css
```

### 3. Deploy

```bash
netlify deploy --prod
```

### 4. Configure Environment

- Add environment variables in Netlify dashboard
- Configure redirects in `netlify.toml`

---

## Cloudflare Setup

### 1. Add Domain

1. Go to Cloudflare dashboard
2. Add your domain
3. Update nameservers

### 2. Configure DNS

```
A    @    your-vultr-ip
A    www  your-vultr-ip
```

### 3. Enable Features

- SSL/TLS: Full (strict)
- Caching: Standard
- Rate Limiting: Configure rules
- Firewall: Add security rules

---

## Database Migration

### Production Database

```bash
# Create production database
createdb silentsignal_prod

# Run migrations
python -c "from backend.database import init_db; init_db()"
```

---

## SSL Certificate

### Using Let's Encrypt

```bash
# Install certbot
apt install certbot python3-certbot-nginx -y

# Get certificate
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Monitoring

### Health Checks

```bash
# Check API health
curl https://yourdomain.com/api/health

# Check system status
curl https://yourdomain.com/api/status
```

### Logs

```bash
# View application logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend
```

---

## Backup Strategy

### Database Backup

```bash
# Create backup script
cat > /opt/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump silentsignal_prod > /opt/backups/db_$DATE.sql
# Upload to Vultr Object Storage
EOF

chmod +x /opt/backup.sh

# Add to crontab
crontab -e
# Add: 0 2 * * * /opt/backup.sh
```

---

## Scaling

### Horizontal Scaling

```bash
# Increase workers
docker-compose up -d --scale backend=3
```

### Load Balancer

- Configure Vultr Load Balancer
- Point to multiple backend instances

---

## Security Checklist

- [ ] Change default passwords
- [ ] Configure firewall (UFW)
- [ ] Enable SSL/TLS
- [ ] Set up rate limiting
- [ ] Configure CORS properly
- [ ] Enable security headers
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity

---

## Rollback Procedure

```bash
# Stop current version
docker-compose down

# Restore previous version
docker-compose up -d --force-recreate

# Restore database backup if needed
psql silentsignal_prod < /opt/backups/db_YYYYMMDD_HHMMSS.sql
```

---

## Performance Optimization

### Redis Caching

- Cache frequently accessed data
- Set appropriate TTL values
- Monitor cache hit rates

### Database Optimization

- Add indexes on frequently queried columns
- Use connection pooling
- Regular VACUUM operations

### CDN Configuration

- Cache static assets
- Optimize image delivery
- Enable compression

---

## Troubleshooting

### Application Won't Start

```bash
# Check logs
docker-compose logs

# Verify environment variables
docker-compose config

# Restart services
docker-compose restart
```

### Database Connection Issues

```bash
# Check PostgreSQL status
docker-compose ps postgres

# Test connection
docker-compose exec postgres psql -U silentsignal -d silentsignal_db
```

### High Memory Usage

```bash
# Check resource usage
docker stats

# Restart services
docker-compose restart
```
