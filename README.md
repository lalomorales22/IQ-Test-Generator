# IQ Test Generator

A modern web application that generates custom IQ test puzzles using Flask and Anthropic's Claude AI. The application creates interactive, SVG-based puzzles with varying complexity levels and types.

<img width="1134" alt="Screenshot 2024-11-13 at 12 14 49 AM" src="https://github.com/user-attachments/assets/d4c69d39-f3c5-4e98-8272-c97f2f8ccc72">


## Features

- **Custom Puzzle Generation**: Create unique puzzles based on:
  - Puzzle Type (Mathematical, Visual Patterns, Logical Deduction)
  - Complexity Level (Easy, Medium, Hard)
  - Element Types (Figures, Symbols, Numbers)
- **Interactive UI**: Modern dark-themed interface with responsive design
- **SVG Visualization**: Clean, vector-based puzzle representations
- **Solution Explanations**: Detailed explanations for each puzzle
- **Mobile Responsive**: Optimized for both desktop and mobile devices

## Prerequisites

- Python 3.7+
- Flask
- Anthropic API access
- Modern web browser

## Installation

1. Clone the repository:
```bash
git clone https://github.com/lalomorales22/iq-test-generator.git
cd iq-test-generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install flask anthropic python-dotenv
```

4. Create a `.env` file in the project root:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

## Configuration

1. Set up your Anthropic API key in the `.env` file
2. Customize the puzzle generation parameters in `generate_puzzle_prompt()`
3. Modify the HTML template in `HTML_TEMPLATE` for UI customization

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Select your desired puzzle options:
   - Choose a puzzle type
   - Set the complexity level
   - Select element types
   - Click "Generate Puzzle"

4. View the generated puzzle and click "Show Solution" when ready

## API Endpoints

### GET `/`
- Returns the main application interface

### POST `/generate-puzzle`
- Generates a new puzzle based on provided options
- Request body:
```json
{
    "puzzle_type": "mathematical",
    "complexity": "medium",
    "elements": "figures"
}
```
- Returns:
```json
{
    "success": true,
    "puzzle": {
        "id": "20240313123456",
        "svg": "<svg>...</svg>",
        "explanation": "Solution explanation...",
        "options": {...},
        "timestamp": "2024-03-13T12:34:56"
    }
}
```

## Technical Details

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Flask (Python)
- **AI Integration**: Anthropic's Claude API (claude-3-sonnet-20240229)
- **Data Format**: SVG for puzzles, JSON for API communication
- **Styling**: CSS with dark theme and responsive design

## Error Handling

- Proper error handling for API failures
- User-friendly error messages
- Graceful degradation for unsupported browsers

## Security Considerations

- API key protection using environment variables
- Input validation for all user inputs
- Safe SVG handling and sanitization


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Anthropic for providing the Claude AI API
- Flask community for the excellent web framework
- Contributors and testers

## Support

For support, please open an issue in the GitHub repository or contact [lalo@laloadrianmorales.com]
