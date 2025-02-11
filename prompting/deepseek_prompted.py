import httpx
import json
from typing import Dict, List, Any
import time
from datetime import datetime
import asyncio
import os 
from dotenv import load_dotenv


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

async def make_groq_request(messages: List[Dict[str, str]], temperature: float = 0.7) -> Dict[Any, Any]:
    """Make a request to Groq API"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    data = {
        "messages": messages,
        "model": "llama-3.3-70b-versatile",
        "temperature": temperature,
        "max_tokens": 1000,
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(BASE_URL, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None

def save_response_to_file(technique: str, response: Dict[str, Any], filename: str = "prompt_responses.txt"):
    """Save response to a text file with proper formatting"""
    if response and 'choices' in response:
        content = response['choices'][0]['message']['content']
        
        with open(filename, "a") as file:
            file.write(f"\n\n=== {technique.upper()} ===\n")
            file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("-" * 80 + "\n")
            file.write(content + "\n")
            file.write("=" * 80 + "\n")

async def compare_prompting_techniques():
    """Compare different prompting techniques"""
    results = {}
    output_file = "prompt_responses.txt"
    
    # Clear previous content if file exists
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # 1. Zero-shot Prompting
    print("\n=== Zero-shot Prompting ===")
    zero_shot_messages = [{
        "role": "user",
        "content": "Analyze the environmental impact of electric vehicles compared to traditional gasoline vehicles."
    }]
    
    zero_shot_response = await make_groq_request(zero_shot_messages)
    save_response_to_file("Zero-shot Prompting", zero_shot_response, output_file)
    
    # 2. Few-shot Prompting
    print("\n=== Few-shot Prompting ===")
    few_shot_messages = [{
        "role": "user",
        "content": """Here are some examples of environmental impact analyses:

Example 1:
Topic: Solar panels
Analysis: Solar panels reduce carbon emissions by generating clean electricity. However, their production requires mining rare materials and energy. Overall impact is positive over their lifetime.

Example 2:
Topic: Plant-based meat
Analysis: Plant-based meat reduces water usage and land requirements compared to animal agriculture. Production has lower carbon footprint. Some processing energy required. Net positive environmental impact.

Now analyze: Electric vehicles compared to traditional gasoline vehicles."""
    }]
    
    few_shot_response = await make_groq_request(few_shot_messages)
    save_response_to_file("Few-shot Prompting", few_shot_response, output_file)
    
    # 3. Chain of Thought Prompting
    print("\n=== Chain of Thought Prompting ===")
    cot_messages = [{
        "role": "user",
        "content": """Let's analyze the environmental impact of electric vehicles vs gasoline vehicles step by step:

1. First, let's consider the manufacturing process for both types
2. Then, analyze the energy sources and efficiency
3. Next, evaluate the lifetime emissions
4. After that, examine the disposal and recycling impact
5. Finally, draw a conclusion based on all factors

Please follow this thinking process to provide a detailed analysis."""
    }]
    
    cot_response = await make_groq_request(cot_messages)
    save_response_to_file("Chain of Thought Prompting", cot_response, output_file)
    
    # 4. Meta Prompting
    print("\n=== Meta Prompting ===")
    meta_messages = [{
        "role": "user",
        "content": """You are an expert environmental analyst with decades of experience in lifecycle assessment. 
        Using your expertise, create a framework for analyzing the environmental impact of electric vehicles vs gasoline vehicles.
        Consider all aspects from manufacturing to disposal, and be sure to:
        - Draw upon scientific research
        - Use quantitative metrics where possible
        - Consider regional variations
        - Account for future technological developments
        
        Structure your response as a professional analysis report."""
    }]
    
    meta_response = await make_groq_request(meta_messages)
    save_response_to_file("Meta Prompting", meta_response, output_file)
    
    # 5. Prompt Chaining
    print("\n=== Prompt Chaining ===")
    manufacturing_messages = [{
        "role": "user",
        "content": "Analyze only the manufacturing environmental impact of electric vs gasoline vehicles."
    }]
    manufacturing_response = await make_groq_request(manufacturing_messages)
    
    operation_messages = [{
        "role": "user",
        "content": "Analyze only the operational environmental impact of electric vs gasoline vehicles."
    }]
    operation_response = await make_groq_request(operation_messages)
    
    if manufacturing_response and operation_response:
        final_chain_messages = [{
            "role": "user",
            "content": f"""Based on these two analyses, provide a comprehensive conclusion:

Manufacturing Analysis:
{manufacturing_response['choices'][0]['message']['content']}

Operation Analysis:
{operation_response['choices'][0]['message']['content']}

Please synthesize these findings into a final comparison."""
        }]
        
        final_chain_response = await make_groq_request(final_chain_messages)
        save_response_to_file("Prompt Chaining", final_chain_response, output_file)
    
    # 6. Tree of Thoughts
    print("\n=== Tree of Thoughts Prompting ===")
    tot_messages = [{
        "role": "user",
        "content": """Let's analyze the environmental impact of electric vs gasoline vehicles using multiple perspectives and exploring different possibilities:

Branch 1 - Optimistic Scenario:
- Assume rapid renewable energy adoption
- Consider breakthrough battery technology
- Factor in improving recycling methods

Branch 2 - Pessimistic Scenario:
- Consider continued fossil fuel dependency
- Account for battery disposal challenges
- Factor in raw material scarcity

Branch 3 - Balanced Scenario:
- Mix of energy sources
- Gradual technology improvement
- Moderate recycling advancement

For each branch, evaluate the environmental impact and then synthesize the insights into a final conclusion."""
    }]
    
    tot_response = await make_groq_request(tot_messages)
    save_response_to_file("Tree of Thoughts Prompting", tot_response, output_file)
    
    return {
        "zero_shot": zero_shot_response,
        "few_shot": few_shot_response,
        "chain_of_thought": cot_response,
        "meta": meta_response,
        "tree_of_thoughts": tot_response,
        "prompt_chaining": final_chain_response if manufacturing_response and operation_response else None
    }

def analyze_results(results: Dict[str, Any]):
    """Analyze and compare results from different prompting techniques"""
    print("\n=== Prompting Techniques Comparison ===")
    
    for technique, response in results.items():
        if response and 'choices' in response:
            content = response['choices'][0]['message']['content']
            token_count = len(content.split())
            
            print(f"\n{technique.upper()} ANALYSIS:")
            print(f"Token count: {token_count}")
            print(f"Response preview: {content[:200]}...")
            print("-" * 80)

if __name__ == "__main__":
    s = time.time()
    print("Starting prompt engineering comparison...")
    results = asyncio.run(compare_prompting_techniques())
    analyze_results(results)
    print("\nResponses saved to 'prompt_responses.txt'")
    print(f"Total time taken : {time.time() - s }")