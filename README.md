Multimodal LLM Test Case Generator
Overview
The Multimodal LLM Test Case Generator is a web application that uses a multimodal language model to generate detailed test cases from screenshots. This tool allows users to upload screenshots and optionally provide context, which the application then uses to generate test cases including descriptions, pre-conditions, steps, expected results, and more.

Features
Upload Multiple Screenshots: Upload multiple screenshots at once for processing.
Context Input: Provide optional context to enhance the generated test cases.
Detailed Test Cases: Automatically generate detailed test cases based on the screenshots.
User-Friendly Interface: Easy-to-use front end with Vue.js for uploading screenshots and displaying test cases.
Technologies Used
Backend: Flask, Cohere API
Frontend: Vue.js, Axios
Image Processing: PIL (Python Imaging Library)
Setup
Backend Setup
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/multimodal-llm-test-case-generator.git
cd multimodal-llm-test-case-generator
Create a Virtual Environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Set Up Environment Variables:

Set your Cohere API key in the app.py file:

python
Copy code
cohere_client = cohere.Client('YOUR_API_KEY')
Run the Flask Server:

bash
Copy code
python app.py
The server will start on http://127.0.0.1:5000.

Frontend Setup
Navigate to the Frontend Directory:

bash
Copy code
cd frontend
Install Dependencies:

bash
Copy code
npm install
Run the Vue.js Development Server:

bash
Copy code
npm run serve
The frontend will be accessible at http://localhost:8080.

Usage
Open the Frontend Application:

Go to http://localhost:8080 in your web browser.

Provide Optional Context:

Enter any relevant context in the provided text area.

Upload Screenshots:

Click on the "Upload Screenshots" button and select one or more image files from your device.

Generate Test Cases:

Click on the "Describe Testing Instructions" button to send the screenshots and context to the Flask backend. The backend will process the images and return detailed test cases, which will be displayed on the page.

Review Test Cases:

The generated test cases will be listed below the upload and context input sections.

Troubleshooting
Error Generating Test Cases: Ensure your Cohere API key is correctly set in the app.py file and that the Flask server is running.
Image Upload Issues: Ensure that the image files are in a supported format (e.g., PNG, JPG) and not corrupted.
![Screenshot 2024-09-09 113906](https://github.com/user-attachments/assets/28411303-9fe5-44d8-b82b-3020c3c8e928)
![Screenshot 2024-09-09 102745](https://github.com/user-attachments/assets/ab598786-482d-411b-9837-01c8633c1511)

