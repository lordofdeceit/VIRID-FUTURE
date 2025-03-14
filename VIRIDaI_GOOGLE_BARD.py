from dataset import to_device, get_device, get_image
from model import get_model
import torch
import config

# Set up Google Bard API credentials
bard_api_key = "[SECRET-API-KEY]"

# function to call Google Bard API and get insights and recommendations
def get_insights(land_type):
    prompt = f"What are the best practices for optimizing yield in {land_type} land type ?"
    response = bard.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.8,
    )
    recommendation = response.choices[0].text.strip()
    return recommendation


def decode_target(target, text_labels=False):
    """Decode target labels into text (or not)"""
    if not text_labels:
        return target
    else:
        return config.IDX_CLASS_LABELS[target]


def predict_single(image):
    device = get_device()
    xb = image.unsqueeze(0)
    xb = to_device(xb, device)
    with torch.no_grad():
        preds = model(xb)
    _, prediction = torch.max(preds.cpu().detach(), dim=1)
    
    # Get insights and recommendations using Google Bard API
    land_type = decode_target(int(prediction), text_labels=True)
    insights = get_insights(land_type)
    
    return land_type, insights


if __name__ == "__main__":
    image = get_image(config.PATH)
    land_type, insights = predict_single(image)
    print(f"Predicted land type: {land_type}")
    print(f"Insights and recommendations: {insights}")
else:
    print("Sorry no insights for this landtype")
