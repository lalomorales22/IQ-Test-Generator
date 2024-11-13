from flask import Flask, request, jsonify, render_template_string
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# HTML template with embedded CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IQ Test Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #121212;
            color: #E0E0E0;
        }

        .container {
            display: flex;
            max-width: 1200px;
            margin: 0 auto;
            background-color: #1E1E1E;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
        }

        .form-container {
            flex: 1;
            margin-right: 20px;
        }

        .puzzle-container {
            flex: 2;
            background-color: #2F3136;
            padding: 20px;
            border-radius: 8px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        h1 {
            text-align: center;
            color: #BB86FC;
            margin-bottom: 30px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #BB86FC;
        }

        select {
            width: 100%;
            padding: 10px;
            border: 1px solid #333;
            border-radius: 4px;
            font-size: 16px;
            background-color: #1E1E1E;
            color: #E0E0E0;
        }

        button {
            background-color: #BB86FC;
            color: #121212;
            padding: 12px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #9A67EA;
        }

        .hidden {
            display: none;
        }

        #solution-container {
            margin-top: 20px;
        }

        #show-solution {
            background-color: #03DAC6;
        }

        #show-solution:hover {
            background-color: #018786;
        }

        #solution-text {
            margin-top: 15px;
            padding: 15px;
            background-color: #1E1E1E;
            border-radius: 4px;
            border-left: 4px solid #03DAC6;
        }

        .loading {
            color: #E0E0E0;
            text-align: center;
            font-size: 18px;
        }

        .error {
            color: #CF6679;
            padding: 15px;
            margin-top: 15px;
            border: 1px solid #CF6679;
            border-radius: 4px;
            background-color: #1E1E1E;
        }

        @media (max-width: 600px) {
            .container {
                flex-direction: column;
            }

            .form-container {
                margin-right: 0;
                margin-bottom: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="form-container">
            <h1>IQ Test Generator</h1>
            <form id="puzzle-form">
                <div class="form-group">
                    <label for="puzzle-type">Puzzle Type:</label>
                    <select id="puzzle-type" name="puzzle_type" required>
                        <option value="mathematical">Mathematical</option>
                        <option value="visual_patterns">Visual Patterns</option>
                        <option value="logical_deduction">Logical Deduction</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="complexity">Complexity:</label>
                    <select id="complexity" name="complexity" required>
                        <option value="easy">Easy</option>
                        <option value="medium">Medium</option>
                        <option value="hard">Hard</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="elements">Elements:</label>
                    <select id="elements" name="elements" required>
                        <option value="figures">Figures</option>
                        <option value="symbols">Symbols</option>
                        <option value="numbers">Numbers</option>
                    </select>
                </div>
                
                <button type="submit">Generate Puzzle</button>
            </form>
        </div>
        
        <div id="puzzle-container" class="puzzle-container">
            <div class="loading">Select options and click Generate to create a puzzle</div>
        </div>
    </div>

    <div id="solution-container" class="hidden">
        <button id="show-solution">Show Solution</button>
        <div id="solution-text" class="hidden"></div>
    </div>

    <script>
        document.getElementById('puzzle-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const puzzleContainer = document.getElementById('puzzle-container');
            const solutionContainer = document.getElementById('solution-container');
            const solutionText = document.getElementById('solution-text');
            
            // Show loading state
            puzzleContainer.innerHTML = '<div class="loading">Generating puzzle...</div>';
            solutionContainer.classList.add('hidden');
            
            // Get form data
            const formData = {
                puzzle_type: document.getElementById('puzzle-type').value,
                complexity: document.getElementById('complexity').value,
                elements: document.getElementById('elements').value
            };
            
            try {
                const response = await fetch('/generate-puzzle', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Display the puzzle
                    puzzleContainer.innerHTML = data.puzzle.svg;
                    
                    // Store the solution
                    solutionText.textContent = data.puzzle.explanation;
                    solutionContainer.classList.remove('hidden');
                    solutionText.classList.add('hidden');
                } else {
                    puzzleContainer.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                }
            } catch (error) {
                puzzleContainer.innerHTML = `<div class="error">Error generating puzzle: ${error.message}</div>`;
            }
        });

        document.getElementById('show-solution').addEventListener('click', () => {
            const solutionText = document.getElementById('solution-text');
            const showSolutionButton = document.getElementById('show-solution');
            
            if (solutionText.classList.contains('hidden')) {
                solutionText.classList.remove('hidden');
                showSolutionButton.textContent = 'Hide Solution';
            } else {
                solutionText.classList.add('hidden');
                showSolutionButton.textContent = 'Show Solution';
            }
        });
    </script>
</body>
</html>
"""

def generate_puzzle_prompt(options):
    """Generate a prompt for Claude to create a puzzle based on options"""
    complexity = options.get('complexity', 'medium')
    puzzle_type = options.get('puzzle_type', 'mathematical')
    elements = options.get('elements', 'figures')
    
    base_prompt = f"""Create an IQ test puzzle with the following specifications:
    - Complexity level: {complexity}
    - Puzzle type: {puzzle_type}
    - Using elements: {elements}
    
    The puzzle should be in SVG format with:
    - Clean, minimal design
    - Dark background (#2F3136)
    - White elements
    - Clear visual hierarchy
    - Show a sequence of equations or patterns leading to a final question
    - Include the solution logic
    
    Generate a puzzle similar to:
    AirPods + AirPods + AirPods = 30
    Person + Person + AirPods = 20
    Watch + Watch + Person = 13
    AirPod + Person × Watch = ?
    
    But create your own unique variation with your own symbols and numbers.
    The SVG should use the viewBox attribute and be responsive.
    After the SVG, provide a clear explanation of the solution logic.
    """
    
    return base_prompt

@app.route('/')
def home():
    """Render the home page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate-puzzle', methods=['POST'])
def generate_puzzle():
    """Generate a new puzzle based on provided options"""
    try:
        options = request.json
        
        # Generate prompt for Claude
        prompt = generate_puzzle_prompt(options)
        
        # Make API call to Claude
        response = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract SVG and solution from Claude's response
        message_content = response.content[0].text
        
        # Parse the response to extract SVG and explanation
        svg_start = message_content.find('<svg')
        svg_end = message_content.find('</svg>') + 6
        svg_content = message_content[svg_start:svg_end]
        
        explanation = message_content[svg_end:].strip()
        
        # Generate unique identifier for the puzzle
        puzzle_id = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Store puzzle details
        puzzle_data = {
            'id': puzzle_id,
            'svg': svg_content,
            'explanation': explanation,
            'options': options,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'puzzle': puzzle_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
