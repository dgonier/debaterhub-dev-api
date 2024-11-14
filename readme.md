# Evidence Generation API Client

This package provides Python and JavaScript implementations for an evidence generation API endpoint.

## Installation

### Python
```bash
pip install requests python-dotenv
```

### JavaScript
No installation required. Uses native fetch API.

## Usage

### Python Implementation
```python
from poller import EndpointPoller

# Initialize poller (API key is read from environment variables)
poller = EndpointPoller()

# Run the complete process
result = poller.run(
    topic="Australia should significantly increase its investment in nuclear energy",
    debate_type="parliamentary",
    side="affirmative",
    query="Impact of energy shortage in Australia",
    type_of_argument="impact",
    save_file_path="output.html"  # Optional: Save HTML output to file
)
```

### JavaScript Implementation
```javascript
const poller = new EndpointPoller();

async function runExample() {
    try {
        const result = await poller.run(
            "Impact of energy shortage in Australia",
            "Australia should significantly increase its investment in nuclear energy",
            "parliamentary",
            "affirmative",
            "impact",
            true  // render option
        );
        console.log(result);
    } catch (error) {
        console.error('Error:', error);
    }
}
```

### Web Interface
Include both `poller.js` and provided `index.html` in your directory. Open `index.html` in a web browser to access a form interface for generating evidence.

## Configuration

### Environment Variables
Create a `.env` file:
```
API_KEY=your_api_key_here
```

### Parameters
- `topic`: The debate topic
- `debate_type`: Type of debate ("parliamentary", "policy", "value")
- `side`: Debater's position ("affirmative", "negative")
- `query`: Specific query for evidence
- `type_of_argument`: Argument type ("impact", "link", "warrant", "any_type")

### Optional Settings
- `max_attempts`: Maximum polling attempts (default: 30)
- `delay`: Seconds between polls (default: 10)
- Python: `save_file_path` for saving HTML output
- JavaScript: `render` boolean to display on page

## Error Handling
Implementations handle:
- HTTP errors
- Process failures
- Timeouts
- Invalid responses

## Response Format
Success response includes:
- `status`: Process status
- `html_output`: Generated HTML content
- Additional process metadata

## Security
- Store API key in environment variables
- Never expose API key in client-side code
- Use secure configuration management