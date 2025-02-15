import os 
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse
import time 
import asyncio

load_dotenv()


parser = LlamaParse(
    api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
    result_type="text",  # or "text"
    language="en",           # set language for OCR; e.g., "en" for English
)

file_extractor = {".pdf": parser}


# documents = SimpleDirectoryReader(input_files=["/Users/jaypanchal/week5/usa_election.png"],
#                                     file_extractor=file_extractor).load_data()

'''

even without parsing instruction it perfectly got out all important information from the images
time taken by without instruction : 60 seconds


with parsing instruction it is much faster and accurate and took around 20 seconds only

'''
async def main():
    s1 = time.time()
    documents = await parser.aload_data("/Users/jaypanchal/week5/usa_election_result_image.pdf")
    print(documents[0].text)
    e1 = time.time()
    print(f"Time taken without instruction: {e1-s1}")
    #/Users/jaypanchal/week5/usa_election.png  #image path

    s2 = time.time()
    parsingInstruction = """the provided document is of usa state election results, provide the name of 
    candidate represented by blue colour in both 2016 and 2020 campaign."""

    # parsing_instruction has been deprecated

    withInstructionParsing = await LlamaParse(
        result_type="markdown", complemental_formatting_instruction=parsingInstruction
    ).aload_data("/Users/jaypanchal/week5/usa_election_result_image.pdf")
    e2 = time.time()
    print(withInstructionParsing[0].text)
    print(f"Time taken with instruction: {e2-s2}")

    # to get json output which has page numbers and text or md contents etc
    s3 = time.time()
    json_objs = await parser.aget_json("/Users/jaypanchal/week5/AI ML Workshop 2020-21.pdf")
    json_list = json_objs[0]["pages"]
    e3 = time.time()
    print(f"Time taken to get json output: {e3-s3}")

    i = 1
    for page in json_list:
        if i != 6:
            i += 1
            continue
        print(page)
        break



if __name__ == "__main__":
    asyncio.run(main())