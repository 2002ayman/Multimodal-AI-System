import torch
from transformers import CLIPProcessor, CLIPModel
from transformers import BlipProcessor, BlipForConditionalGeneration

class MultimodalHandler:
    def __init__(self):
        # --- CLIP ---
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        # --- BLIP ---
        self.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")

    # --- BLIP Captioning ---
    def generate_caption(self, image):
        """توليد وصف نصي للصورة"""
        inputs = self.blip_processor(images=image, return_tensors="pt")
        out = self.blip_model.generate(**inputs)
        caption = self.blip_processor.decode(out[0], skip_special_tokens=True)
        return caption

    # --- CLIP Feature Extraction ---
    def extract_features(self, image):
        """تحويل الصورة إلى Feature Vector"""
        inputs = self.clip_processor(images=image, return_tensors="pt")
        with torch.no_grad():
            features = self.clip_model.get_image_features(**inputs)
        return features.numpy()

    def extract_text_features(self, text):
        inputs = self.clip_processor(text=[text], return_tensors="pt", padding=True)
        with torch.no_grad():
            features = self.clip_model.get_text_features(**inputs)
        return features.numpy()
