import json
from typing import Optional, List
from langchain_core.pydantic_v1 import BaseModel, Field
from string import Template
from langchain_core.messages import AIMessage
import re

API_KEY = ''

import os

os.environ["OPENAI_API_KEY"] = API_KEY



class Contract(BaseModel):
    """
    A generalized schema to extract key information from various types of contracts,
    with provisions for handling missing information.
    """

    # General Information
    agreement_type_location: Optional[str] = Field(
        default=None,
        description="Indicate the section or paragraph in the contract text where the type or category of this agreement is mentioned"
    )
    contractor: Optional[str] = Field(
        default=None,
        description="The name of the party or entity providing the services or goods."
    )
    client: Optional[str] = Field(
        default="Not specified",
        description="In which section is The name of the party or entity receiving the services or goods mentioned?"
    )
    contract_date: Optional[str] = Field(
        default="Date not provided",
        description="The date the contract was signed or becomes effective."
    )
    contract_duration: Optional[str] = Field(
        default="Duration not provided",
        description="The duration or term of the contract."
    )

    # Objective and Scope
    objective: Optional[str] = Field(
        default="Objective not specified",
        description="The main purpose or objective of the contract."
    )
    scope_of_work: Optional[List[str]] = Field(
        default_factory=lambda: ["Scope not specified"],
        description="The detailed description of the work, products, or services to be provided."
    )

    # Rights, Obligations, and Conditions
    rights_obligations: Optional[List[str]] = Field(
        default_factory=lambda: ["Rights and obligations not specified"],
        description="The rights, responsibilities, and obligations of each party under the contract."
    )
    conditions: Optional[List[str]] = Field(
        default_factory=lambda: ["Conditions not specified"],
        description="Key conditions, restrictions, or prerequisites that must be met under the contract."
    )

    # Financial Terms and Payment
    financial_terms: Optional[List[str]] = Field(
        default_factory=lambda: ["Financial terms not specified"],
        description="The financial terms, including payment schedule, fees, and penalties."
    )

    payment_terms: Optional[str] = Field(
        default="Payment terms not specified",
        description="The detailed payment terms, including amounts, milestones, and deadlines."
    )

    # Intellectual Property and Confidentiality
    intellectual_property_rights: Optional[List[str]] = Field(
        default_factory=lambda: ["IP rights not specified"],
        description="Terms related to ownership and use of intellectual property created or exchanged."
    )
    confidentiality_terms: Optional[List[str]] = Field(
        default_factory=lambda: ["Confidentiality terms not specified"],
        description="Provisions for confidentiality, non-disclosure, and data protection."
    )

    # Termination and Dispute Resolution
    termination_clauses: Optional[List[str]] = Field(
        default_factory=lambda: ["Termination clauses not specified"],
        description="The conditions under which the contract can be terminated by either party."
    )
    dispute_resolution: Optional[List[str]] = Field(
        default_factory=lambda: ["Dispute resolution methods not specified"],
        description="Methods or procedures for resolving disputes (e.g., arbitration, mediation)."
    )

    # Compliance and Legal Considerations
    compliance_requirements: Optional[List[str]] = Field(
        default_factory=lambda: ["Compliance requirements not specified"],
        description="Any compliance requirements, including adherence to laws, regulations, or internal policies."
    )
    governing_law: Optional[str] = Field(
        default="Governing law not specified",
        description="The jurisdiction or governing law under which the contract is enforceable."
    )

    # Amendments and Modifications
    amendment_terms: Optional[List[str]] = Field(
        default_factory=lambda: ["Amendment terms not specified"],
        description="Provisions for modifying or amending the contract, including approval processes."
    )

    # Miscellaneous
    miscellaneous: Optional[List[str]] = Field(
        default_factory=lambda: ["Miscellaneous terms not specified"],
        description="Additional terms and conditions that do not fit into the other categories."
    )

    # Task or Product-Specific Details
    service_tasks: Optional[List[str]] = Field(
        default_factory=lambda: ["Service tasks not specified"],
        description="If applicable, a list of tasks or services to be delivered under the contract."
    )
    product_description: Optional[List[str]] = Field(
        default_factory=lambda: ["Product description not specified"],
        description="If applicable, a description of the products being provided."
    )

    # Reporting, Documentation, and Compliance
    documentation_requirements: Optional[List[str]] = Field(
        default_factory=lambda: ["Documentation requirements not specified"],
        description="Requirements for reporting, documentation, or audits under the contract."
    )


from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value."
            "Additionally, for each piece of extracted information, "
            "indicate the section or paragraph where this information is found."
        ),
        # Please see the how-to about improving performance with
        # reference examples.
        # MessagesPlaceholder('examples'),
        ("human", "{text}"),
    ]
)

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


from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")


### first attempt with structured output to add location (was difficult )

# runnable = prompt | llm.with_structured_output(schema=Contract2)
# output = runnable.invoke({"text": text})
# print(output)
# print(type(output))




