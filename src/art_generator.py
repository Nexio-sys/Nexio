from PIL import Image
import numpy as np
from stable_diffusion_pytorch import StableDiffusion
import torch
import logging

class AIArtGenerator:
    def __init__(self, model_path, device=None):
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Setup device
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = device
            
        self.logger.info(f"Using device: {self.device}")
        
        try:
            self.model = StableDiffusion.from_pretrained(model_path)
            self.model.to(self.device)
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            raise
    
    def generate_art(self, prompt, style_params=None):
        """
        Generate art using Stable Diffusion
        
        Args:
            prompt (str): Text description of the desired image
            style_params (dict): Parameters for image generation
                height (int): Image height
                width (int): Image width
                num_inference_steps (int): Number of denoising steps
                guidance_scale (float): How closely to follow the prompt
                seed (int, optional): Random seed for reproducibility
                negative_prompt (str, optional): Things to avoid in the image
        """
        try:
            # Set default style parameters if none provided
            default_params = {
                'height': 512,
                'width': 512,
                'num_inference_steps': 50,
                'guidance_scale': 7.5,
                'negative_prompt': None,
                'seed': None
            }
            
            if style_params is None:
                style_params = default_params
            else:
                # Update defaults with provided parameters
                for key, value in default_params.items():
                    if key not in style_params:
                        style_params[key] = value
            
            # Set seed if provided
            if style_params['seed'] is not None:
                torch.manual_seed(style_params['seed'])
            
            self.logger.info(f"Generating image with prompt: {prompt}")
            self.logger.info(f"Style parameters: {style_params}")
            
            # Generate image using Stable Diffusion
            generation_params = {
                'prompt': prompt,
                'height': style_params['height'],
                'width': style_params['width'],
                'num_inference_steps': style_params['num_inference_steps'],
                'guidance_scale': style_params['guidance_scale']
            }
            
            if style_params['negative_prompt']:
                generation_params['negative_prompt'] = style_params['negative_prompt']
            
            image = self.model(**generation_params)
            
            self.logger.info("Image generation successful")
            return image
            
        except Exception as e:
            self.logger.error(f"Error generating art: {str(e)}")
            return None
    
    def save_image(self, image, path):
        """Save the generated image to a file"""
        try:
            if image is not None:
                image.save(path)
                self.logger.info(f"Image saved successfully to {path}")
                return True
            self.logger.warning("No image to save")
            return False
        except Exception as e:
            self.logger.error(f"Error saving image: {str(e)}")
            return False
    
    def generate_variations(self, prompt, num_variations=4, style_params=None):
        """Generate multiple variations of the same prompt"""
        images = []
        for i in range(num_variations):
            if style_params and 'seed' in style_params:
                # Increment seed for each variation
                style_params['seed'] += 1
            
            self.logger.info(f"Generating variation {i+1}/{num_variations}")
            image = self.generate_art(prompt, style_params)
            if image is not None:
                images.append(image)
        
        return images 