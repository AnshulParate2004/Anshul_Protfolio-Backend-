# 🚀 Vercel Deployment Guide

## Prerequisites
- Python 3.9+
- Google API Key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Vercel account (free tier works)
- Git installed

## Step-by-Step Deployment

### 1️⃣ Prepare Your Code

Ensure you have these files in your project:
```
less/
├── main.py
├── agent.py
├── config.py
├── profile_data.py
├── requirements.txt
├── vercel.json
├── .env.example
├── .gitignore
└── README.md
```

### 2️⃣ Test Locally First

```bash
# Navigate to the less directory
cd D:\Anshul_Protfolio-Backend-\less

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Then edit .env and add your GOOGLE_API_KEY

# Run the server
python main.py

# Test in another terminal
python test_api.py
```

Visit http://localhost:8000/docs to see the interactive API documentation.

### 3️⃣ Deploy via Vercel CLI (Recommended)

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from the less directory
cd D:\Anshul_Protfolio-Backend-\less
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - What's your project's name? anshul-portfolio-backend (or your choice)
# - In which directory is your code located? ./
# - Want to override the settings? No
```

### 4️⃣ Add Environment Variables

After deployment, add your Google API key:

```bash
# Add environment variable
vercel env add GOOGLE_API_KEY

# Choose:
# - Production: Yes
# - Preview: Yes
# - Development: Yes

# Paste your Google API key when prompted
```

Or via Vercel Dashboard:
1. Go to your project in Vercel
2. Settings → Environment Variables
3. Add `GOOGLE_API_KEY` with your key
4. Select all environments (Production, Preview, Development)

### 5️⃣ Deploy to Production

```bash
# Deploy to production
vercel --prod
```

### 6️⃣ Alternative: GitHub Integration

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Create a repository on GitHub and push
git remote add origin https://github.com/yourusername/your-repo.git
git branch -M main
git push -u origin main
```

Then in Vercel Dashboard:
1. Click "Add New Project"
2. Import your GitHub repository
3. Configure:
   - Framework Preset: Other
   - Root Directory: `less` (if deploying from subdirectory)
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
4. Add Environment Variables:
   - `GOOGLE_API_KEY`: your-api-key
5. Click "Deploy"

## 📋 Post-Deployment Checklist

- [ ] Deployment successful (check Vercel dashboard)
- [ ] Environment variables set correctly
- [ ] Test the `/health` endpoint: `https://your-app.vercel.app/health`
- [ ] Test the `/` endpoint: `https://your-app.vercel.app/`
- [ ] Test the `/docs` endpoint: `https://your-app.vercel.app/docs`
- [ ] Test chat functionality
- [ ] Check logs in Vercel dashboard if any errors

## 🧪 Testing Your Deployed API

```bash
# Replace YOUR_VERCEL_URL with your actual URL

# Test health
curl https://YOUR_VERCEL_URL/health

# Test chat
curl -X POST https://YOUR_VERCEL_URL/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Who is Anshul?", "session_id": "test"}'

# Test quick info
curl -X POST https://YOUR_VERCEL_URL/quick-info \
  -H "Content-Type: application/json" \
  -d '{"info_type": "contact"}'
```

## 🔧 Troubleshooting

### Build Fails

**Issue**: Python version mismatch
```bash
# Specify Python version in vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python",
      "config": { "runtime": "python3.9" }
    }
  ]
}
```

### Import Errors

**Issue**: Missing dependencies
```bash
# Verify requirements.txt is correct
cat requirements.txt

# Test installation locally
pip install -r requirements.txt
```

### API Key Not Working

**Issue**: Environment variable not set
1. Check Vercel Dashboard → Settings → Environment Variables
2. Ensure `GOOGLE_API_KEY` is added for all environments
3. Redeploy after adding: `vercel --prod`

### 500 Internal Server Error

**Issue**: Check Vercel logs
1. Go to Vercel Dashboard
2. Click on your deployment
3. Go to "Functions" tab
4. Click on the function to see logs

Common causes:
- Missing environment variables
- Import errors
- API key issues

### Cold Start Timeout

**Issue**: First request takes too long
- This is normal for serverless functions
- Vercel has a 10-second timeout for hobby tier
- Consider keeping the function warm with a cron job

```bash
# Optional: Add a vercel.json cron config
{
  "crons": [{
    "path": "/health",
    "schedule": "*/5 * * * *"
  }]
}
```

## 🎯 Performance Optimization

### 1. Keep Functions Warm
Use a service like [UptimeRobot](https://uptimerobot.com/) to ping your `/health` endpoint every 5 minutes.

### 2. Optimize Response Size
The API already:
- ✅ Limits conversation history to 10 messages
- ✅ Uses efficient Pydantic models
- ✅ Minimizes dependencies
- ✅ Caches agent initialization

### 3. Monitor Performance
Use Vercel Analytics:
1. Go to your project in Vercel
2. Click "Analytics" tab
3. Monitor response times and errors

## 📚 Additional Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [FastAPI on Vercel](https://vercel.com/guides/deploying-fastapi-with-vercel)
- [Google AI Studio](https://makersuite.google.com/app/apikey)
- [Vercel CLI Documentation](https://vercel.com/docs/cli)

## 🔐 Security Best Practices

1. **Never commit `.env` file** - it's in `.gitignore`
2. **Use environment variables** for all secrets
3. **Rotate API keys** periodically
4. **Enable CORS** properly for your frontend domain
5. **Monitor usage** in Google AI Studio dashboard

## 📊 Monitoring & Logs

```bash
# View real-time logs
vercel logs https://your-app.vercel.app

# View logs for specific function
vercel logs https://your-app.vercel.app --follow
```

## 🎉 Success!

Your API should now be live at: `https://your-project.vercel.app`

Test it with:
- Interactive docs: `https://your-project.vercel.app/docs`
- Health check: `https://your-project.vercel.app/health`
- Root endpoint: `https://your-project.vercel.app/`

## 💡 Next Steps

1. Update your frontend to use the new Vercel URL
2. Test all endpoints thoroughly
3. Monitor logs and performance
4. Add custom domain (optional)
5. Set up monitoring alerts

## 📞 Support

If you encounter issues:
1. Check Vercel logs first
2. Review this guide's troubleshooting section
3. Check the main README.md
4. Open an issue on GitHub

Happy deploying! 🚀
