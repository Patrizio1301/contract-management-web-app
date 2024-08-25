import os
import json
import re
import uvicorn
from typing import List, Optional
from string import Template
from pypdf import PdfReader
from io import BytesIO
from docx import Document
import pandas as pd
from io import StringIO

from pydantic import BaseModel as PydanticBaseModel, Field
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, storage
from langchain_openai import ChatOpenAI

from task2_multipleRAG import main_evaluation


# Firebase initialization
cred = credentials.Certificate({})
firebase_admin.initialize_app(cred)
bucket = storage.bucket('psyched-bonito-433414-t5.appspot.com')

# FastAPI app setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://pirate-service-124107706411.europe-west1.run.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


API_KEY = ''
os.environ["OPENAI_API_KEY"] = API_KEY


# Pydantic models
class ContractInput(PydanticBaseModel):
    contract_name: str
    contract_content: str


class QueryRequest(PydanticBaseModel):
    query: str
    documents: List[str]


query_task_one = Template("""
System: 
You are an expert extraction algorithm specializing in contracts with legal terms. Your role is to extract all relevant 
information while ensuring that no crucial detail is missed. Since this is a legal document, every detail is potentially important, 
so even nuanced or subtle points must be captured if they pertain to the requested attributes. If you do not know the value of an attribute 
asked to extract, return the provided default value for the attribute's value. Answer the user query while wrapping the output in `json` tags. 

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
```
{"description": "A generalized schema to extract key information from various types of contracts,\nwith provisions for handling missing information.", "properties": {"agreement_type_location": {"title": "Agreement Type Location", "description": "Indicate the section or paragraph in the contract text where the type or category of this agreement is mentioned", "type": "string"}, "contractor": {"title": "Contractor", "description": "The name of the party or entity providing the services or goods.", "type": "string"}, "client": {"title": "Client", "description": "In which section is The name of the party or entity receiving the services or goods mentioned?", "default": "Not specified", "type": "string"}, "contract_date": {"title": "Contract Date", "description": "The date the contract was signed or becomes effective.", "default": "Date not provided", "type": "string"}, "contract_duration": {"title": "Contract Duration", "description": "The duration or term of the contract.", "default": "Duration not provided", "type": "string"}, "objective": {"title": "Objective", "description": "The main purpose or objective of the contract.", "default": "Objective not specified", "type": "string"}, "scope_of_work": {"title": "Scope Of Work", "description": "The detailed description of the work, products, or services to be provided.",  "default": ["The detailed description of the work, products, or services are not provided"], "type": "array", "items": {"type": "string"}}, "rights_obligations": {"title": "Rights Obligations", "description": "The rights, responsibilities, and obligations of each party under the contract.", "default": ["Information about The rights, responsibilities, and obligations of each party under the contract is not provided"],  "type": "array", "items": {"type": "string"}}, "conditions": {"title": "Conditions", "description": "Key conditions, restrictions, or prerequisites that must be met under the contract.",  "default": ["Key conditions, restrictions, or prerequisites that must be met under the contract are not provided"],  "type": "array", "items": {"type": "string"}}, "financial_terms": {"title": "Financial Terms", "description": "The financial terms, including price, payment schedule, fees, and penalties.",   "default": ["The financial terms, including price, payment schedule, fees, and penalties are not provided"],  "type": "array", "items": {"type": "string"}}, "payment_terms": {"title": "Payment Terms", "description": "The detailed payment terms, including amounts, milestones, and deadlines.", "default": "Payment terms not specified", "type": "string"}, "intellectual_property_rights": {"title": "Intellectual Property Rights", "description": "Terms related to ownership and use of intellectual property created or exchanged.",  "default": ["Terms related to ownership and use of intellectual property created or exchanged are not provided"],  "type": "array", "items": {"type": "string"}}, "confidentiality_terms": {"title": "Confidentiality Terms", "description": "Provisions for confidentiality, non-disclosure, and data protection.",  "default": ["Provisions for confidentiality, non-disclosure, and data protection are not provided"],  "type": "array", "items": {"type": "string"}}, "termination_clauses": {"title": "Termination Clauses", "description": "The conditions under which the contract can be terminated by either party.", "default": ["The conditions under which the contract can be terminated by either party are not provided"], "type": "array", "items": {"type": "string"}}, "dispute_resolution": {"title": "Dispute Resolution", "description": "Methods or procedures for resolving disputes (e.g., arbitration, mediation).", "default": ["Methods or procedures for resolving disputes (e.g., arbitration, mediation) are not provided"],"type": "array", "items": {"type": "string"}}, "compliance_requirements": {"title": "Compliance Requirements", "description": "Any compliance requirements, including adherence to laws, regulations, or internal policies.", "default": ["Any compliance requirements, including adherence to laws, regulations, or internal policies are not provided"], "type": "array", "items": {"type": "string"}}, "governing_law": {"title": "Governing Law", "description": "The jurisdiction or governing law under which the contract is enforceable.", "default": "Governing law not specified", "type": "string"}, "amendment_terms": {"title": "Amendment Terms", "description": "Provisions for modifying or amending the contract, including approval processes.", "default": ["Information about provisions for modifying or amending the contract, including approval processes are not provided"], "type": "array", "items": {"type": "string"}}, "miscellaneous": {"title": "Miscellaneous", "description": "Additional terms and conditions that do not fit into the other categories.", "default": ["Additional terms and conditions that do not fit into the other categories are not provided"], "type": "array", "items": {"type": "string"}}, "service_tasks": {"title": "Service Tasks", "description": "If applicable, a list of tasks or services to be delivered under the contract.", "default": ["Information not provided"],"type": "array", "items": {"type": "string"}}, "product_description": {"title": "Product Description", "description": "If applicable, a description of the products being provided.", "default": ["Products not provided"], "type": "array", "items": {"type": "string"}}, "documentation_requirements": {"title": "Documentation Requirements", "description": "Requirements for reporting, documentation, or audits under the contract.","default": ["Requirements for reporting, documentation, or audits under the contract are not provided"], "type": "array", "items": {"type": "string"}}}}
```

For each field, please add an additional key, value pair, where you indicate in which section or paragraph the data has been extracted from. Examples are:
- {"agreement_type_location": {"Information": "product selling", "location": "section 1"}}
- {"price": {"Information": "100 dollars", "location": "section 3.5"}}
- {"price": {"Information": "100 dollars", "location": "First paragraph"}}
- {"price": {"Information": "100 dollars", "location": "paragraph 4"}}
- {"price": {"Information": "100 dollars", "location": "Between paragraph one and two."}}

A bad example would be:
- {"price": {"Information": "100 dollars", "location": "Header"}}
- {"price": {"Information": "100 dollars", "location": "Between section"}}
- {"price": {"Information": "100 dollars", "location": "Between"}}

You cannot set "between" as a location value, mention at least between which paragraphs. 

Here is the contract text:
$text
""")


