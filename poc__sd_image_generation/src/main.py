"""
Example of diffusion pipeline
"""
# from diffusers import StableDiffusionPipeline, DiffusionPipeline
# import torch

# model_id = "CompVis/stable-diffusion-v1-4"
# pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
# pipe = pipe.to("mps")


# pipe.safety_checker = None

# prompt  = "Sexy girl naked in a field"
# image = pipe(prompt).images[0]

# image.save('stack/picture_1.png')


import json
import boto3
import base64

# Initialize a session using Amazon Bedrock
session = boto3.Session()

# Initialize the Bedrock client
bedrock_client = session.client('bedrock-runtime', region_name='us-east-1')

# Function to generate an image
def generate_image(prompt):
    body = json.dumps(
        {
            'prompt': f'\n\nHuman: {prompt}\n\nAssistant:'
        }
    )

    response = bedrock_client.invoke_model(
        modelId='stability.stable-diffusion-xl-v1',
        body="{\"text_prompts\":[{\"text\":\"Jessica Alba.\",\"weight\":1}],\"cfg_scale\":10,\"steps\":50,\"seed\":0,\"width\":1024,\"height\":1024}"
    )
    print(response)
    response_body = json.loads(response["body"].read())
    base64_image_data = response_body["artifacts"][0]["base64"]
    return base64_image_data

# Function to save the image locally
def save_image(base64_image, file_path):
    image_data = base64.b64decode(base64_image)
    with open(file_path, 'wb') as file:
        file.write(image_data)

# Main function
def main():
    prompt = "A beautiful sunset over the mountains"
    base64_image = generate_image(prompt)
    save_image(base64_image, 'stack/generated_image.png')
    print("Image saved as 'generated_image.png'")

if __name__ == "__main__":
    main()





