from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set your OpenAI API key here
# openai.api_key = 'api key'

# Function to convert image to base64
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str

# Function to get image description using a vision-language model
def extract_image_description(image_path):
    # Placeholder for actual image description code.
    description = "A screenshot showing the login page with fields for username and password."
    return description

# Function to generate test case from image description using GPT-4
def generate_test_case_from_image(image_path, context):
    image_description = extract_image_description(image_path)

    prompt = f"""
    Given the following screen description: "{image_description}", generate a detailed test case using the following structure:

    Step 1 – Test Case ID: Assign a unique identifier to the test case.

    Step 2 – Test Case Description: Briefly describe the goal of this test case based on the screen.

    Step 3 – Pre-Conditions: List any pre-conditions necessary before executing the test case.

    Step 4 – Test Steps: Provide step-by-step instructions to execute this test case.

    Step 5 – Test Data: Define any necessary input data for this test case.

    Step 6 – Expected Result: Describe the expected result after executing the test steps.

    Step 7 – Post Conditions: List any cleanup steps that should be done after executing the test case.

    Step 8 – Actual Result: Describe the actual observed result after performing the test.

    Step 9 – Status: Indicate if the test passed or failed.
    """

    try:
        response = openai.Completion.create(
          engine="gpt-3.5-turbo",
          prompt=prompt,
          max_tokens=800,
          temperature=0.5,
        )
        return response.choices[0].text.strip()
    except openai.error.RateLimitError:
        return "Rate limit exceeded. Please try again later."

@app.route('/generate-test-cases', methods=['POST'])
def generate_test_cases():
    context = request.form.get('context', '')
    files = request.files.getlist('screenshots')
    
    test_cases = []
    
    for file in files:
        if file and file.content_type.startswith('image/'):
            image = Image.open(file.stream)
            image_path = 'temp_image.png'
            image.save(image_path)
            
            test_case_text = generate_test_case_from_image(image_path, context)
            test_cases.append({'description': test_case_text})
    
    return jsonify({'testCases': test_cases})

if __name__ == '__main__':
    app.run(debug=True)
