"""
RADORDENA Connect Agent: VLM Inference Module.
Uses Qwen-VL-Chat-Int4 to analyze battery images on consumer hardware (RTX 4050).
"""
from transformers import AutoModelForCausalLM, AutoTokenizer

# GenerationConfig might be needed successfully for Qwen models
# from transformers.generation import GenerationConfig


def load_connect_agent():
    """
    Load the Quantized Qwen-VL-Chat-Int4 model onto the GPU.
    """
    print("Loading RADORDENA Connect (Qwen-VL-Int4)...")

    # Load quantized model to fit in RTX 4050 6GB
    # trust_remote_code=True is required for Qwen architecture
    tokenizer = AutoTokenizer.from_pretrained(
        "Qwen/Qwen-VL-Chat-Int4", trust_remote_code=True)

    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen-VL-Chat-Int4",
        device_map="cuda",      # Send to RTX 4050
        trust_remote_code=True,
        # 4050 supports Flash Attn 2 usually, but False is safer for setup compatibility
        use_flash_attn=False
    ).eval()

    return model, tokenizer


def analyze_battery_photo(model, tokenizer, image_path):
    """
    Generate an expert analysis of the battery image using the loaded VLM.
    """
    # The "System Prompt" for the Agent
    query = tokenizer.from_list_format([
        {'image': image_path},
        {'text': 'You are an expert Battery Recycler. '
                 'Identify the type of battery in this image. '
                 'Estimate its condition (swollen, rusted, good). '
                 'Is it safe for transport?'}
    ])

    inputs = tokenizer(query, return_tensors='pt')
    inputs = inputs.to(model.device)

    # Generate response
    pred = model.generate(**inputs, max_new_tokens=200)
    response = tokenizer.decode(pred.cpu()[0], skip_special_tokens=True)
    return response


if __name__ == '__main__':
    # Test Block (requires a real image file to work)
    print("Agent module loaded. Call load_connect_agent() to start.")
    # agent, tok = load_connect_agent()
    # RES = analyze_battery_photo(agent, tok, "test_battery.jpg")
    # print(RES)
