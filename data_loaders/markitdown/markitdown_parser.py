from markitdown import MarkItDown
from groq import AsyncGroq, Groq
# from openai import OpenAI
import os 
from dotenv import load_dotenv
import time 
import json

load_dotenv()

s = time.time()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
md = MarkItDown(llm_client=client, llm_model="llama-3.2-90b-vision-preview")
workshop_path = "/Users/jaypanchal/week5/AI ML Workshop 2020-21.pdf"
image_path = "/Users/jaypanchal/week5/Image from Slack.jpg"
result = md.convert("/Users/jaypanchal/week5/AI ML Workshop 2020-21.pdf")
e = time.time()
print(result.text_content)
print(f"Time Taken: {e-s}")
print(dir(result))
print(result.title)


# print(f"Prompt Tokens: {result.usage['prompt_tokens']}")
# print(f"Completion Tokens: {result.usage['completion_tokens']}")
# print(f"Total Tokens: {result.usage['total_tokens']}")


'''
output of the code of model : llama-3.2-11b-vision-preview, 2.45 seconds

this is accurate in the sense that there are only 3 image collage in the Orignal image 

# Description:
This image is a collage of three photographs of a water cooler with a clear, 
translucent front panel, showcasing its design and functionality.

In the leftmost image, the front panel is depicted without any water,
highlighting its transparent nature. The remaining two images display the machine 
in its everyday operational state, with one showing the clear panel being used to dispense
fresh water from the black spout.

The photographs convey a mundane yet intriguing aesthetic, capturing the water cooler's essential 
role in providing hydration in a corporate or office setting.

'''




'''

output of the code of model : llama-3.2-90b-vision-preview, 3.3 seconds
# Description:
The image features a series of photographs showcasing a white water cooler with a clear, rectangular water bottle, encased in a blue cover and situated in various settings.

Starting from the far left, the first photo offers a close-up view of the water bottle through the 
cover, with the blue filter on top. The second photo shows the 
water cooler in a white-tiled bathroom alongside a row of silver urinals. The third photo 
presents a closer view of the water cooler, in the background are two white sinks mounted on the wall
. The fourth photo depicts the water cooler installed within office seating arrangements, and the
 fifth photo shows it installed within a plane next to a circular window.

In addition to the water cooler, various objects are visible, including white-tiled bathroom walls,
 silver urinals, silver pipes, and sinks with a silver faucet in the bathroom, a person in white shirt
   and blue vest standing next to the water cooker, office chairs under a white desk, and a grey a
   irplane interior with the words "THAN PERFECT" visible to the right. Overall, the water cooler
     is prominently displayed in a range of settings, likely for business purposes.



'''