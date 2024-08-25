<template>
  <div class="q-pa-md">
    <q-select v-model="selected_contract" :options="contractNames" label="Standard" style="max-width:300px" />
    <q-input
      v-model="query"
      label="Question"
      type="textarea"
    />
    <q-btn @click="processContract" label="Process Contract" style="max-width:300px" />
    <!-- Output Display -->

    <p class="css-fix">{{output.answer}}</p>


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
import { getDocs, collection } from "firebase/firestore";
import { db } from "../firebase";

// Refs for form inputs
const selected_contract = ref('');
const output = ref({});
const query = ref("");
const contractNames = ref([]);
const persistent= ref(false)

// Reference to the Firestore collection
const numbersRef = collection(db, "numbers");

function replaceWithBr() {
  return haiku.replace(/\n/g, "<br />")
}

// Function to fetch documents
const fetchDocuments = async () => {
  try {
    const querySnapshot = await getDocs(numbersRef);
    contractNames.value = querySnapshot.docs.map(doc => ({
      label: doc.data().contract_name, // Shown in the dropdown
      value: doc.data() // The full contract data
    }));
  } catch (error) {
    console.error("Error fetching documents: ", error);
  }
};

// Fetch documents on component mount
onMounted(fetchDocuments);

const processContract = async () => {
  if (!selected_contract.value) {
    alert('Please select a contract');
    return;
  }

  try {
    persistent.value = true
    const requestBody = {
      documents: [selected_contract.value.value.contract_content], // Contract content as array
      query: query.value // The query input
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
    persistent.value = false
  } catch (error) {
    console.error('Error processing contract:', error);
    persistent.value = false
  }
};
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