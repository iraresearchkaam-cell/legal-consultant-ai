# ⚖️ Legal Mind AI - AI Legal Consultant

An intelligent legal consultation chatbot powered by AI that helps users ask questions about Supreme Court judgments. This application provides a streamlined interface for legal research and case analysis.

## 🌟 Features

- **Interactive Chat Interface**: Natural conversation flow for asking legal questions
- **Supreme Court Judgment Analysis**: Specialized in analyzing Supreme Court cases (Workstream 2 Pilot)
- **Real-time AI Processing**: Instant responses powered by OpenAI GPT-4o-mini
- **Chat History**: Maintains conversation context throughout the session
- **User-Friendly UI**: Clean, intuitive interface built with Streamlit
- **Cloud-Ready**: Direct OpenAI integration works seamlessly on Streamlit Cloud

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd legal-consultant-ai-main
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your OpenAI API key**
   
   Open `.streamlit/secrets.toml` and add your API key:
   ```toml
   OPENAI_API_KEY = "sk-your-actual-api-key-here"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   
   Open your browser and navigate to:
   ```
   http://localhost:8501
   ```

## 📋 Configuration

### OpenAI API Key Setup

The application uses OpenAI's API directly for AI-powered legal consultation. You need to configure your API key:

**For Local Development:**

1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Open `.streamlit/secrets.toml`
3. Replace `your-openai-api-key-here` with your actual API key

**For Streamlit Cloud Deployment:**

1. Go to your app dashboard on [Streamlit Cloud](https://share.streamlit.io/)
2. Click on your app settings (⚙️)
3. Navigate to "Secrets" section
4. Add the following:
   ```toml
   OPENAI_API_KEY = "your-openai-api-key-here"
   ```
5. Save and your app will automatically restart with the new configuration

## 💡 Usage

1. **Start the application** using `streamlit run app.py`
2. **Type your legal question** in the chat input box
3. **Wait for AI analysis** - the system will process your query
4. **Review the response** - AI-generated answers based on Supreme Court judgments
5. **Continue the conversation** - ask follow-up questions as needed

### Example Questions

- "Can a railway penalty be imposed after delivery?"
- "What are the precedents for contract breach cases?"
- "Explain the judgment on property rights disputes"

## 🛠️ Technical Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Integration**: OpenAI API (GPT-4o-mini)
- **Language**: Python 3.8+

## 📁 Project Structure

```
legal-consultant-ai-main/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .streamlit/
│   └── secrets.toml           # API keys and secrets (local only)
├── .gitignore                 # Git ignore rules
└── .devcontainer/             # Development container configuration
```

## 🔧 Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Configure your API key in .streamlit/secrets.toml

# Run in development mode
streamlit run app.py
```

### Environment Variables

The app supports configuration via Streamlit secrets or environment variables:

```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Your OpenAI API key
```

## 🚢 Deployment

### Streamlit Cloud (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Updated to use OpenAI direct integration"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Click "New app"
   - Select your repository and branch
   - Set main file path: `app.py`

3. **Configure Secrets**
   - In your app settings, go to "Secrets"
   - Add your OpenAI API key:
     ```toml
     OPENAI_API_KEY = "sk-your-actual-api-key-here"
     ```

4. **Deploy!** Your app will be live at `https://your-app-name.streamlit.app`

### Other Platforms

The application can be deployed to any platform that supports Python and Streamlit applications (Heroku, Railway, etc.).

## 🐛 Troubleshooting

### Common Issues

**"OpenAI API key not configured" Warning**
- Ensure you've added `OPENAI_API_KEY` to `.streamlit/secrets.toml` (local)
- Or added it to Streamlit Cloud secrets (cloud deployment)
- Verify the API key is valid and has credits

**"Error processing your query" Message**
- Check your OpenAI API key is correct
- Verify you have available API credits
- Check your internet connection
- Review error message for specific details

**Module Not Found**
- Run `pip install -r requirements.txt`
- Ensure you're using Python 3.8+
- Activate your virtual environment if using one

**Rate Limit Errors**
- OpenAI has rate limits based on your plan
- Consider upgrading your OpenAI plan
- Implement request throttling if needed

## 📝 API Reference

### Internal Function: `consultant_bot(user_query)`

The application uses an internal function to process legal queries:

**Input:**
- `user_query` (string): The user's legal question

**Output:**
- Returns AI-generated response based on OpenAI GPT-4o-mini

**System Prompt:**
The AI is configured as an expert legal consultant specializing in Supreme Court judgments and Indian law, providing:
- Precise legal analysis
- Relevant case law references
- Professional legal insights
- Clear explanations of complex concepts

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is part of the Workstream 2 Pilot for legal AI consultation.

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Document upload for case analysis
- [ ] Export chat history
- [ ] Advanced filtering and search
- [ ] Integration with additional legal databases
- [ ] User authentication and session management

## 📞 Support

For questions or issues, please open an issue in the repository or contact the development team.

---

**Built with ❤️ for legal professionals and researchers**