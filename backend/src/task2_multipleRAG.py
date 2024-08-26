from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
import os





def load_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    return splitter.create_documents(documents)


def initialize_vector_store(documents, API_KEY):
    embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store.as_retriever(search_kwargs={"k": 6})


def initialize_qa_chain(vector_store):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store,
        return_source_documents=True
    )


def financial_assessment(qa_chain, situation):
    prompt = (
        f"The following situation involves assessing whether the described financial actions comply with a given contract. "
        f"Analyze the situation solely with attention to the contract’s budget conditions, permissible expenditures, exceptions, "
        f"and any relevant multipliers or adjustments. Specifically, determine whether the described expenditures fall within the budget by considering:\n"
        f"- The base budget limit for the expense.\n"
        f"- cost units provided (one vs. multiple units) and multiply accordingly by the number. With multiple we mean more than one which cloud be two or three or four or even more. State in the final answer, what has been assumed and maybe try out different scenarios if multiple is vage. If you assume a unit number, this makes the decision unclear if there is no clear unit number provided.\n"
        f"- Any relevant multipliers or adjustments(e.g.,for night and weekend travel, high-cost locations, peak seasons, or urgency surcharges) that should be applied based on the scenario.\n"
        f"- The proper sequential multiplication of applicable factors to calculate the final allowable budget.\n"
        f"When applying multiple factors, ensure they are multiplied in the correct order. If there is uncertainty about which multipliers apply, clearly state that and provide an explanation.\n\n"
        f"Situation: {situation}"
    )
    return qa_chain({"query": prompt})


def goal_assessment(qa_chain):
    prompt = (
        f"Could you please describe in a sentence the main objective and goal of the contract. What tasks does the contract involve if it is a service agreement?"
    )
    return qa_chain({"query": prompt})


def non_financial_assessment(qa_chain, situation, goals):
    prompt = (f"Given the contract and the situation provided:\n\n"
        f"Focus solely on non-financial aspects in determining whether the situation violates the contract or not. This includes evaluating whether the expense reason is reasonably related to the contract’s main purpose or work.\n"
        f"Determine whether the expense is reasonably related to the contract’s main purpose or work defined here: {goals} Specifically:"
        f"Assess Expense Relevance: Determine whether the expense is reasonably related to the contract’s main purpose or work (is working location essential for the task to be done there; is the task itself related to the main "
                f"objective; can the work be done remotely instead as for example mainly tasks in the digital world?). Specifically: Alignment with Objectives: "
                        f"Assess if the expense is necessary and contributes to achieving the primary objectives of the contract. Consider if the "
                        f"expenditure is essential for fulfilling the contract’s requirements or if it could be substituted with a less costly or more "
                        f"appropriate alternative. This evaluation should be based on whether the expense supports the contract’s intended outcomes and overall goals. "        
        f"Do not assume non-compliance simply because information (like pre-approvals) is missing. If the situation does not explicitly state that a required action was missed or non-compliance occurred, you should assume compliance.\n"
        f"If you cannot determine non-compliance based on the available non-financial information, conclude that the situation does not violate the contract and provide recommendations for any additional information needed.\n\n"
        f"Decision Criteria:\n"
        f"'Yes': The situation clearly violates the contract’s non-financial requirements (e.g., pre-approval processes, location-specific rules, reporting obligations) or the expense reason is not reasonably related to the contract’s main purpose or work."
        f"'No': The situation does not violate the contract’s non-financial requirements based on the available information, and the expense reason is reasonably related to the contract’s main purpose or work. Missing information should not be treated as a sign of non-compliance unless the situation explicitly shows that something was not done according to the contract."
        f"'Unclear': Use this only if the contract’s non-financial terms are ambiguous, leading to genuine uncertainty in determining compliance, or if it is unclear whether the expense reason is reasonably related to the contract’s main purpose or work."
        f"Situation: {situation}"
    )
    return qa_chain({"query": prompt})


def contract_clarity_check(qa_chain, situation):
    prompt = (
        f"Prompt:\n\n"
        f"You are tasked with evaluating whether a contract is clear and precise regarding a specific situation. Focus on the clarity of the contract in relation to the given situation. Your analysis should address whether the contract explicitly covers the situation or if it contains ambiguous language.\n\n"
        f"Consider the following:\n\n"
        f"1. Clear and Explicit Definitions and Guidance:\n"
        f"- Does the contract provide specific definitions, terms, or clauses that directly address the situation described?\n"
        f"- Are the relevant sections of the contract detailed enough to clearly guide the situation without room for interpretation?\n\n"
        f"2. Ambiguity and Lack of Detail:\n"
        f"- Identify any ambiguous terms or clauses in the contract that relate to the situation. For instance:\n"
        f"- Are there terms that could be interpreted in more than one way?\n"
        f"- Is there a lack of detail that leaves the situation open to interpretation?\n"
        f"- Are there any gaps in the contract where the situation does not fit neatly into the provided terms?\n\n"
        f"3. Application to the Situation:\n"
        f"- Does the contract explicitly apply to the situation described, or does it leave key aspects unresolved?\n"
        f"- Is there a clear way to determine whether the contract applies to the situation based on the language used?\n\n"
        f"Situation: {situation}"
    )
    return qa_chain({"query": prompt})


def final_decision(qa_chain, financial_result, non_financial_result, situation):
    prompt = (
        f"Final Revised Prompt:\n\n"
        f"Given the following inputs:\n\n"
        f"Financial Aspects: {financial_result['result']}\n"
        f"Qualitative Argument: {non_financial_result['result']}\n"
        f"Please provide a final decision on whether the situation to be validated '{situation}' violates the contract. The possible answers are 'yes', 'no', or 'unclear'.\n\n"
        f"Decision Criteria:\n"
        f"'Yes, contract violated': The situation clearly violates the contract terms based on the provided financial aspects and qualitative arguments.\n"
        f"'No contract violation': The situation does not violate the contract terms based on the provided financial aspects and qualitative arguments.\n"
        f"'Unclear': Use this decision only if the contract language itself is ambiguous or does not provide clear guidance on the situation, making it impossible to determine compliance.\n\n"
        f"Detailed Reasoning:\n"
        f"Explain why the situation does or does not violate the contract based on the financial and qualitative aspects.\n"
    )
    return qa_chain({"query": prompt})


def main_evaluation(documents, situation, api):
    # Load documents and initialize components
    documents = load_documents(documents)
    vector_store = initialize_vector_store(documents, api)
    qa_chain = initialize_qa_chain(vector_store)

    # Run assessments
    financial_result = financial_assessment(qa_chain, situation)
    goals = goal_assessment(qa_chain)
    non_financial_result = non_financial_assessment(qa_chain, situation, goals=goals)

    # Perform final evaluation
    final_result = final_decision(qa_chain, financial_result, non_financial_result, situation)

    return final_result
