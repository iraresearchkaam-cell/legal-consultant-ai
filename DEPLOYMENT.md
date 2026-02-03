# 🚀 Deployment Guide for Streamlit Cloud

## ✅ What We Fixed

**Problem:** The app was trying to connect to `localhost:5678` (n8n webhook) from Streamlit Cloud, which doesn't work because localhost on the cloud server is not your local machine.

**Solution:** Moved all the AI logic directly into the Streamlit app using OpenAI's API. No more external webhooks needed!

## 📋 Changes Made

1. **app.py** - Replaced webhook calls with direct OpenAI integration
2. **requirements.txt** - Updated to include `openai` package instead of `requests`
3. **README.md** - Updated documentation to reflect new setup
4. **.streamlit/secrets.toml** - Created template for API key storage
5. **.gitignore** - Added to prevent committing secrets

## 🔑 Before You Deploy

### Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)
5. **Important:** Save it somewhere safe - you can't see it again!

### Test Locally First (Optional)

1. Open `.streamlit/secrets.toml`
2. Replace `your-openai-api-key-here` with your actual API key
3. Run: `streamlit run app.py`
4. Test the chat to make sure it works

## 🌐 Deploy to Streamlit Cloud

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Fixed for cloud deployment - using OpenAI direct integration"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click **"New app"**
4. Select:
   - Repository: `your-username/legal-consultant-ai`
   - Branch: `main`
   - Main file path: `app.py`

### Step 3: Add Your API Key as a Secret

**This is the most important step!**

1. After creating the app, click on **Settings** (⚙️ icon)
2. Go to **"Secrets"** section
3. Add this (replace with your actual key):

```toml
OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
```

4. Click **"Save"**
5. Your app will automatically restart with the new configuration

### Step 4: Test Your Deployed App

1. Wait for the app to finish deploying
2. Your app will be live at: `https://[your-app-name].streamlit.app`
3. Try asking a legal question to verify it works!

## 💰 Cost Considerations

- **GPT-4o-mini** is very cost-effective (~$0.15 per 1M input tokens)
- For a typical legal query (500 tokens in, 500 tokens out), cost is ~$0.0002
- You can monitor usage at: https://platform.openai.com/usage

## 🔧 Troubleshooting

### "OpenAI API key not configured" warning
- Make sure you added the secret in Streamlit Cloud settings
- Check that the key starts with `sk-`
- Verify there are no extra spaces or quotes

### "Error processing your query"
- Check your OpenAI account has credits
- Verify the API key is valid
- Check the error message for specific details

### App won't start
- Make sure `requirements.txt` includes `openai`
- Check the logs in Streamlit Cloud for specific errors

## 📊 Monitoring

- **Streamlit Cloud Logs:** Check app logs in the Streamlit Cloud dashboard
- **OpenAI Usage:** Monitor at https://platform.openai.com/usage
- **Set spending limits:** Configure in OpenAI account settings to avoid surprises

## 🎉 You're Done!

Your app is now fully cloud-ready and will work perfectly on Streamlit Cloud without any localhost dependencies!