# Function to extract JSON from a string
def extract_json(message: str) -> List[dict]:
    """Extracts JSON content from a string where JSON is embedded between ```json and ``` tags.

    Parameters:
        message (str): The text containing the JSON content.

    Returns:
        list: A list of extracted JSON dictionaries.
    """
    pattern = r"```json(.*?)```"

    print(message)

    matches = re.findall(pattern, message.content, re.DOTALL)
    try:
        return [json.loads(match.strip()) for match in matches]
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}")


# FastAPI routes
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/process-contract/")
async def process_contract(contract: ContractInput):
    llm = ChatOpenAI(model="gpt-4o")
    json_string = llm.invoke(query_task_one.substitute({'text': contract.contract_content}))
    json_format_data = extract_json(json_string)[0]

    file_name = f"{contract.contract_name}_current_status.json"
    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(json_format_data), content_type="application/json")

    return json_format_data





@app.get("/json-structured-information-extraction")
def download_file(contract_name: str):
    local_file_path = f"/tmp/{contract_name}_current_status.json"
    try:
        blob = bucket.blob(f"{contract_name}_current_status.json")
        blob.download_to_filename(local_file_path)
        return FileResponse(path=local_file_path, filename=f"{contract_name}_current_status.json", media_type='application/json')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")


def read_pdf(file_content: bytes) -> str:
    # Convert byte content to a file-like object
    # pdf_file = BytesIO(file_content)
    # Extract text from the PDF
    # reader = PdfReader(pdf_file)
    text = "plain_test"
    # print(reader)
    #for page in reader.pages:
    #    print(page)
    return text


def read_docx(file_content: bytes) -> str:
    # Convert byte content to a file-like object
    docx_file = BytesIO(file_content)
    document = Document(docx_file)
    # Extract text from the docx
    return "\n".join([para.text for para in document.paragraphs])


@app.post("/upload_scenarios")
async def upload_scenarios(file: UploadFile = File(...), path: Optional[str] = None):
    if not file.filename.endswith(('csv')):
        raise HTTPException(status_code=400, detail='Only CSV files are allowed')

    # Read the file content
    file_content = await file.read()

    # Convert CSV content to JSON
    try:
        # Convert bytes content to a string and read it as a CSV using pandas
        csv_data = pd.read_csv(StringIO(file_content.decode('utf-8')))

        # Convert the DataFrame to a list of dictionaries (JSON-like format)
        json_data = csv_data.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV file: {str(e)}")

    if not path:
        path = file.filename

    # Upload to the specified path in the bucket
    blob = bucket.blob(path)
    blob.upload_from_string(file_content, content_type=file.content_type)

    return {"content": json_data}

@app.post("/upload")
async def upload(file: UploadFile = File(...), path: Optional[str] = None):
    if not file.filename.endswith(('txt', 'docx')):
        raise HTTPException(status_code=400, detail='Only text, Word, and PDF files are allowed')

    if not path:
        path = file.filename

    blob = bucket.blob(path)
    file_content = await file.read()

    blob.upload_from_string(file_content, content_type=file.content_type)

    # Extract text content based on file type
    if file.filename.endswith('txt'):
        text_content = file_content.decode('utf-8', errors='ignore')  # Decode with UTF-8 and ignore errors
    elif file.filename.endswith('docx'):
        text_content = read_docx(file_content)

    return {"content": text_content}

@app.post("/ask")
async def ask_question(query_request: QueryRequest):
    result = main_evaluation(query_request.documents, query_request.query, API_KEY)
    answer = result["result"]
    source_documents = [{"content": doc.page_content} for doc in result["source_documents"]]
    return {"answer": answer, "sources": source_documents}


"""
# Setup QA chain function
def setup_qa_chain(documents: List[str], api_key: str) -> RetrievalQA:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents(documents)
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vector_store = FAISS.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever()
    llm = OpenAI(temperature=0, openai_api_key=api_key)
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
"""

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
