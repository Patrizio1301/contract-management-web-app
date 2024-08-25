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
splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
docs = splitter.create_documents(documents)

# Generate embeddings
embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)

# Store embeddings in a FAISS vector store
vector_store = FAISS.from_documents(docs, embeddings)


retriever = vector_store.as_retriever(search_kwargs={"k": 6})

from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# Initialize OpenAI LLM
llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0)

# Create the QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # Use "map_reduce" for larger documents
    retriever=retriever,
    return_source_documents=True
)


situation1 = "Client workshop in Silicon Valley which costs $2400."
situation2 = "Sales training in Dubai during peak tourist season which costs $2,700"
situation3 = "Research trip to remote part of Norway (booked last-minute) which costs $3,500"
situation4 = "Conference in New York with weekend travel which costs $3,000"
situation5 = "Team building event in Colorado which costs $2,200"
situation6 = "Marketing tour across Asia (planned and pre-approved)which costs 	$9,500"
situation7 = "Strategy retreat in the Swiss Alps during winter	which costs $2,400"
situation8 = "Field research in Amazon rainforest (urgent and rainy season)which costs 	$3,000"
situation9 = "Trade show participation in Florida during hurricane season	which costs $3,500"
situation10 = "Executive meeting in London during a bank holiday weekend	which costs $3,500"
situation11 = "Development workshop in Tokyo during Golden Week	which costs $2,550"
situation12 = "Client visit to manufacturing site in Germany	which costs $2,800"
situation13 = "Product launch prep in California, planned one month in advance which costs 	$7,500"
situation14 = "Annual review meeting in Singaporewhich costs 	$2,300"
situation15 = "Investor roadshow in multiple US cities (urgent and pre-approved)which costs 	$10,500"
situation16 = "Site survey for new plant in Iceland during winterwhich costs 	$3,800"
situation17 = "Negotiation meeting in high-risk area in Middle East (urgent)which costs 	$6,000"
situation18 = "Workshop in Las Vegas during a major conferencewhich costs 	$3,000"
situation19 = "Client meeting in Paris during Fashion Week	which costs $3,200"
situation20 = "Engineering team offsite in remote Alaska in January	which costs $5,000"
situation21 = "Business development trip to new markets in Africa	which costs $2,400"
situation22 = "Product testing in the Sahara Desert during summer	which costs $3,800"
situation23 = "Quarterly executive strategy meeting in Hawaii	which costs $4,000"
situation24 = "Humanitarian aid project in a high-risk area	which costs $6,000"
situation25 = "Internal training session in New York City over a holiday weekend	which costs $2,800"

"""situation 6 is wrong"""

situation = situation6

result_1 = qa_chain(
    {
        "query": f"The following situation involves assessing whether the described financial actions comply with a given contract. Analyze the situation solely with attention to the contract’s budget conditions, permissible expenditures, exceptions, and any relevant multipliers or adjustments. Specifically, determine whether the described expenditures fall within the budget by considering:"
                 f"- The base budget limit for the expense. "
                 f"- cost units provided (one vs. multiple units) and multiply accordingly by the number. With multiple we mean more than one. State in the final answer, what has been assumed."
                 f"- Any relevant multipliers or adjustments(e.g.,for night and weekend travel, high-cost locations, peak seasons, or urgency surcharges) that should be applied based on the scenario."
                 f"- The proper sequential multiplication of applicable factors to calculate the final allowable budget."
                 f"When applying multiple factors, ensure they are multiplied in the correct order. If there is uncertainty about which multipliers apply, clearly state that and provide an explanation."
                 f""
                 f"Situation: {situation}"})


non_financial_prompt = f"""
Given the contract and the situation provided:

Focus solely on non-financial aspects in determining whether the situation violates the contract or not.
Do not assume non-compliance simply because information (like pre-approvals) is missing. If the situation does not explicitly state that a required action was missed or non-compliance occurred, you should assume compliance.
If you cannot determine non-compliance based on the available non-financial information, conclude that the situation does not violate the contract and provide recommendations for any additional information needed.
Decision Criteria:
'Yes': The situation clearly violates the contract’s non-financial requirements (e.g., pre-approval processes, location-specific rules, reporting obligations).
'No': The situation does not violate the contract’s non-financial requirements based on the available information. Missing information should not be treated as a sign of non-compliance unless the situation explicitly shows that something was not done according to the contract.
'Unclear': Use this only if the contract’s non-financial terms are ambiguous, leading to genuine uncertainty in determining compliance.
Detailed Reasoning:
Focus on non-financial aspects like pre-approval, procedural requirements, and location-specific rules.
If the decision is 'No,' clearly list any recommendations for verifying additional non-financial details without implying non-compliance.
If the decision is 'Unclear,' explain that it is due to contract ambiguity, not due to missing situational details.

Situation: {situation}
"""



