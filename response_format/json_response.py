from typing import List, Optional, Dict, Any
import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from groq import Groq
import json
import httpx
import time

load_dotenv()

groq = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

# Data model for LLM to generate
class Ingredient(BaseModel):
    name: str
    quantity: str
    quantity_unit: Optional[str]


class Recipe(BaseModel):
    recipe_name: str
    ingredients: List[Ingredient]
    directions: List[str]

class RecipeJSON:
    def __init__(self, recipe_name: str, ingredients: List[Ingredient], directions: List[str]):
        self.recipe_name = recipe_name
        self.ingredients = ingredients
        self.directions = directions

    def to_dict(self) -> dict:
        return {
            "recipe_name": self.recipe_name,
            "ingredients": [ingredient.model_dump() for ingredient in self.ingredients],
            "directions": self.directions,
        }

def pretty_print(data: dict):
    print(json.dumps(data, indent=2))
    



def make_groq_request(messages: List[Dict[str, str]], temperature: float = 0.7) -> Dict[Any, Any]:

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    data = {
        "messages": messages,
        "model": "llama-3.3-70b-versatile",
        "temperature": temperature,
        "max_completion_tokens": 1000,
        "response_format" : {"type": "json_object"}
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(BASE_URL, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None





def api_call_recipe(recipe_name: str) -> Dict[Any, Any]:
    messages=[
            {
                "role": "system",
                "content": "You are a recipe database that outputs recipes in JSON.\n"
                # Pass the json schema to the model. Pretty printing improves results.
                f" The JSON object must use the schema: {json.dumps(Recipe.model_json_schema(), indent=2)}",
            },
            {
                "role": "user",
                "content": f"Fetch a recipe for {recipe_name}",
            },
        ]
    response =  make_groq_request(messages)
    recipe = Recipe.model_validate_json(response["choices"][0]["message"]["content"])
    recipe_json = RecipeJSON(recipe.recipe_name, recipe.ingredients, recipe.directions)
    return recipe_json.to_dict()

def get_recipe(recipe_name: str) -> Recipe:
    
    chat_completion = groq.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a recipe database that outputs recipes in JSON.\n"
                # Pass the json schema to the model. Pretty printing improves results.
                f" The JSON object must use the schema: {json.dumps(Recipe.model_json_schema(), indent=2)}",
            },
            {
                "role": "user",
                "content": f"Fetch a recipe for {recipe_name}",
            },
        ],
        model="llama3-70b-8192",
        temperature=0,
        # Streaming is not supported in JSON mode
        stream=False,
        response_format={"type": "json_object"},
    )
    
    recipe = Recipe.model_validate_json(chat_completion.choices[0].message.content)
    recipe_json = RecipeJSON(recipe.recipe_name, recipe.ingredients, recipe.directions)
    print(pretty_print(recipe_json.to_dict()))
    return Recipe.model_validate_json(chat_completion.choices[0].message.content)


def print_recipe(recipe: Recipe):
    print("Recipe:", recipe.recipe_name)

    print("\nIngredients:")
    for ingredient in recipe.ingredients:
        print(
            f"- {ingredient.name}: {ingredient.quantity} {ingredient.quantity_unit or ''}"
        )
    print("\nDirections:")
    for step, direction in enumerate(recipe.directions, start=1):
        print(f"{step}. {direction}")


# s_sdk = time.time()
# recipe = get_recipe("apple pie")
# print_recipe(recipe)
# print("Time taken for sdk: ", time.time()-s_sdk)
# # 2.29 seconds


s_api = time.time()
recipe = api_call_recipe("apple pie") 
print(pretty_print(recipe))
print("Time taken for api: ", time.time()-s_api)
# 2.65 seconds