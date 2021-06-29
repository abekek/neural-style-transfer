# Define imports
try:
    import unzip_requirements
except ImportError:
    pass

import json
from io import BytesIO
import pathlib
import base64
import logging
import re

import boto3
import numpy as np
from PIL import Image

import torch
import torchvision.transforms as transforms
from torch.autograd import Variable
from network.transformer_net import TransformerNet

def img_to_base64_str(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)
    img_byte = buffered.getvalue()
    img_str = "data:image/png;base64," + base64.b64encode(img_byte).decode()
    return img_str

def load_models(s3, bucket):
    logging.debug('loading models')
    pathlib.Path(__file__).parent.resolve()
    styles = ["Rain Princess", "Candy", "Mosaic", "Udnie"]
    style_paths = ['serverless/backend/dev/models/rain_princess.pth', 'serverless/backend/dev/models/candy.pth', 'serverless/backend/dev/models/mosaic.pth', 'serverless/backend/dev/models/udnie.pth']
    models = {}

    for i in range(len(style_paths)):
        with torch.no_grad():
            model = TransformerNet()
            response = s3.get_object(Bucket=bucket, Key=style_paths[i])
            state = torch.load(BytesIO(response["Body"].read()))
            for k in list(state.keys()):
                if(re.search(r'in\d+\.running_(mean|var)$', k)):
                    del state[k]
        model.load_state_dict(state)
        model.eval()
        models[styles[i]] = model

    return models

gpu = -1

logging.debug('bucket loading')
s3 = boto3.client("s3")
bucket = 'backend-dev-serverlessdeploymentbucket-1w4gicr8a38h8'
logging.debug('bucket loaded')

mapping_id_to_style = {
    0: "Rain Princess",
    1: "Candy",
    2: "Mosaic",
    3: "Udnie"
}

models = load_models(s3, bucket)
logging.debug('models loaded...')

# normalizing the float to uint8
def normalize8(I):
  mn = I.min()
  mx = I.max()

  mx -= mn

  I = ((I - mn)/mx) * 255
  return I.astype(np.uint8)

def lambda_handler(event, context):
  """
  lambda handler to execute the image transformation
  """
  # warming up the lambda
  if(event.get("source") in ["aws.events", "serverless-plugin-warmup"]):
      print('Lambda is warm!')
      return {}

  # extracting the image form the payload and converting it to PIL format
  data = json.loads(event["body"])
  print("data keys :", data.keys())
  image = data["image"]
  image = image[image.find(",")+1:]
  dec = base64.b64decode(image + "===")
  image = Image.open(BytesIO(dec))
  image = image.convert("RGB")

  # loading the model with the selected style based on the model_id payload
  model_id = int(data["model_id"])
  style = mapping_id_to_style[model_id]
  model = models[style]

  # resize the image based on the load_size payload
  load_size = int(data["load_size"])

  h = image.size[0]
  w = image.size[1]
  ratio = h * 1.0 / w
  if ratio > 1:
      h = load_size
      w = int(h*1.0 / ratio)
  else:
      w = load_size
      h = int(w * ratio)

  image = image.resize((h, w), Image.BICUBIC)
  image = np.asarray(image)

  # convert PIL image from  RGB to BGR
  image = image[:, :, [2, 1, 0]]
  image = transforms.ToTensor()(image).unsqueeze(0)

  # transform values to (-1, 1)
  image = -1 + 2 * image
  if gpu > -1:
      image = Variable(image, volatile=True).cuda()
  else:
      image = image.float()

  # style transformation
  with torch.no_grad():
      output_image = model(image)
      output_image = output_image[0]

  output_image = normalize8(output_image.cpu().numpy())
  output_image = Image.fromarray(output_image.transpose(1, 2, 0))

  # convert the PIL image to base64
  result = {
      "output": img_to_base64_str(output_image)
  }

  # send the result back to the client inside the body field
  return {
      "statusCode": 200,
      "body": json.dumps(result),
      "headers": {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
      }
  }