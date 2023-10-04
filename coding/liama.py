import os 
import replicate

os.environ['REPLICATE_API_TOKEN'] = "r8_FhEaFUEUUwFglCHK4j2pFQJjz6EVGPT2LUNWR"

prompt_input = input("Enter you question: ")

output = replicate.run(
    "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e",
    input={
        "prompt": f"{prompt_input} ",  
        "temperature": 0.1,  
        "top_p": 0.9,  
        "max_length": 256,
        "repitition_penalty": 1
    }
)

full_response = ""

for item in output:
    full_response += item

print(full_response)

print("\n\n")

