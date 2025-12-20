from helpers.promptGenerators import *
from helpers.modelHelpers import queryModel, parseModelResponseJSON
from helpers.toolHelpers import runToolRequests
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import os

import callableTools
TOOL_MODULES = [callableTools]

load_dotenv(".env", override=True)
load_dotenv(".env.local", override=True)

def runPipeline(query: str):
    tool_prompts = generatePromptForTools(TOOL_MODULES)
    output_only_tools_prompt = json.dumps(list(filter(lambda t: '"output":' in t, tool_prompts)))
    context_enrich_prompt = generateContextEnrichmentPrompt(output_only_tools_prompt, query)
    res = queryModel(context_enrich_prompt)

    print(f"LLM response stage1: {res}")

    tool_requests_stage1 = parseModelResponseJSON(res)
    tool_outputs_stage1 = runToolRequests(tool_requests_stage1, TOOL_MODULES)
    actions_prompt = generateActionsPrompt(json.dumps(tool_prompts), tool_outputs_stage1, query)

    res = queryModel(actions_prompt)

    print(f"LLM response stage2: {res}")

    tool_requests_stage2 = parseModelResponseJSON(res)

    tool_outputs_stage2 = runToolRequests(tool_requests_stage2, TOOL_MODULES)
    final_response_prompt = generateFinalResponsePrompt(output_only_tools_prompt, tool_outputs_stage1 + tool_outputs_stage2, query)
    final_response = queryModel(final_response_prompt)

    return final_response

old_messages = ()


def setUpReceiver():
    def on_message(client, userdata, msg):
        data = msg.payload.decode()

        try:
            res = runPipeline(data)
        except:
            res = "Fail"

        client.publish("telegram/send-message", res)

    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
            client.subscribe("telegram/new-message")
        else:
            print(f"Connection failed, rc={rc}")
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"))
    client.connect(os.getenv("MQTT_BROKER"), 1883, 60)

    client.loop_forever()


def main():
    setUpReceiver()

if __name__ == "__main__":
    main()

# print(runPipeline("Find 1 dragon image on google"))