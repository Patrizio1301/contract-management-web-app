<template>
  <div class="q-pa-md">
    <div style="margin-top: 20px; font-size: 20px; margin-bottom: 20px;">Feel free to upload a contract</div>
    <div style="margin-top: 20px; font-size: 15px; margin-bottom: 20px; font-weight: 300">
      Our app simplifies contract management by allowing you to easily upload contracts, automatically extracting key legal information, and providing instant answers to your legal questions. Whether you’re unsure about specific clauses or just need quick guidance, the app gives you clear insights, so you can navigate your agreements with confidence. Efficient, user-friendly, and always accessible—your contract assistant, ready whenever you need it.
    </div>
    <q-form>
    <q-stepper v-model="step" vertical color="primary" animated>

      <q-step :name="1" title="Provide a contract name" icon="settings" done-color="orange-5" active-color="orange-5" :done="step > 1">
        Please provide a name for the contract you want to upload.

        <q-input v-model="contract_name" label="Standard" />


        <q-stepper-navigation>
          <q-btn @click="step = 2" color="black" label="Continue" />
        </q-stepper-navigation>
      </q-step>

      <q-step :name="2" title="Upload contract file" icon="create_new_folder" done-color="orange-5" active-color="orange-5" :done="step > 2">
        Please provide the content of the contract.

        <q-select
              v-model="fileType"
              :options="fileOptions"
              label="Select file type"
              color="orange"
              outlined
            />

        <q-stepper-navigation>
          <q-btn @click="step = 3" color="black" label="Continue" />
          <q-btn flat @click="step = 1" color="black" label="Back" class="q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <q-step :name="3" title="Upload contract file" icon="create_new_folder" done-color="orange-5" active-color="orange-5" :done="step > 3">
        Please provide the content of the contract.

        <div class="q-pa-md" style="max-width: 90%" v-if="fileType.value === 'plain text'">
          <q-input v-model="contract_content" filled type="textarea" />
        </div>

        <q-uploader
              v-if="fileType.value === 'file (txt)'"
              label="Upload your contract"
              color="orange"
              accept=".txt,.docx"
              :max-file-size="20000000"
              url="https://pirate-service-124107706411.europe-west1.run.app/upload"
              @added="file_selected"
              bordered
            />

        <q-stepper-navigation>
          <q-btn @click="step = 4" color="black" label="Continue" />
          <q-btn flat @click="step = 2" color="black" label="Back" class="q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <q-step :name="4" title="Save in database" done-color="orange-5" active-color="orange-5" icon="add_comment">
        Click on finish if you correctly provided the contract information.

        <q-stepper-navigation>
          <q-btn color="black" label="Finish" @click="onSubmit()" />
          <q-btn flat color="black" @click="step = 3" label="Back" class="q-ml-sm" />
        </q-stepper-navigation>
      </q-step>
    </q-stepper>
    </q-form>
    <q-dialog v-model="persistent" persistent transition-show="scale" transition-hide="scale">
      <q-card class="bg-orange text-white" style="width: 50%">
        <q-card-section >
          <div class="text-h9">Loading...</div>
        </q-card-section>

        <q-card-actions align="center" class="bg-white text-teal" >
            <div style="min-height: 30vh">
            <q-spinner-bars align="center" color="orange" size="5em" style="margin-top: 11vh"/>
            </div>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { addDoc } from 'firebase/firestore';
import { numbersRef } from '../firebase';

// Define reactive variables
const step = ref(1);
const persistent= ref(false)
const contract_name = ref('');
const contract_content = ref('');
const selected_file = ref(new File([], 'https://localhost:5174/upload/contract (5).txt', { type: 'text/plain' }));
const fileType = ref({ label: 'Plain Text', value: 'plain text' }); // Default to 'plain text'

// Define options for <q-select>
const fileOptions = [
  { label: 'Plain Text', value: 'plain text' },
  { label: 'File (txt)', value: 'file (txt)' }
];

// Function to handle file selection
function file_selected(files) {
  console.log(files, files.length > 0)
  if (files.length > 0) {
    selected_file.value = files[0];
    console.log(selected_file.value)
  }
}

// Function to handle form submission
async function onSubmit() {
  persistent.value = true

  if (fileType.value === 'plain text' && !contract_content.value) {
    console.error('Plain text content is missing');
    return;
  }

  if (fileType.value === 'file (txt)' && (!selected_file.value || !contract_name.value)) {
    console.error('File or contract name is missing');
    return;
  }
  console.log(fileType.value.value, fileType.value, fileType.value.value === 'plain text')

  // Check which file type is selected
  if (fileType.value.value === 'plain text') {
    // Directly create document with plain text content
    createDocument({ contract_content: contract_content.value });
    persistent.value = false
    step.value =1

  } else if (fileType.value.value === 'file (txt)') {
    // Handle file upload
    const url = 'https://sample-124107706411.europe-west1.run.app/upload';
    const fileData = new FormData(); // No arguments are passed here
    fileData.append('file', selected_file.value); // Manually append the file

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: fileData
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();

      // Call createDocument with the content retrieved from the server
      createDocument({ contract_content: result.content });
      persistent.value = false
      step.value =1

    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
      persistent.value = false
    }
  }
}

// Modify createDocument to accept contract_content as an argument
async function createDocument({ contract_content }) {
  const newDocument = {
    contract_name: contract_name.value,
    contract_content
  };
  console.log(newDocument);

  try {
    await addDoc(numbersRef, newDocument);
  } catch (error) {
    console.error('Error creating document:', error);
  }
}
</script>





<style scoped>
.image-container {
  position: relative;
}

.image {
  width: 100%;
  height: calc(100vh - 0px);
}

.overlay-text {
  position: absolute;
  top: 47%;
  left: 20%;
  transform: translate(-50%, -50%);
  color: black;
  font-family: "Bebas Neue", sans-serif;
  font-size: 70px;
  font-weight: 400;
  text-align: center;
  background-color: transparent;
}
.overlay-text2 {
  position: absolute;
  top: 53%;
  left: 20%;
  transform: translate(-50%, -50%);
  color: black;
  font-family: "Bebas Neue", sans-serif;
  font-size: 40px;
  font-weight: 400;
  text-align: center;
  background-color: transparent;
}

@media (max-width: 1200px) {
  .overlay-text {
    font-size: 60px;
    font-weight: 300;
  }
  .overlay-text2 {
    font-size: 35px;
    font-weight: 300;
  }
}

@media (max-width: 992px) {
  .overlay-text {
    left: 20%;
    font-size: 50px;
    font-weight: 300;
  }
  .overlay-text2 {
    left: 20%;
    font-size: 30px;
    font-weight: 300;
  }
  .image {
    height: calc(100vh - 0px);
  }
}

@media (max-width: 768px) {
  .overlay-text {
    left: 30%;
    font-size: 40px;
    font-weight: 300;
  }
  .overlay-text2 {
    left: 30%;
    font-size: 25px;
    font-weight: 300;
  }
  .image {
    height: calc(100vh - 0px);
  }
}
@media (max-width: 576px) {
  .overlay-text {
    top: 44%;
    left: 30%;
    font-size: 25px;
    font-weight: 300;
  }
  .overlay-text2 {
    top: 49%;
    left: 30%;
    font-size: 25px;
    font-weight: 300;
  }
  .image {
    height: calc(100vh - 0px);
  }
}
</style>
