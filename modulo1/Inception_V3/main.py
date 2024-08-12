import os
import torch
from PIL import Image
from typing import List
from torchvision import transforms
from torchvision.models import inception_v3, Inception_V3_Weights

CLASSES_NAMES_FILE =  'imagenet_classes.txt'

class Inception_V3:
  def __init__(self): 
    self.model = inception_v3(weights=Inception_V3_Weights.IMAGENET1K_V1)
    self.model.eval()

    if torch.cuda.is_available():
      self.device = 'cuda'
      self.model.to(self.device)
    else:
      self.device = 'cpu'

    classes_file_path = os.path.join(os.path.dirname(__file__), CLASSES_NAMES_FILE)
    with open(classes_file_path, "r") as f:
      self.categories = [s.strip() for s in f.readlines()]

  def predict(self, img_path) -> List[float]:  
    input_image = Image.open(img_path)

    preprocess = transforms.Compose([
      transforms.Resize(256),
      transforms.CenterCrop(224),
      transforms.ToTensor(),
      transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)
    input_batch = input_batch.to(self.device)

    with torch.no_grad():
      output = self.model(input_batch)
    
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    return probabilities.cpu().numpy()
  
  def showCategories(self, probabilities):
    result = []
    for i, probability in enumerate(probabilities):
      result.append((self.categories[i], probability))
    
    return result

  def topCategories(self, probabilities, k):
    result = []
    for i, p in enumerate(probabilities):
      result.append((self.categories[i], float(p)))

    result = list(sorted(result, key=lambda x: x[1], reverse=True))

    return result[:k]