### second attempt with structured output taking the query as input and adjusting with additional requests

"""
# Set up a parser
parser = PydanticOutputParser(pydantic_object=Contract)

# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user query. Wrap the output in `json` tags\n{format_instructions}",
        ),
        ("human", "{text}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

print(prompt.format_prompt(text=text).to_string())
"""

query = Template("""
System: Answer the user query. Wrap the output in `json` tags
The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
```
{"description": "A generalized schema to extract key information from various types of contracts,\nwith provisions for handling missing information.", "properties": {"agreement_type_location": {"title": "Agreement Type Location", "description": "Indicate the section or paragraph in the contract text where the type or category of this agreement is mentioned", "type": "string"}, "contractor": {"title": "Contractor", "description": "The name of the party or entity providing the services or goods.", "type": "string"}, "client": {"title": "Client", "description": "In which section is The name of the party or entity receiving the services or goods mentioned?", "default": "Not specified", "type": "string"}, "contract_date": {"title": "Contract Date", "description": "The date the contract was signed or becomes effective.", "default": "Date not provided", "type": "string"}, "contract_duration": {"title": "Contract Duration", "description": "The duration or term of the contract.", "default": "Duration not provided", "type": "string"}, "objective": {"title": "Objective", "description": "The main purpose or objective of the contract.", "default": "Objective not specified", "type": "string"}, "scope_of_work": {"title": "Scope Of Work", "description": "The detailed description of the work, products, or services to be provided.", "type": "array", "items": {"type": "string"}}, "rights_obligations": {"title": "Rights Obligations", "description": "The rights, responsibilities, and obligations of each party under the contract.", "type": "array", "items": {"type": "string"}}, "conditions": {"title": "Conditions", "description": "Key conditions, restrictions, or prerequisites that must be met under the contract.", "type": "array", "items": {"type": "string"}}, "financial_terms": {"title": "Financial Terms", "description": "The financial terms, including payment schedule, fees, and penalties.", "type": "array", "items": {"type": "string"}}, "payment_terms": {"title": "Payment Terms", "description": "The detailed payment terms, including amounts, milestones, and deadlines.", "default": "Payment terms not specified", "type": "string"}, "intellectual_property_rights": {"title": "Intellectual Property Rights", "description": "Terms related to ownership and use of intellectual property created or exchanged.", "type": "array", "items": {"type": "string"}}, "confidentiality_terms": {"title": "Confidentiality Terms", "description": "Provisions for confidentiality, non-disclosure, and data protection.", "type": "array", "items": {"type": "string"}}, "termination_clauses": {"title": "Termination Clauses", "description": "The conditions under which the contract can be terminated by either party.", "type": "array", "items": {"type": "string"}}, "dispute_resolution": {"title": "Dispute Resolution", "description": "Methods or procedures for resolving disputes (e.g., arbitration, mediation).", "type": "array", "items": {"type": "string"}}, "compliance_requirements": {"title": "Compliance Requirements", "description": "Any compliance requirements, including adherence to laws, regulations, or internal policies.", "type": "array", "items": {"type": "string"}}, "governing_law": {"title": "Governing Law", "description": "The jurisdiction or governing law under which the contract is enforceable.", "default": "Governing law not specified", "type": "string"}, "amendment_terms": {"title": "Amendment Terms", "description": "Provisions for modifying or amending the contract, including approval processes.", "type": "array", "items": {"type": "string"}}, "miscellaneous": {"title": "Miscellaneous", "description": "Additional terms and conditions that do not fit into the other categories.", "type": "array", "items": {"type": "string"}}, "service_tasks": {"title": "Service Tasks", "description": "If applicable, a list of tasks or services to be delivered under the contract.", "type": "array", "items": {"type": "string"}}, "product_description": {"title": "Product Description", "description": "If applicable, a description of the products being provided.", "type": "array", "items": {"type": "string"}}, "documentation_requirements": {"title": "Documentation Requirements", "description": "Requirements for reporting, documentation, or audits under the contract.", "type": "array", "items": {"type": "string"}}}}
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


output = llm.invoke(query.substitute({ 'text': text}))

# Custom parser
def extract_json(message: AIMessage) -> List[dict]:
    """Extracts JSON content from a string where JSON is embedded between ```json and ``` tags.

    Parameters:
        text (str): The text containing the JSON content.

    Returns:
        list: A list of extracted JSON strings.
    """
    text = message.content
    # Define the regular expression pattern to match JSON blocks
    pattern = r"```json(.*?)```"

    # Find all non-overlapping matches of the pattern in the string
    matches = re.findall(pattern, text, re.DOTALL)

    # Return the list of matched JSON strings, stripping any leading or trailing whitespace
    try:
        return [json.loads(match.strip()) for match in matches]
    except Exception:
        raise ValueError(f"Failed to parse: {message}")

print(output)

print(extract_json(output))

