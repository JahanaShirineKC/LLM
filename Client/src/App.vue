<template>
  <div id="app">
    <h1>Generate Testing Instructions</h1>
    
    <!-- Text input for optional context -->
    <div>
      <label for="context">Optional Context:</label>
      <textarea v-model="context" placeholder="Enter optional context here"></textarea>
    </div>
    
    <!-- Multi-file uploader for screenshots -->
    <div>
      <label for="screenshots">Upload Screenshots:</label>
      <input type="file" multiple @change="handleFileUpload" accept="image/*" />
    </div>
    
    <!-- Button to trigger LLM processing -->
    <button @click="submitData">Describe Testing Instructions</button>

    <!-- Display generated testing instructions -->
    <div v-if="testCases.length" >
      <h2>Generated Testing Instructions:</h2>
      <div v-for="(testCase, index) in testCases" :key="index">
        <h3>Test Case {{ index + 1 }}:</h3>
        <p><strong>Description:</strong> {{ testCase.description }}</p>
        <p><strong>Pre-conditions:</strong> {{ testCase.preconditions }}</p>
        <p><strong>Testing Steps:</strong> {{ testCase.steps }}</p>
        <p><strong>Expected Result:</strong> {{ testCase.expectedResult }}</p>
        <p><strong>Post Conditions:</strong> {{ testCase.postConditions }}</p>
        <p><strong>Actual Result:</strong> {{ testCase.actualResult }}</p>
        <p><strong>Status:</strong> {{ testCase.status }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      context: '',
      screenshots: [],
      testCases: []
    };
  },
  methods: {
    handleFileUpload(event) {
      this.screenshots = event.target.files;
    },
    async submitData() {
      const formData = new FormData();
      formData.append('context', this.context);
      for (let i = 0; i < this.screenshots.length; i++) {
        formData.append('screenshots', this.screenshots[i]);
      }

      try {
        const response = await axios.post('http://127.0.0.1:5000/generate-test-cases', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        this.testCases = response.data.testCases;
      } catch (error) {
        console.error('Error generating test cases:', error);
      }
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 50px;
}

textarea {
  width: 100%;
  height: 100px;
}

input[type="file"] {
  margin-top: 10px;
  margin-bottom: 20px;
}
</style>
