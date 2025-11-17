# 🚀 Deployment Guide

This guide will help you deploy your Real Estate Analysis Chatbot to production.

## Architecture

- **Frontend**: Vercel (React app)
- **Backend**: Railway (Django API)

---

## 📦 Backend Deployment (Railway)

### Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app)

### Step 1: Prepare Your Backend

1. **Create a `railway.json` file** in the `/backend` directory:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn realestate_chatbot.wsgi:application --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

2. **Update `requirements.txt`** (already done):

   - Ensure `gunicorn` is listed
   - All dependencies are pinned

3. **Update `settings.py`** for production:

Add to `/backend/realestate_chatbot/settings.py`:

```python
import dj_database_url

# Railway database configuration
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

# Railway domain
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',
    '.vercel.app',
]

# CORS for production
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://your-frontend.vercel.app',  # Update this after deploying frontend
]

# Static files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
```

### Step 2: Deploy to Railway

1. **Push your code to GitHub**:

```bash
cd /Users/anujsmacbookair/SigmaValue
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

2. **Create Railway Project**:

   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Select the `backend` directory as the root

3. **Configure Environment Variables**:

Click on your project → Variables → Add the following:

```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
GEMINI_API_KEY=AIzaSyAGDPv0HAlwfS1vKdidtB_yg1XN84STbNE
ALLOWED_HOSTS=.railway.app,.vercel.app
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

To generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

4. **Add PostgreSQL Database** (Optional but recommended):

   - Click "New" → "Database" → "PostgreSQL"
   - Railway will automatically set `DATABASE_URL` environment variable

5. **Deploy**:

   - Railway will automatically detect Python and deploy
   - Wait for deployment to complete
   - Your backend will be available at: `https://your-app.railway.app`

6. **Run Migrations**:
   - Go to your Railway project
   - Click on "Settings" → "Deploy"
   - Add a one-time command: `python manage.py migrate`

### Step 3: Test Backend

Visit: `https://your-app.railway.app/api/areas/`

You should see the API response.

---

## 🌐 Frontend Deployment (Vercel)

### Step 1: Prepare Your Frontend

1. **Update API URL** in `/frontend/src/services/api.js`:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
```

2. **Create `.env.production`** in `/frontend`:

```env
REACT_APP_API_URL=https://your-backend.railway.app
```

3. **Create `vercel.json`** in `/frontend`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "framework": "create-react-app",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### Step 2: Deploy to Vercel

#### Option A: Using Vercel CLI

1. **Install Vercel CLI**:

```bash
npm install -g vercel
```

2. **Deploy**:

```bash
cd /Users/anujsmacbookair/SigmaValue/frontend
vercel
```

3. **Follow the prompts**:

   - Set up and deploy? Yes
   - Which scope? Select your account
   - Link to existing project? No
   - Project name? `realestate-chatbot`
   - Directory? `./`
   - Override settings? No

4. **Set Environment Variable**:

```bash
vercel env add REACT_APP_API_URL production
```

Enter: `https://your-backend.railway.app`

5. **Deploy to production**:

```bash
vercel --prod
```

#### Option B: Using Vercel Dashboard

1. **Push code to GitHub** (if not done):

```bash
cd /Users/anujsmacbookair/SigmaValue
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

2. **Import to Vercel**:

   - Go to https://vercel.com
   - Click "New Project"
   - Import your GitHub repository
   - Select the `frontend` directory as root
   - Click "Deploy"

3. **Configure Environment Variables**:

   - Go to Project Settings → Environment Variables
   - Add: `REACT_APP_API_URL` = `https://your-backend.railway.app`
   - Click "Save"

4. **Redeploy**:
   - Go to Deployments
   - Click "Redeploy" to apply environment variables

### Step 3: Update Backend CORS

Once you have your Vercel URL, update Railway environment variables:

```
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

Redeploy the backend on Railway.

---

## 🔄 Continuous Deployment

Both Railway and Vercel support automatic deployments:

- **Push to GitHub** → Automatically deploys to both platforms
- **Main branch** → Production deployment
- **Other branches** → Preview deployments

---

## ✅ Post-Deployment Checklist

### Backend (Railway)

- [ ] API endpoints respond correctly
- [ ] Database migrations completed
- [ ] Environment variables set
- [ ] CORS configured for frontend domain
- [ ] File uploads working (configure media storage)

### Frontend (Vercel)

- [ ] App loads correctly
- [ ] API calls work
- [ ] File upload functional
- [ ] Charts display properly
- [ ] Responsive on mobile

---

## 🐛 Troubleshooting

### Backend Issues

**500 Error:**

- Check Railway logs: Project → Deployments → View Logs
- Verify `DEBUG=False` and `ALLOWED_HOSTS` is set correctly

**Database Connection Error:**

- Ensure PostgreSQL is added to Railway project
- Check `DATABASE_URL` environment variable

**CORS Error:**

- Update `CORS_ALLOWED_ORIGINS` with your Vercel URL
- Redeploy backend

### Frontend Issues

**API Connection Failed:**

- Verify `REACT_APP_API_URL` is set correctly
- Check browser console for errors
- Test backend URL directly

**Build Failed:**

- Check Vercel build logs
- Ensure all dependencies are in `package.json`
- Try building locally: `npm run build`

---

## 📊 File Storage (Optional)

For production file uploads, configure cloud storage:

### AWS S3 Setup

1. **Install boto3**:

```bash
pip install boto3 django-storages
```

2. **Update `settings.py`**:

```python
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = 'us-east-1'
```

3. **Add to Railway environment variables**:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_STORAGE_BUCKET_NAME`

---

## 🔗 Final URLs

After deployment, your app will be accessible at:

- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://your-app.railway.app`

Update your README with these URLs! 🎉

---

## 💡 Tips

1. **Custom Domains**: Both Railway and Vercel support custom domains
2. **Environment Variables**: Keep sensitive data in environment variables, never commit them
3. **Monitoring**: Use Railway and Vercel dashboards to monitor performance
4. **Logs**: Check logs regularly for errors
5. **Database Backups**: Railway provides automatic PostgreSQL backups

---

## 📞 Support

- **Railway**: https://docs.railway.app
- **Vercel**: https://vercel.com/docs
- **Django**: https://docs.djangoproject.com

Good luck with your deployment! 🚀
