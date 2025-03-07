from dotenv import load_dotenv
from openai import OpenAI
import json
import pandas as pd
pd.set_option('future.no_silent_downcasting', True)
# Load environment variables
load_dotenv()
client = OpenAI()

# Function to process OpenAI JSON response safely
def parse_json_response(response):
    try:
        response = response.strip().replace("```json", "").replace("```", "")  # Clean unwanted formatting
        return json.loads(response)
    except json.JSONDecodeError as e:
        print("Error decoding JSON response:", response)  # Log the problematic response for debugging
        raise ValueError("Invalid JSON response from OpenAI") from e

# Bias Detection Agent
def bias_agent(column_name, description, long_description, text_body):
    messages = [
        {
            "role": "developer",
            "content": f"""
            You are an analytical assistant searching for cognitive biases in a given text. Your job is to identify if {description} is present and provide VERBATIM evidence from the text.
            
            **Definition of {description}:**
            {long_description}
            
            **Output Requirements:** 
            - Return a **valid JSON object**.
            - The JSON must contain:
              - A boolean key named "{column_name}" indicating if the bias is present (`true` or `false`).
              - A key named `"evidence"` with the exact part of the text where the bias appears.
            - If multiple instances exist, return them in a **JSON array**.
            - Output MUST include every instance of {description} found in the text. If a sentence contains {description}, return it as evidence.  Your evidence must perfectly match the original text.


            **Example Output:**
            ```json
            [
                {{"{column_name}": true, "evidence": "Exact text where the bias appears."}}
            ]
            ```

            """
        },
        {
            "role": "user",
            "content": text_body
        }
    ]

    completion = client.chat.completions.create(
        model="gpt-4o",
        store=True,
        messages=messages,
        seed=531
    )

    response_text = completion.choices[0].message.content.strip()  # Get raw response
    return parse_json_response(response_text)  # Parse JSON safely

# Logical Fallacy Detection Agent
def logic_agent(column_name, description, long_description, text_body):
    messages = [
        {
            "role": "developer",
            "content": f"""
            You are an analytical assistant searching for logical fallacies in a given text. Your job is to identify if the following logical fallacy is present: **{description}**, and provide VERBATIM evidence from the text.

            **Definition of {description}:**
            {long_description}

            **Output Requirements:** 
            - Return a **valid JSON object**.
            - The JSON must contain:
              - A boolean key named "{column_name}" indicating if the fallacy is present (`true` or `false`).
              - A key named `"evidence"` with the exact part of the text where the fallacy appears.
            - If multiple instances exist, return them in a **JSON array**.
            - Output MUST include every instance of {description} found in the text. If a sentence contains {description}, return it as evidence.  Your evidence must perfectly match the original text.
            
            **Example Output:**
            ```json
            [
                {{"{column_name}": true, "evidence": "Exact text where the fallacy appears."}}
            ]
            ```
            
            """
        },
        {
            "role": "user",
            "content": text_body
        }
    ]

    completion = client.chat.completions.create(
        model="gpt-4o",
        store=True,
        messages=messages,
        seed=531
    )

    response_text = completion.choices[0].message.content.strip()  # Get raw response
    return parse_json_response(response_text)  # Parse JSON safely


def agentic_analysis(text_body):
    # Load Configuration
    with open("agent_config.json") as f:
        agent_config = json.load(f)
    
    bias_config = agent_config.get("biases", [])
    logic_config = agent_config.get("logic", [])
    
    # Process Biases
    bias_data = []
    for row in bias_config:
        result = bias_agent(row["column_name"], row["description"], row["long_description"], text_body)
        bias_data.append(result)
    bias_data=[
        x
        for xs in bias_data
        for x in xs if x not in (None,[])
    ]
    # Process Logical Fallacies
    logic_data = []
    for row in logic_config:
        result = logic_agent(row["column_name"], row["description"], row["long_description"], text_body)
        logic_data.append(result)
    logic_data=[
        x
        for xs in logic_data
        for x in xs if x not in (None,[])
    ]
    combined=logic_data+bias_data
    df=pd.DataFrame(combined)

    cols=[i['column_name'] for i in bias_config+logic_config]
    existing_cols=list(df.columns)
    for i in cols:
        if i not in existing_cols:
            df[i]=float('nan')
    if len(df)==0:
        df.loc[len(df)] = False
    if 'evidence' not in list(df.columns):
        df['evidence']=''
    # df=df[df['evidence'] != '']
    # df=df.dropna(subset=['evidence'])
    df=df.fillna(False)
    df=df.groupby("evidence", as_index=False).max()


    return df