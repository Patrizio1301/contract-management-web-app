# Contract Application

## Overview

The Contract Application is a tool designed to streamline the process of managing and analyzing contracts. The application consists of three main functionalities: Document Ingestion, Contract Information Extraction, and Contract QA (Question and Answer). The app currently handles text files, but there is potential for future improvements, including support for more complex file types, enhanced user interface, and more advanced contract analysis features.

The application is available under the link: https://pirate-service-124107706411.europe-west1.run.app/

## Features

### 1. Document Ingestion

- *Purpose*: The first step in using the application is to ingest a document. The app is capable of reading contract documents as plain text.
- *Functionality*: Users can upload contract documents in text format. The application processes and stores these documents for further analysis.
- *Future Improvements*:
  - Support for additional file formats such as PDF and Word documents.
  - Enhanced text parsing to handle more complex document structures.

### 2. Contract Information Extraction

- *Purpose*: This page allows users to extract and view specific information from a stored contract.
- *Functionality*: 
  - Users can select a previously saved contract.
  - The application presents relevant information in a structured format. If a particular piece of information is not available in the contract, the corresponding field will remain empty.
- *Future Improvements*:
  - Customizable templates based on contract type, allowing different types of information to be extracted depending on the nature of the contract.
  - More sophisticated parsing to capture more complex contract details.

### 3. Contract QA (Question and Answer)

- *Purpose*: This feature enables users to ask questions about a contract and determine if certain conditions are violated.
- *Functionality*: 
  - Users can pose questions related to the contract's terms.
  - The system analyzes the contract and provides answers, indicating whether the contract is being violated or not.
- *Future Improvements*:
  - Improved accuracy and depth of analysis in answering questions.
  - Ability to handle more nuanced or complex queries regarding the contract.

## Potential Future Enhancements

- *User Authentication*: Implement a profile authentication system to secure access and personalize user experience.
- *Document Formats*: Expand support beyond text to include PDF and Word documents.
- *User Interface Design*: Revamp the design for better user experience and more intuitive navigation. Some main problems still is that we do not get advised when something is loading or finished.
- *Dynamic Template Generation*: Enable dynamic templates that adapt based on the type of contract, allowing for more tailored information extraction.
- *Advanced QA Features*: Expand the QA functionality with more sophisticated question-handling.

## Technical Methodology

### 1. Contract Information Extraction
- *Implementation*: Leveraging LangChain and OpenAI APIs, the application reads and processes text documents. Forcing outputs into a specific structure is achieved using Pydantic classes. The application organizes extracted information into a list of guiding points for clarity and ease of use.
  The extracted contract data is structured into predefined sections using Pydantic. This ensures that all critical information is systematically captured. The application displays this information in a user-friendly format, with any missing data left as empty fields.

### 2. Contract QA (Question and Answer)
- *Implementation*: Two approaches were considered for contract QA:
  1. *Rule-Based System*: Initially, a simple rules-based system was implemented with carefully crafted prompts. This system assesses contract compliance and provides straightforward answers.
  2. *Agent-Based AI System*: For a more advanced approach, a multi-agent system was developed. This system includes:
     - *Budget Agent*: Focuses on budgetary compliance.
     - *Plan Agent*: Evaluates overall adherence to the contract plan.
     - *Decision Agent*: Synthesizes the inputs from the other agents to produce a final decision, which includes a binary or uncertain outcome (Yes/No/Maybe) along with a reasoning statement.

### Further improvements
- *Task combination*: A third approach for the contract QA could be to leverage the information extraction from task 1 so that the retriever might be more efficent to do and might be more reliable. 
- *Introduce more RAGs*: Another RAG system could solely focus on ambiguity and inform the system about things which are unclear. I tried to attach that but to obtain good results this might require more time.
- *Generalization*: In the prompts main focus has been to enable meaningful answers with wise decisions and reasoning but to keep the prompts general for many contracts. This can be improved to identify different types of contracts and to write prompts for each of them. 
- *Robustness*: Improvement of answers, to make sure that they are stable and do not variate too much. 
- *Monitoring*: Create a monitoring and validation system. As for now, outputs have been validated manually. 

- *Components*: Leverage more the modular manner of creating Vue applications by creating components.
- *Upload*: Relax restrictions on the csv file to be uploaded for the scenarios.  
- *Data Management*: Leverage Pinia for better data storage. As for now data is deleted all the time...


## Technical Stack

### Backend
- *FastAPI*: The API for handling tasks is built with FastAPI, ensuring fast performance and easy deployment.
- *Google Cloud*: The backend is hosted on Google Cloud, providing scalable and reliable cloud infrastructure.

### Frontend
- *Vue.js with Quasar*: The user interface is built using the Vue.js framework, with the Quasar framework to ensure a smooth and responsive user experience.
  
### Database
- *Firebase*: Firebase is used for real-time database management, offering seamless data synchronization across the application.

### Deployment
- *Google Cloud*: Both the frontend and backend are deployed on Google Cloud, with services communicating through the APIs hosted on the platform.

## Conclusion

This project showcases a combination of modern technologies to create an efficient and scalable contract management tool. The design and implementation focus on simplicity, clarity, and ease of use, with potential for significant future enhancements. This README highlights the application of technology and methodology to solve complex problems in a straightforward way, demonstrating both technical competence and a commitment to continuous improvement.