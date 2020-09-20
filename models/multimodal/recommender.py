import torch
import numpy as np
import pandas as pd
from vectorizer import CaptionVectorizer
from model import MultiModalModel

class ImageRecommender:
    def __init__(self, weights_path, embedding_path, hidden_size=1024):
        self.hidden_size = hidden_size
        self.vectorizer = CaptionVectorizer()
        self.vectorizer.load_embedding(embedding_path)

        self.model = MultiModalModel(self.vectorizer.embedding_size,
            hidden_size, bidirectional=True)
        self.model.load_state_dict(torch.load(weights_path))
        self.model.eval()

    def search_image(self, caption, images):
        embd_cap = self.vectorizer(caption).unsqueeze(1)
        cap_vec = self.model.forward_cap(embd_cap).squeeze(0)

        errors = torch.zeros(len(images))
        for i, image in enumerate(images):
            img_vec = self.model.forward_cnn(image.unsqueeze(0)).squeeze(0)
            diff = cap_vec - img_vec
            errors[i] = -torch.dot(diff, diff)

        return torch.argmin(errors).item()

def main():
    images = [torch.rand(3, 224, 224), torch.rand(3, 224,224), torch.rand(3, 224,244)]
    caption = "A man wearing a spiffing hat"

    recommender = ImageRecommender("bin/model_22.pth", "bin/embedding.pkl")
    idx = recommender.search_image(caption, images)
    print("Best image", idx)

if __name__ == "__main__":
    main()