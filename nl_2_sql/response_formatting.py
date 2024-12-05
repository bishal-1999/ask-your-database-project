from langchain.prompts import PromptTemplate
from llm_interface import get_llm_endpoint


####################################################################################################################################

format_template = """
<s>[INST] You are an expert at converting raw database output into clear, concise, and human-readable answers.
Generate a natural language answer based on the user's question and the provided data:
Question: {question}
Data: {data}
Use clear and precise language to summarize the information. Provide additional context if necessary, but avoid including irrelevant details. 
[/INST]</s>"""

format_prompt_template = PromptTemplate.from_template(format_template)


####################################################################################################################################

def generate_formatted_answer(question, data):
    llm = get_llm_endpoint()
    formatted_prompt = format_prompt_template.format(question=question, data=data)
    
    response = llm.stream(formatted_prompt)
    final_report = ''.join([res for res in response])
    
    return final_report.strip().replace("</s>", "").replace("<s>", "")


####################################################################################################################################