result_2 = qa_chain(
        {"query": non_financial_prompt})


promt_clarity = f"""
Prompt:

You are tasked with evaluating whether a contract is clear and precise regarding a specific situation. Focus on the clarity of the contract in relation to the given situation. Your analysis should address whether the contract explicitly covers the situation or if it contains ambiguous language.

Consider the following:

Clear and Explicit Definitions and Guidance:

Does the contract provide specific definitions, terms, or clauses that directly address the situation described?
Are the relevant sections of the contract detailed enough to clearly guide the situation without room for interpretation?
Ambiguity and Lack of Detail:

Identify any ambiguous terms or clauses in the contract that relate to the situation. For instance:
Are there terms that could be interpreted in more than one way?
Is there a lack of detail that leaves the situation open to interpretation?
Are there any gaps in the contract where the situation does not fit neatly into the provided terms?
Application to the Situation:

Does the contract explicitly apply to the situation described, or does it leave key aspects unresolved?
Is there a clear way to determine whether the contract applies to the situation based on the language used?
Your Expected Output:

Determine Clarity and Precision: Is the contract clear and precise regarding the situation described (Yes/No)?
Explain the Basis for Your Determination: Provide a detailed explanation of how the contract addresses or fails to address the situation, focusing on any ambiguities or lack of clarity.
Offer Recommendations: If the contract is ambiguous, suggest practical steps to clarify the contract or address the ambiguity.

Situation: {situation}
"""

# result_3 = qa_chain({ "query": promt_clarity})


final_prompt = f"""
Final Revised Prompt:
Given the following inputs:

Financial Aspects: {result_1}
Qualitative Argument: {result_2}
Please provide a final decision on whether the situation to be validated "{situation}" violates the contract. The possible answers are 'yes', 'no', or 'unclear'.

Decision Criteria:
'Yes': The situation clearly violates the contract terms based on the provided financial aspects and qualitative arguments. This applies when:

The contract terms are explicitly breached (e.g., budget caps, approval requirements, or daily expense limits are violated).
The available evidence clearly shows non-compliance with contract terms, regardless of any missing details.
'No': The situation does not violate the contract terms based on the provided financial aspects and qualitative arguments. Use this decision when:

The key financial caps are met based on the information provided, even if it leaves little room for additional costs.
Any missing information (like daily expenses, duration, or pre-approval) does not indicate a breach of contract and does not materially affect the conclusion of compliance.
The decision is based on the evidence at hand, and while further details may be recommended, they do not change the overall determination that the contract is currently adhered to.
'Unclear': Use this decision only if the contract language itself is ambiguous or does not provide clear guidance on the situation, making it impossible to determine compliance. Missing or incomplete situational information should not lead to an “unclear” decision if the core contract terms suggest compliance. Use this only when:

The contract language is open to multiple interpretations relevant to the situation.
The contract does not clearly address the situation, leading to genuine uncertainty about compliance.
Detailed Reasoning:
Explain why the situation does or does not violate the contract based on the financial and qualitative aspects.
If the decision is 'No,' list any recommendations for additional details or documentation needed for completeness without affecting the compliance decision.
If the decision is 'Unclear,' clearly specify that this is due to ambiguities in the contract terms, not because of missing situational details.

"""


final_result = qa_chain(
        {"query": final_prompt})

# print(result_1["result"])
#for doc in result_1["source_documents"]:
#    print(f"Source Document: {doc.page_content}")

#print(result_2["result"])
#for doc in result_2["source_documents"]:
#    print(f"Source Document: {doc.page_content}")

print("FINANCIAL")
print(result_1["result"])

print("NON FINANCIAL")
print(result_2["result"])

print("FINAAAAAAAAAAAAAA")
print(final_result["result"])



