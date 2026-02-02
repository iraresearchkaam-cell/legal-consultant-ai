# ⚖️ Legal Mind AI - AI Legal Consultant

An intelligent legal consultation chatbot powered by AI that helps users ask questions about Supreme Court judgments. This application provides a streamlined interface for legal research and case analysis.

## 🌟 Features

- **Interactive Chat Interface**: Natural conversation flow for asking legal questions
- **Supreme Court Judgment Analysis**: Specialized in analyzing Supreme Court cases (Workstream 2 Pilot)
- **Real-time Processing**: Instant responses powered by AI backend
- **Chat History**: Maintains conversation context throughout the session
- **User-Friendly UI**: Clean, intuitive interface built with Streamlit
- **N8N Integration**: Seamless backend integration for AI processing

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- N8N workflow automation tool (for backend)

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

3. **Configure the N8N webhook**
   
   Open `app.py` and update the webhook URL:
   ```python
   N8N_WEBHOOK_URL = "your-n8n-webhook-url-here"
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

### N8N Webhook Setup

The application requires an N8N webhook endpoint to process legal queries. Configure your N8N workflow to:

1. Accept POST requests with JSON payload: `{"chatInput": "user question"}`
2. Process the query through your AI/legal database
3. Return JSON response: `{"answer": "AI response"}`

**Default webhook URL**: `http://localhost:5678/webhook-test/consultant-bot`

Update this in `app.py` line 6 to match your N8N instance.

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
- **Backend Integration**: N8N webhook
- **HTTP Client**: Requests library
- **Language**: Python 3.x

## 📁 Project Structure

```
legal-consultant-ai-main/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── .devcontainer/        # Development container configuration
```

## 🔧 Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run in development mode
streamlit run app.py
```

### Environment Variables

For production deployment, consider using environment variables for sensitive configuration:

```python
import os
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook-test/consultant-bot")
```

## 🚢 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Set environment variables in Streamlit Cloud dashboard
4. Deploy!

### Vercel/Other Platforms

The application can be deployed to any platform that supports Python and Streamlit applications.

## 🐛 Troubleshooting

### Common Issues

**Connection Error**
- Ensure N8N is running and accessible
- Verify the webhook URL is correct
- Check network connectivity

**No Response from AI**
- Verify N8N workflow is active
- Check webhook payload format
- Review N8N logs for errors

**Module Not Found**
- Run `pip install -r requirements.txt`
- Ensure you're using Python 3.8+

## 📝 API Reference

### N8N Webhook Endpoint

**Request**
```json
POST /webhook-test/consultant-bot
Content-Type: application/json

{
  "chatInput": "Your legal question here"
}
```

**Response**
```json
{
  "answer": "AI-generated response based on legal analysis"
}
```

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