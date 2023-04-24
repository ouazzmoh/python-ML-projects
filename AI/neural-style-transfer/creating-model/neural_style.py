from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import time

import torch
import torch.optim as optim
import requests
from torchvision import transforms, models

from model import config
import sys
import os
from torch import nn
from model.network import SimpleDetector

model = torch.load(config.BEST_MODEL_PATH).to(config.DEVICE).features
for param in model.parameters():
    param.requires_grad = False
device = config.DEVICE
model.to(device)


def image_loader(path):
    image = Image.open(path)
    loader = transforms.Compose([
        transforms.Resize(size=(224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = loader(image).unsqueeze(0)
    return image.to(config.DEVICE)

content = image_loader('tesla.jpeg')
style = image_loader('van_gogh.jpg')

# helper function for un-normalizing an image 
# and converting it from a Tensor image to a NumPy image for display
def im_convert(tensor):
    """ Display a tensor as an image. """
    
    image = tensor.to("cpu").clone().detach()
    image = image.numpy().squeeze()
    image = image.transpose(1,2,0)
    image = image * np.array((0.229, 0.224, 0.225)) + np.array((0.485, 0.456, 0.406))
    image = image.clip(0, 1)

    return image

# display the images
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
# content and style ims side-by-side
ax1.imshow(im_convert(content))
ax2.imshow(im_convert(style))
plt.show()

def get_features(image, model, layers=None):
    if layers is None:
        layers = {'0': 'conv1_1',
                  '4': 'conv2_1', 
                  '8': 'conv3_1', 
                  '12': 'conv4_1',
                  '16': 'conv5_1'}  ## content representation
    features = {}
    x = image
    # model._modules is a dictionary holding each module in the model
    for name, layer in model._modules.items():
        x = layer(x)
        if name in layers:
            features[layers[name]] = x
    return features


# print(get_features(content, model))


def gram_matrix(tensor):    
    # get the batch_size, depth, height, and width of the Tensor
    _, d, h, w = tensor.size()
    
    # reshape so we're multiplying the features for each channel
    tensor = tensor.view(d, h * w)
    
    # calculate the gram matrix
    gram = torch.mm(tensor, tensor.t())
    
    return gram 

content_features = get_features(content, model)
style_features = get_features(style, model)

style_grams = {layer: gram_matrix(style_features[layer]) for layer in style_features}

target = content.clone().requires_grad_(True).to(config.DEVICE)
# target = torch.randn_like(content).requires_grad_(True).to(config.DEVICE)

style_weights = {'conv1_1': 1.,
                 'conv2_1': 0.75,
                 'conv3_1': 0.2,
                 'conv4_1': 0.2,
                 'conv5_1': 0.2}

content_weight = 1  # alpha
style_weight = 1e6  # beta

show_every = 10000

# iteration hyperparameters
optimizer = optim.Adam([target], lr=0.003)
steps = 20000  # decide how many iterations to update your image (5000)

for ii in range(1, steps+1):
    
    # get the features from your target image
    target_features = get_features(target, model)
    
    # the content loss
    content_loss = torch.mean((target_features['conv5_1'] - content_features['conv5_1'])**2)
    
    # the style loss
    # initialize the style loss to 0
    style_loss = 0
    # then add to it for each layer's gram matrix loss
    for layer in style_weights:
        # get the "target" style representation for the layer
        target_feature = target_features[layer]
        target_gram = gram_matrix(target_feature)
        _, d, h, w = target_feature.shape
        # get the "style" style representation
        style_gram = style_grams[layer]
        # the style loss for one layer, weighted appropriately
        layer_style_loss = style_weights[layer] * torch.mean((target_gram - style_gram)**2)
        # add to the style loss
        style_loss += layer_style_loss / (d * h * w)
        
    # calculate the *total* loss
    total_loss = content_weight * content_loss + style_weight * style_loss
    
    # update your target image
    optimizer.zero_grad()
    total_loss.backward()
    optimizer.step()
    
    # display intermediate images and print the loss
    if  ii % show_every == 0:
        print('Total loss: ', total_loss.item())
        plt.imshow(im_convert(target))
        plt.show()
        plt.pause(2)
        plt.close()



# from PIL import Image

# # Load the image
# contenu = Image.open('tesla.jpeg')
# style = Image.open('van_gogh.jpg')

# # Display the image using Matplotlib
# # plt.imshow(contenu)
# # plt.show()
# # plt.imshow(style)
# # plt.show()