# 🎯 Quick Deployment Steps

## Prerequisites

- GitHub account
- Railway account (https://railway.app)
- Vercel account (https://vercel.com)

---

## ⚡ Fast Track (5 Minutes)

### Step 1: Push to GitHub

```bash
cd /Users/anujsmacbookair/SigmaValue
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy Backend to Railway

1. Go to **https://railway.app**
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Choose **`backend`** as root directory
5. Add environment variables:
   ```
   DJANGO_SECRET_KEY=<generate-with-command-below>
   DEBUG=False
   GEMINI_API_KEY=AIzaSyAGDPv0HAlwfS1vKdidtB_yg1XN84STbNE
   ALLOWED_HOSTS=.railway.app,.vercel.app
   ```
6. Wait for deployment (2-3 minutes)
7. Copy your Railway URL: `https://your-app.railway.app`

**Generate Secret Key:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 3: Deploy Frontend to Vercel

1. Go to **https://vercel.com**
2. Click **"New Project"** → **"Import Git Repository"**
3. Select your repository
4. Set **Root Directory** to `frontend`
5. Add environment variable:
   ```
   REACT_APP_API_URL=https://your-app.railway.app
   ```
   _(Replace with your Railway URL from Step 2)_
6. Click **"Deploy"**
7. Wait for deployment (1-2 minutes)
8. Copy your Vercel URL: `https://your-app.vercel.app`

### Step 4: Update CORS

1. Go back to **Railway** → Your project → **Variables**
2. Add:
   ```
   CORS_ALLOWED_ORIGINS=https://your-app.vercel.app
   ```
   _(Replace with your Vercel URL from Step 3)_
3. Railway will auto-redeploy

---

## ✅ Verification

1. **Test Backend**: Visit `https://your-app.railway.app/api/areas/`
2. **Test Frontend**: Visit `https://your-app.vercel.app`
3. **Upload file** and test a query

---

## 🎉 That's It!

Your app is now live at:

- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-app.railway.app`

---

## 📚 Need More Details?

See **DEPLOYMENT.md** for:

- Troubleshooting
- Database setup
- Custom domains
- File storage configuration

---

## 🔧 Common Issues

**Backend 500 Error?**

- Check Railway logs: Project → Deployments → View Logs
- Verify all environment variables are set

**Frontend can't connect to API?**

- Check `REACT_APP_API_URL` in Vercel
- Verify CORS settings in Railway

**"react-scripts: command not found" on Vercel?**

- **CRITICAL:** Make sure Root Directory is set to `frontend` in Vercel project settings
- Framework Preset should auto-detect as "Create React App"
- If not, go to Project Settings → General → Root Directory → Change to `frontend`

**Build failed?**

- Check build logs in Railway/Vercel
- Ensure all files are committed to GitHub
- Verify Root Directory is correctly set

---

## 💡 Pro Tips

1. **Auto-deploy**: Push to GitHub → Auto deploys to Railway & Vercel
2. **Preview URLs**: Each branch gets its own preview URL
3. **Logs**: Check Railway/Vercel dashboards for errors
4. **Domains**: Add custom domains in project settings

---

Need help? Check the docs:

- Railway: https://docs.railway.app
- Vercel: https://vercel.com/docs
