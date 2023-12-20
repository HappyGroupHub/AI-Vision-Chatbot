import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import aoai
import ai_vision
import utilities as utils

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

env = utils.read_env()


@app.post("/api/generate_image")
async def generate_image(request: Request):
    """Generate image from text.

    :param Request request: Request
    :return dict response: Response
    """
    request_body = await request.json()
    prompt = request_body['text']
    response = aoai.generate_image_with_text(prompt)
    return FileResponse(response['image_path'])


@app.post("/api/generate_text")
async def generate_text(request: Request):
    """Generate text from image.

    :param Request request: Request
    :return dict response: Response
    """
    request_body = await request.json()
    image_url = request_body['image_url']
    response = ai_vision.get_image_caption(image_url)
    return response


@app.post("/api/echo")
async def echo(request: Request):
    """Echo.

    :param Request request: Request
    :return dict response: Response
    """
    request_body = await request.json()
    message = request_body['message']
    return {'botResponse': message}


if __name__ == '__main__':
    uvicorn.run(app, port=5000)
