<template>
  <div class="q-pa-md">
     <q-select v-model="selected_contract" :options="contractNames" label="Standard" style="max-width:300px"/>
      <q-btn @click="processContract" label="Process Contract" style="max-width:300px"/>

      <q-page>
    <q-form style="max-width:800px">
      <!-- Agreement Type -->
      <q-select
        v-model="form.agreement_type"
        label="Agreement Type"
        required
      />

      <!-- Contractor -->
      <q-select
        v-model="form.contractor "
        label="Contractor"
        required
      />

      <!-- Client -->
      <q-select
        v-model="form.client "
        label="Client"
        required
      />

      <!-- Client -->
      <q-select
        v-model="form.contract_date "
        label="Contract Date"
        required
      />

      <!-- Client -->
      <q-select
        v-model="form.contract_duration "
        label="Contract Duration"
        required
      />

      <!-- Objective -->
      <q-input
        v-model="form.scope_of_work "
        label="Scope Of Work"
        type="text"
        required
      />

      <!-- Objective -->
      <q-input
        v-model="form.objective "
        label="Objective"
        type="text"
        required
      />

      <!-- Rights & Obligations -->
      <q-input
        v-model="form.rights_obligations "
        label="Rights & Obligations"
        type="textarea"
        :autogrow="true"
      />

      <!-- Financial Terms -->
      <q-input
        v-model="form.financial_terms "
        label="Financial Terms"
        type="textarea"
        :autogrow="true"
      />

      <!-- Financial Terms -->
      <q-input
        v-model="form.conditions "
        label="Conditions"
        type="textarea"
        :autogrow="true"
      />

      <!-- Intellectual Property Rights -->
      <q-input
        v-model="form.Intellectual_Property_Rights "
        label="Intellectual Property Rights"
        type="textarea"
        :autogrow="true"
      />

      <!-- Intellectual Property Rights -->
      <q-input
        v-model="form.confidentiality_terms "
        label="Confidentiality Terms"
        type="textarea"
        :autogrow="true"
      />

      <!-- Intellectual Property Rights -->
      <q-input
        v-model="form.compliance_requirements "
        label="compliance_requirements"
        type="textarea"
        :autogrow="true"
      />

      <!-- Intellectual Property Rights -->
      <q-input
        v-model="form.amendment_terms "
        label="Amendment Terms"
        type="textarea"
        :autogrow="true"
      />

      <!-- Miscellaneous -->
      <q-input
        v-model="form.Miscellaneous "
        label="Miscellaneous"
        type="textarea"
        :autogrow="true"
      />

      <!-- Service Tasks -->
      <q-input
        v-model="form.service_tasks "
        label="Service Tasks"
        type="textarea"
        :autogrow="true"
      />


      <!-- Product Description -->
      <q-input
        v-model="form.product_description "
        label="Product Description"
        type="textarea"
        :autogrow="true"
      />
    </q-form>
  </q-page>
  <q-btn @click="downloadJson" label="Download JSON" style="max-width:300px"/>
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
import { ref, onMounted } from 'vue';
import { addDoc, getDocs, collection } from "firebase/firestore";
import { db } from "../firebase";

// Refs for form inputs
const contract_name = ref('');
const contract_content = ref('');
const selected_contract = ref('');
const output = ref({});
const persistent = ref(false);

const form = ref( {
        agreement_type: null,
        contractor: null,
        client: null,
        price: '',
        objective: '',
        rights_obligations: '',
        financial_terms: '',
        Intellectual_Property_Rights: '',
        Miscellaneous: '',
        service_tasks: '',
        product_description: '',
        contract_date: '',
        contract_duration: '',
        scope_of_work: '',
        conditions: '',
        confidentiality_terms: '',
        compliance_requirements: '',
        amendment_terms: '',
        service_tasks: '',
        product_description: '',
      })

// Reference to the Firestore collection
const numbersRef = collection(db, "numbers");

// Function to add a document
const fetchDocuments = async () => {
  try {
    const querySnapshot = await getDocs(numbersRef);
    // Map the documents to only include contract names
    contractNames.value = querySnapshot.docs.map(doc => ({
      label: doc.data().contract_name, // This will be shown in the dropdown
      value: doc.data() // You can use the document ID as the value
    }));
  } catch (error) {
    console.error("Error fetching documents: ", error);
  }
};

// Ref to store the documents
const documents = ref([]);

const contractNames = ref([]);

// Fetch documents on component mount
onMounted(fetchDocuments);


const processContract = async () => {
  if (!selected_contract.value) {
    alert('Please select a contract');
    return;
  }

  persistent.value = true

  try {
    console.log(JSON.stringify(selected_contract.value.value))
    const response = await fetch('https://sample-124107706411.europe-west1.run.app/process-contract/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(selected_contract.value.value)
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    output.value = await response.json();

    form.value = {
      agreement_type: output.value.agreement_type_location.Information || '',
      contractor: output.value.contractor.Information || '',
      client: output.value.client.Information || '',
      contract_date: output.value.contract_date.Information || '',
      contract_duration: output.value.contract_duration.Information || '',
      scope_of_work: output.value.scope_of_work.Information || '',
      client: output.value.client.Information || '',
      objective: output.value.objective.Information || '',
      rights_obligations: output.value.rights_obligations.Information || [],
      financial_terms: output.value.financial_terms.Information || [],
      conditions: output.value.conditions.Information || [],
      Intellectual_Property_Rights: output.value.intellectual_property_rights.Information || [],
      confidentiality_terms: output.value.confidentiality_terms.Information || [],
      compliance_requirements: output.value.compliance_requirements.Information || [],
      amendment_terms: output.value.amendment_terms.Information || [],
      Miscellaneous: output.value.miscellaneous.Information || [],
      service_tasks: output.value.service_tasks.Information || [],
      product_description: output.value.product_description.Information || []
    };
    persistent.value = false
  } catch (error) {
    console.error('Error processing contract:', error);
    persistent.value = false
  }
};

// Function to handle downloading JSON file
const downloadJson = async () => {
  try {

    const contractName = JSON.stringify(selected_contract.value.value.contract_name).trim().replace(/^"|"$/g, '')
    const url_ = `https://sample-124107706411.europe-west1.run.app/json-structured-information-extraction?contract_name=${encodeURIComponent(contractName)}`;


    const response = await fetch(url_);

    if (!response.ok) {
      throw new Error('Failed to download the JSON file');
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    // Create a link element, trigger a click to download the file, then clean up
    const link = document.createElement('a');
    link.href = url;
    link.download = 'contract_data.json'; // Set the file name
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Clean up the object URL
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error downloading the JSON file:', error);
  }
};

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