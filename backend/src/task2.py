from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

import os

API_KEY = ''
os.environ["OPENAI_API_KEY"] = API_KEY

text = """
Service Agreement

Between:
“GlobalService LLC,” represented by CEO John Doe, acting on the basis of the Charter, hereinafter referred to as the “Contractor,”
and
“ClientProject Inc.,” represented by CEO Jane Smith, acting on the basis of the Charter, hereinafter referred to as the “Client.”

1. Object of the Agreement
The Contractor agrees to provide software development services in accordance with the specifications annexed to and forming an integral part of this Agreement.
The Client agrees to accept and pay for the services provided under the terms of this Agreement.

2. Rights and Obligations
2.1 The Contractor may involve third parties to perform parts of the work without notifying the Client.
2.2 The Client must provide the Contractor with all necessary information for the performance of the work within the timelines set by the specifications.
2.3 The Contractor may not use the Client’s confidential information for purposes not related to the execution of this Agreement.

3. Financial Terms
3.1 The total fee for the services under this Agreement is USD 100,000.
3.2 Payment is made by the Client in stages: 50% upfront before the commencement of work, and 50% upon completion of the work.
3.3 If payment is delayed by more than 10 days, the Contractor is entitled to suspend work until payment is received.

4. General Travel Provisions

4.1 Pre-approval Requirement
All travel arrangements must be pre-approved by the Client in writing to ensure alignment with project budgets and timelines.

4.2 Budget Caps
Total expenses for any single trip must not exceed USD 2,500, with daily expenses capped at USD 500 to maintain financial control.

4.3 Travel Class Specifications
Domestic flights should be booked in economy class to reduce costs; international flights exceeding 6 hours in duration may be booked in business class to ensure traveler well-being.

4.4 Accommodation Standards
Accommodations must be booked in approved hotels within the standard cost range, unless otherwise justified by specific project needs.

4.5 Location and Seasonal Adjustments

4.5.1 High-Cost Locations
For travels to locations like New York City or San Francisco, daily budgets may be increased by up to 20% with prior written approval from senior management.

4.5.2 Seasonal Price Fluctuations
During peak tourist seasons, such as summer or local festivals, a budget increase of up to 10% can be approved to account for seasonal price hikes.

4.6 Special Circumstances Provisions

4.6.1 Weather and Environmental Considerations
Additional allowances of up to USD 300 per trip are provided for travel to areas experiencing severe weather conditions or challenging environments.

4.6.2 Health and Safety Provisions
All necessary health and safety expenses, including vaccinations and insurance, are covered for travel to regions with known health risks.

4.7 Compliance with Policies and Laws

4.7.1 Environmental Compliance
All travel must seek to minimize environmental impact, using green transportation options where possible.

4.7.2 Legal and Regulatory Compliance
Travel must adhere to all applicable local, national, and international laws, including visa and work permit requirements.

4.8 Documentation and Reporting Requirements

4.8.1 Expense Reporting
Detailed expense reports are required within 10 days following any travel, including all receipts and justifications for expenditures over budget.

4.8.2 Audit Rights
The Client reserves the right to audit travel expenses and documentation to ensure compliance with the agreement terms and to prevent financial discrepancies.

5. Confidentiality and Data Protection
5.1 The Contractor shall keep the Client’s business secrets and other confidential information in strict confidence during and after the term of this Agreement.
5.2 Any breach of confidentiality substantially affects the execution of this Agreement and will be subject to legal remedies.

6. Intellectual Property Rights
6.1 All intellectual property rights in the software developed under this Agreement belong to the Client unless otherwise agreed in writing.
6.2 The Contractor grants the Client a non-exclusive, worldwide license to use, modify, and distribute the software.

7. Termination
7.1 This Agreement may be terminated by either party with a 30-day written notice if the other party breaches the Agreement and fails to correct the breach within a 15-day notice period.
7.2 Upon termination, all finished work and work in progress must be handed over to the Client, and all outstanding payments must be settled.

8. Limitation of Liability
8.1 The Contractor’s liability under this Agreement shall be limited to the total fee paid by the Client.
8.2 Neither party shall be liable for any indirect, incidental, or consequential damages arising from this Agreement.

9. Compliance with Laws
9.1 Both parties agree to comply with all applicable laws and regulations in the execution of this Agreement.
9.2 The Client is responsible for ensuring that the software does not violate any legal regulations in its intended markets.

10. Amendments
10.1 No modification of this Agreement shall be valid unless signed by both parties.
10.2 Any amendments to the scope of work as defined in the specifications require a written amendment to this Agreement.

11. Miscellaneous
11.1 This Agreement is governed by the laws of the State of New York.
11.2 All disputes arising from this Agreement shall be resolved through arbitration in New York, NY.

12. Software Development Tasks
12.1 Scope of Work: The Contractor will develop, test, and deploy software as per the functional and technical specifications provided by the Client.
12.2 Development Standards: All software must adhere to high industry standards of code quality and performance. The Contractor agrees to conduct rigorous testing and quality assurance before delivery.
12.3 Delivery and Implementation: The software shall be delivered according to the milestones set forth in the project plan, and the Contractor shall assist with the implementation of the




Amendment to the Service Agreement Regarding Travel Expenses

This Amendment is part of the Service Agreement (the “Agreement”) entered into between GlobalService LLC, represented by CEO John Doe, and ClientProject Inc., represented by CEO Jane Smith, originally dated [Insert Date of Main Agreement].

Purpose:
To introduce complex multi-factor adjustments to the travel expense policy to accommodate various scenarios affecting travel costs, ensuring fair and efficient management of corporate travel expenses.

1. Amendments to Travel Expense Policy:

1.1 Introduction of Multi-Factor Adjustment Conditions:

	•	Night and Weekend Travel Multiplier:
Travel expenses incurred for flights scheduled between 9:00 PM and 5:00 AM or on weekends (from Friday 9:00 PM to Monday 5:00 AM) will include a multiplier of 1.1 to address the increased costs associated with off-hours travel.
	•	Seasonal and Location-Based Adjustments:
For travel during designated peak seasons (including Christmas, New Year, and national holidays in the destination country) and to high-cost locations (as predefined in the corporate travel policy), an additional multiplier of 1.2 will be applied to the standard travel budget.
	•	Urgency and Unscheduled Travel Surge Pricing:
If travel is necessitated with less than 48 hours notice, a surge pricing multiplier of 1.3 will be applied, reflecting the higher costs associated with last-minute travel arrangements.

1.2 Example for Application of Multi-Factor Adjustments:
Consider an urgent business requirement necessitates travel to New York City over New Year’s weekend, with flight booking required on a Friday night. If the base approved travel budget is $2,500, the applicable adjustments would be:

	•	Night and Weekend Travel Multiplier: 1.1
	•	Seasonal and Location Adjustment for New York during New Year: 1.2
	•	Urgency Multiplier for last-minute booking: 1.3
The total allowable expense for this travel scenario would be $2,500 * 1.1 * 1.2 * 1.3 = $4,158.

2. Enforcement and Compliance:
Failure to comply with the stipulated adjustment rules will be considered a violation of the corporate travel policy, subject to disciplinary actions and potential financial repercussions as outlined in the main Agreement.

"""

# Sample document loading
documents = [text]

# Split documents into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.create_documents(documents)

# Generate embeddings
embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)

# Store embeddings in a FAISS vector store
vector_store = FAISS.from_documents(docs, embeddings)


retriever = vector_store.as_retriever()

from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

# Initialize OpenAI LLM
llm = OpenAI(temperature=0)

# Create the QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # Use "map_reduce" for larger documents
    retriever=retriever,
    return_source_documents=True
)

query = "where is the The type or category of this agreement (e.g., service, product, partnership) mentioned in the text?"
result = qa_chain.invoke({"query": query})

print(result["result"])
for doc in result["source_documents"]:
    print(f"Source Document: {doc.page_content}")




