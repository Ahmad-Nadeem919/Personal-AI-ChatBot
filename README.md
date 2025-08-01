# Simple Agent Backend API

A FastAPI backend for your AI agent with API key authentication, ready to use with React frontend.

## Setup

### 1. Install Dependencies

```bash
pip install -e .
```

### 2. Environment Variables

Create a `.env` file in the root directory with:

```
GEMINI_API_KEY=your_gemini_api_key_here
API_KEY=your-secret-api-key-here
```

### 3. Run the Backend

```bash
python api.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check

- `GET /` - Root endpoint
- `GET /health` - Health check

### Chat with Agent

- `POST /chat` - Send messages to the AI agent

**Headers Required:**

```
X-API-Key: your-secret-api-key-here
```

**Request Body:**

```json
{
  "message": "What's the weather in Islamabad?"
}
```

**Response:**

```json
{
  "response": "The weather in Islamabad is too much best for the Pakistani people...",
  "success": true,
  "error": null
}
```

## React Integration

Here's how to use this API in your React frontend:

```javascript
// Example React component
import { useState } from "react";

function ChatComponent() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const API_KEY = "your-secret-api-key-here"; // Store this securely

  const sendMessage = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": API_KEY,
        },
        body: JSON.stringify({ message }),
      });

      const data = await res.json();
      if (data.success) {
        setResponse(data.response);
      } else {
        console.error("Error:", data.error);
      }
    } catch (error) {
      console.error("Failed to send message:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask me anything..."
      />
      <button onClick={sendMessage} disabled={loading}>
        {loading ? "Sending..." : "Send"}
      </button>
      {response && (
        <div>
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default ChatComponent;
```

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Security Notes

- Keep your API keys secure and never expose them in client-side code
- Consider using environment variables in your React app for the API key
- The API key should be stored securely on the client side (consider using a backend proxy for production)
