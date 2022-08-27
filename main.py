import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, LMSDiscreteScheduler
from dotenv import load_dotenv
import os

load_dotenv()

model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda"

auth_token = os.getenv("AUTH_TOKEN")
print(auth_token)

print("creating scheduler")
scheduler = LMSDiscreteScheduler(
    beta_start=0.00085,
    beta_end=0.012,
    beta_schedule="scaled_linear",
    num_train_timesteps=1000,
)

print("creating pipe")
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    revision="fp16",
    scheduler=scheduler,
    use_auth_token=auth_token,
)

print("pipe to cuda")
pipe = pipe.to(device)

# prompt = "a photo of an astronaut riding a horse on mars"
# prompt = "a photo of a realistic double door flat texture, realistic 8k"
# prompt = "high quality simple top down 2d grass texture"
# prompt = "high quality dark slate bricks 2d texture"
prompt = "Rockefeller Christmas Tree full frame high quality"

print("generating")
with autocast("cuda"):
    image = pipe(prompt, guidance_scale=7.5)["sample"][0]

print("saving")
image.save("tree.png")
