import os 
from dotenv import load_dotenv
import httpx 
import aiofiles
import asyncio
import time

load_dotenv()

def clean_whitespace(text):
    return ' '.join(text.split())


async def parse_pdf_raw_api_call(file_path: str) -> dict:

    LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    BASE_LLAMAPARSE_URL = "https://api.cloud.llamaindex.ai/api/parsing"

    if not LLAMA_CLOUD_API_KEY:
        raise ValueError("LLAMA_CLOUD_API_KEY is not set in the environment variables.")

    headers = {"Authorization": f"Bearer {LLAMA_CLOUD_API_KEY}"}

    try:
        async with aiofiles.open(file_path, "rb") as f:
                file_bytes = await f.read()
    except Exception as e:
        raise Exception(f"Failed to read file: {file_path}. Error: {str(e)}")
    
    files = {
        "file": ("file.pdf", file_bytes, "application/pdf")
    }

    url = f"{BASE_LLAMAPARSE_URL}/upload"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, files=files)
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
                raise Exception(f"API call failed with status code {e.response.status_code}. Error: {str(e)}")
        
        # here we will get the job id from response and then check for its status
        print(response.json())
        print(response.status_code)
        job_id = response.json()["id"]
        result_type = "json"#"text" # or it can be "markdown"

        status_url = f"{BASE_LLAMAPARSE_URL}/job/{job_id}"
        result_url = f"{BASE_LLAMAPARSE_URL}/job/{job_id}/result/{result_type}"

        while True:
            try : 
                status_response = await client.get(status_url, headers=headers)
                status_response.raise_for_status()
                status_data = status_response.json()
                job_status = status_data["status"]
                if job_status == "COMPLETED":
                    break

                response = await client.get(result_url, headers=headers)
                print(f"in get request {response.json()}")
                print(response.status_code)
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise Exception("Job not found.")
                else:
                    print("Waiting for response...")
                    await asyncio.sleep(2)
                    continue
            
            if response.status_code == 200:
                break
            

        
        result = response.json()
        output = result.get(result_type, "")
        if not output:
            raise Exception(f"No {result_type} output found in the API response.")
        # output = result[result_type]
        return output
    

async def main():
    s = time.time()
    file_path = "/Users/jaypanchal/week5/attention_is_all_you_need.pdf"
    encode_path = "/Users/jaypanchal/week5/AI ML Workshop 2020-21.pdf"
    gpt2_path = "/Users/jaypanchal/week5/gpt2_paper.pdf"
    try : 
        output = await parse_pdf_raw_api_call("/Users/jaypanchal/week5/AI ML Workshop 2020-21.pdf")
    except Exception as e:
        print(f"Error occurred in main: {str(e)}")
        return
    
    e = time.time()

    print(output[:100])
    print(f"type of output : {type(output)}")
    print(f"Length of output: {len(output)}")

    cleaned_text = clean_whitespace(output)
    try :
        async with aiofiles.open("ai_ml_text.txt", mode='a') as file:
            await file.write(cleaned_text)
    except Exception as e:
        print(f"Error occurred while writing to file: {str(e)}")

    print(cleaned_text[:100])

    print(f"Time taken: {e-s}")


if __name__ == "__main__":
    asyncio.run(main())