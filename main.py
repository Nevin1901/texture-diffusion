import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, LMSDiscreteScheduler
from dotenv import load_dotenv
import os
from flask import Flask, request, send_file

app = Flask(__name__)
# prompt = "a photo of an astronaut riding a horse on mars"
# prompt = "a photo of a realistic double door flat texture, realistic 8k"
# prompt = "high quality simple top down 2d grass texture"
# prompt = "high quality dark slate bricks 2d texture"
# prompt = "Rockefeller Christmas Tree full frame high quality"
# prompt = "Ground Control to Major Tom abstract painting high res"


# print("saving")
# image.save("tree2.png")

@app.route("/")
def index():
    args = request.args
    text = args.get("name")
    samples = args.get("samples")

    if samples is None:
        samples = 1

    print(samples)
    print(text)
    print("generating")
    with autocast("cuda"):
        image = pipe(text, guidance_scale=7.5, height=512, width=512)["sample"][0]
        # print(image)
        # print(dir(image))
        print("saving")
        image.save(f"{text}.png")

    return send_file(f"{text}.png", mimetype="image/png")



if __name__ == "__main__":
    print("got here")

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
    print("done")

    app.run()

