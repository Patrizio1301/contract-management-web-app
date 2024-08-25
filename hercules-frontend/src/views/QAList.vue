<template>
  <div class="q-pa-md">
    <div style="margin-top: 20px; font-size: 20px; margin-bottom: 20px;">Feel free to upload a contract</div>
    <div style="margin-top: 20px; font-size: 15px; margin-bottom: 20px; font-weight: 300">
      Select your uploaded contract, upload scenario details in a CSV format, and instantly discover if each case violates the contract terms! The CSV should have two simple columns: Description and Amount, separated by a comma. Once uploaded, each scenario is automatically evaluated against your contract—quickly revealing which scenarios comply and which ones breach the rules. It’s a fast and efficient way to ensure you stay within the terms of your contract!    </div>
    <q-form>
    <q-stepper v-model="step" vertical color="primary" animated>

      <q-step :name="1" title="Select a contract" icon="settings" done-color="orange-5" active-color="orange-5" :done="step > 1">
        Please select a contract you want to explore.

        <q-select v-model="selected_contract" :options="contractNames" label="Standard" style="max-width:300px"/>


        <q-stepper-navigation>
          <q-btn @click="step = 2" color="black" label="Continue" />
        </q-stepper-navigation>
      </q-step>

      <q-step :name="2" title="Upload contract scenarios" icon="create_new_folder" done-color="orange-5" active-color="orange-5" :done="step > 2">
        Please provide the content of the scenarios in csv format. For the CSV file to work correctly as input, it should have the following format: The CSV file should have two columns named exactly as follows: "Description" and "Amount". The columns should be separated by a comma (,). The first row should contain the headers: "Description" and "Amount". Each subsequent row should contain the relevant description and amount values.

        <q-uploader
              label="Upload your scenarios"
              color="orange"
              accept=".csv"
              :max-file-size="20000000"
              url="https://pirate-service-124107706411.europe-west1.run.app/upload"
              @added="file_selected"
              bordered
            />

        <q-stepper-navigation>
          <q-btn @click="step = 3" color="black" label="Continue" />
          <q-btn flat @click="step = 1" color="black" label="Back" class="q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <q-step :name="3" title="Save in database" done-color="orange-5" active-color="orange-5" icon="add_comment">
        Click on finish if you correctly provided the scenario information.

        <q-stepper-navigation>
          <q-btn color="black" label="Finish" @click="onSubmit()" />
          <q-btn flat color="black" @click="step = 2" label="Back" class="q-ml-sm" />
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
     <div style="margin-top:20px">
    <q-table
      title="Scenarios"
      :rows="jsonData"
      :columns="columns"
      row-key="name"
    >
        <template v-slot:body="props">
        <q-tr :props="props" @click="onRowClick(props.row)">
          <q-td key="description" :props="props">
            {{ props.row.Description }}
          </q-td>
          <q-td key="Amount" :props="props">
              {{ props.row.Amount }}
          </q-td>
          <q-td key="Answer" :props="props">
            <q-btn @click="fetchAnswer(props.row.Amount, props.row.Description)"> Check Answer </q-btn>
          </q-td>
        </q-tr>
      </template>
    </q-table>
    <q-dialog v-model="show_answer" persistent transition-show="scale" transition-hide="scale">
      <q-card class="bg-orange text-white" style="width: 50%">
        <q-card-section >
          <div class="text-h9">Answer</div>
        </q-card-section>

        <q-card-actions v-if="!loading_answer" align="center" class="bg-white text-black" >
            <p class="css-fix">{{output.answer}}</p>
        </q-card-actions>

        <q-card-actions v-if="loading_answer" align="center" class="bg-white text-teal" >
            <div style="min-height: 30vh">
            <q-spinner-bars align="center" color="orange" size="5em" style="margin-top: 11vh"/>
            </div>
        </q-card-actions>

        <q-card-actions v-if="!loading_answer" align="right" class="bg-white text-black" >
            <q-btn flat label="OK" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed  } from 'vue';
import { addDoc, getDocs, collection } from "firebase/firestore";
import { db } from "../firebase";

// Define reactive variables
const step = ref(1);
const show_answer = ref(false);
const loading_answer = ref(false);
const persistent= ref(false);
const contract_name = ref('');
const contract_content = ref('');
const selected_file = ref(new File([], 'https://localhost:5174/upload/contract (5).txt', { type: 'text/plain' }));
const fileType = ref({ label: 'Plain Text', value: 'plain text' }); // Default to 'plain text'

const contractNames = ref([]);
const selected_contract = ref('');

const jsonData = ref([{'scenario': 'Vacations', 'price': 0}]);
const numbersRef = collection(db, "numbers");

const output = ref("")

// Computed property to generate the columns based on the keys of the JSON
const columns = [{
    name: 'description',
    required: true,
    label: 'Task Description',
    align: 'left',
    field: 'description',
    format: val => `${val}`,
    sortable: true
  },
  { name: 'Amount', align: 'center', label: 'Amount', field: 'Amount', sortable: true },
  { name: 'Answer', align: 'center', label: 'Answer', field: 'Answer', sortable: true }]

async function fetchAnswer(amount, description) {
  // Generate the concatenated sentence
  const sentence = `${description} with a cost of ${amount}`;

  // Prepare the data to be sent (if needed as JSON payload)

  try {
    show_answer.value = true
    loading_answer.value = true
    console.log(sentence)
    console.log("CONTEEEEENT", selected_contract.value.value.contract_content)
    const requestBody = {
      documents: [selected_contract.value.value.contract_content], // Contract content as array
      query: sentence // The query input
    };

    console.log(JSON.stringify(requestBody))

    const response = await fetch('https://sample-124107706411.europe-west1.run.app/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody) // Properly stringified request body
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    output.value = await response.json(); // Get the response as JSON
    console.log("OUTPUTTTTT", output.value)
    loading_answer.value = false
  } catch (error) {
    console.error('Error processing contract:', error);
    persistent.value = false
  }
}


const fetchDocuments = async () => {
  try {
    console.log("WE TRYYYY")
    const querySnapshot = await getDocs(numbersRef);
    // Map the documents to only include contract names
    contractNames.value = querySnapshot.docs.map(doc => ({
      label: doc.data().contract_name, // This will be shown in the dropdown
      value: doc.data() // You can use the document ID as the value
    }));
    console.log("CONTRAAACT", contractNames.value)
  } catch (error) {
    console.error("Error fetching documents: ", error);
  }
};

// Fetch documents on component mount
onMounted(fetchDocuments);



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
  console.log("ALL GOOD BEFORE", selected_file, !selected_file.value);
  const url = 'https://sample-124107706411.europe-west1.run.app/upload_scenarios';
    const fileData = new FormData(); // No arguments are passed here
    fileData.append('file', selected_file.value); // Manually append the file


    console.log(fileData)

    console.log("WE MADE IT")

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: fileData
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();
      jsonData.value = result.content;
      console.log("OUTPUT", jsonData.value)

      // Call createDocument with the content retrieved from the server
      persistent.value = false
      step.value =1

    } catch (error) {
      console.log(error)
      console.error('There was a problem with the fetch operation:', error);
      persistent.value = false
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

.css-fix {
  white-space: pre-wrap;
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