from groq import Groq
import base64
import time 
import os
from dotenv import load_dotenv
load_dotenv()


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "/Users/jaypanchal/week5/Image from Slack.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

s = time.time()
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", 
                 "text": '''List what you observe in this photo in JSON format
                list out all images and all objects in an image
                with in depth descriotion

                ```
                this is the output format 
                {
                    "images": [
                        {
                            "image_name": "string",  // image number
                            "objects": [
                                {
                                "object_name": "string",  // Name of the detected object
                                "description": "string",  // Description of the detected object
                                "position": "string"  // Position in words (e.g., "upper left", "bottom right", "center")
                                }
                            ]
                        }
                    ]
                }
                ```
                 '''},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
    model="llama-3.2-11b-vision-preview",
    response_format={"type": "json_object"},
)
e = time.time()

print(chat_completion.choices[0].message.content)
print(f"Time Taken: {e-s}")


usage = chat_completion.usage
print(f"Prompt Tokens: {usage.prompt_tokens}")
print(f"Completion Tokens: {usage.completion_tokens}")
print(f"Total Tokens: {usage.total_tokens}")







"""


COT : Chain of thoughts
```
                follow this chain of thoughts (COT) process to describe the image:
                1) first look at the image and decide if it is a collage or not
                2) if it is not collage then describe the image directly in depth
                3) if it is a collage then carefully count the number of sub images in the collage
                4) again count the number of sub images in the collage if it matches then only go to next step else go back to step 3
                4) describe each image of the collage with their location and description in depth

                ```



2 shot prompts

```
                 example 1: 
                    the image is a collage containting 3 images
                    1) first image 
                        location : top left corner
                        description : in this image there is a red car in front of a house and the sky is clear
                    2) second image 
                        location : top right corner
                        description : in this image a cat is sleeping on the sofa
                    3) third image 
                        location : bottom left corner
                        description : in this image there is a skyshot firecracker in the sky bursting brightly
                    4) fourth image 
                        location : bottom right corner
                        description : in this image there is a rocket leaving the earth, rocket is saturn V
                 
                 example 2:
                    this image is not a collage :
                    description : in this image a dog is running on the grass field with a long stick in
                    his mouth and the sky is clear and the sun is shining brightly in the background
                 
                 ```

"""