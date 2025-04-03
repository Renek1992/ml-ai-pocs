from transformers import AutoConfig

def estimate_model_memory(model_name: str) -> int:
    config = AutoConfig.from_pretrained(pretrained_model_name_or_path=model_name)

    # Extract relevant configuration details
    hidden_size = config.hidden_size
    num_hidden_layers = config.num_hidden_layers
    vocab_size = config.vocab_size

    # Estimate the size of the model parameters
    # For a transformer model, main parameters include:
    # - Embedding layer: vocab_size * hidden_size
    # - Transformer layers: 12 * hidden_size^2 (approximate for each transformer layer)
    # - Layer normalization, biases, and other small parameters are ignored for simplicity

    embedding_params = vocab_size * hidden_size
    transformer_params = num_hidden_layers * (12 * hidden_size ** 2)

    # Total number of parameters
    total_params = embedding_params + transformer_params
    param_size = total_params * 4  # Assuming each parameter is a 32-bit float, which is 4 bytes

    # Convert bytes to gigabytes
    param_size_gb = param_size / (1024 ** 3)

    # Return the estimated size in GB
    return param_size_gb