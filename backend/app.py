from flask import Flask, request, jsonify
from flask_cors import CORS
import cohere
from PIL import Image
from io import BytesIO
import base64
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set your Cohere API key here
# cohere_client = cohere.Client('')

# Function to convert image to base64
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str

# Function to generate a descriptive image name
def generate_description_from_image_name(image_name):
    # Remove the file extension
    image_description = os.path.splitext(image_name)[0]
    
    # Replace underscores or hyphens with spaces
    image_description = image_description.replace('_', ' ').replace('-', ' ')
    
    # Capitalize first letter of each word for better readability
    image_description = image_description.title()
    
    # Optionally add some contextual information to the description
    description = image_description
    
    return description

# Function to generate test case from image description using Cohere
def generate_test_case_from_image(image_name, context):
    # Remove the file extension and create a description
    image_description = os.path.splitext(image_name)[0].replace('_', ' ').replace('-', ' ').title()

    # Full prompt for generating a detailed test case
    prompt = f"""
    The image name is "{image_description}". Based on the image name, generate a description of the image and use that description to generate a detailed test case using the following structure:
    Context: {context}
    Step 1 – Test Case ID: Assign a unique identifier to the test case.

    Step 2 – Test Case Description: Briefly describe the goal of this test case based on the screen.

    Step 3 – Pre-Conditions: List any pre-conditions necessary before executing the test case.

    Step 4 – Test Steps: Provide step-by-step instructions to execute this test case.

    Step 5 – Test Data: Define any necessary input data for this test case.

    Step 6 – Expected Result: Describe the expected result after executing the test steps.

    Step 7 – Post Conditions: List any cleanup steps that should be done after executing the test case.

    Step 8 – Actual Result: Describe the actual observed result after performing the test.

    Step 9 – Status: Indicate if the test passed or failed.
    Step 10 – : Description about image .
    
    """

    try:
        response = cohere_client.generate(
            model='command-xlarge-nightly',
            prompt=prompt,
            max_tokens=800,
            temperature=0.5
        )
        test_case_text = response.generations[0].text.strip()
        return {'description': image_description, 'test_case': test_case_text}
    except Exception as e:
        return {'description': image_description, 'test_case': f"An error occurred: {str(e)}"}


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
            
            # Generate the description based on the image filename
            image_description = generate_description_from_image_name(file.filename)
            
            # Generate the test case for this image based on the description
            test_case_text = generate_test_case_from_image(image_description, context)
            
            test_cases.append({
                'description': image_description,
                'testCase': test_case_text
            })
    
    return jsonify({'testCases': test_cases})

if __name__ == '__main__':
    app.run(debug=True)
