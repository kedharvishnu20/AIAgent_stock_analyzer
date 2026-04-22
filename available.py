import os
from google import genai


api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key)

# List all models
target_models = []
for model in client.models.list():
    target_models.append(model.name)
    print(f"Model ID: {model.name}")
    # The SDK update changed this to supported_actions
    print(f"Capabilities: {model.supported_actions}")
    print("-" * 20)





print(f"{'Model Name':<35} | {'Input Limit':<12} | {'Output Limit'}")
print("-" * 65)

for model_id in target_models:
    try:
        # Fetch model metadata
        model_info = client.models.get(model=model_id)
        
        print(f"{model_info.name:<35} | "
              f"{model_info.input_token_limit:<12} | "
              f"{model_info.output_token_limit}")
    except Exception as e:
        print(f"Could not retrieve {model_id}: {e}")

print("\nNote: For RPM/RPD (Requests Per Day), refer to your AI Studio Dashboard:")
print("https://aistudio.google.com/rate-limit")