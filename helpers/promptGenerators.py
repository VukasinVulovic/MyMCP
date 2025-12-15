import json
import inspect
import sys
from dotenv import load_dotenv
load_dotenv()

def generatePromptForTools(modules: list):
    tool_prompts = []

    for mod in modules:
        for _, obj in inspect.getmembers(mod):
            for _, member in inspect.getmembers(obj):
                if isinstance(member, (staticmethod, classmethod)):
                    func = member.__func__
                elif inspect.isfunction(member):
                    func = member
                else:
                    continue

                if hasattr(func, "__tool_prompt__"):
                    tool_prompts.append(func.__tool_prompt__)

    return json.dumps(tool_prompts)

def generateContextEnrichmentPrompt(tools_prompt: str, user_query: str):
    with open("./prompts/context_enrichment.txt", "r") as f:
        return f.read().replace("{tools}", tools_prompt).replace("{user_query}", user_query)
    
def generateActionsPrompt(tools_prompt: str, tools_outputs: list, user_query: str):
    with open("./prompts/action.txt", "r") as f:
        return f.read().replace("{tools}", tools_prompt).replace("{tools_outputs}", json.dumps(tools_outputs)).replace("{user_query}", user_query)
    
def generateFinalResponsePrompt(tools_prompt: str, tools_outputs: list, user_query: str):
    with open("./prompts/final_response.txt", "r") as f:
        return f.read().replace("{query}", user_query).replace("{tool_outputs}", json.dumps(tools_outputs))