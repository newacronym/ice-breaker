import os
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser


def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_username, mock=True)

    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them

    Use information from linkedin
    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables = ["information"], 
        template = summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()},
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    chain = summary_prompt_template | llm | summary_parser
    linkedin_data = scrape_linkedin_profile("https://www.linkedin.com/in/harshit-gupta-561543190/", mock=True)
    res = chain.invoke(input={"information": linkedin_data})

    print(res)

if __name__ == "__main__":
    load_dotenv()

    print("ice breaker Enter")
    res = ice_break_with(name="Harshit Gupta")
    
    

    