import openai
import os
import requests
from PIL import Image
from io import BytesIO
 
# Use an environment variable for the API key
openai.api_key = os.getenv('OPENAI_API_KEY')
 
def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url
 
def display_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.show()
 
# Example usage
prompt = input("Enter your prompt: ")
image_url = generate_image(prompt)
display_image(image_url)
