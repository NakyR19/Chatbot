class ModelConfig:

    def __init__(self, provider, model_name, temperature, max_tokens, modality):

        if provider is None:
            raise ValueError("provider cannot be None")
        self.provider = provider

        if model_name is None:
            raise ValueError("model_name cannot be None")
        self.model_name = model_name

        if temperature is None:
            raise ValueError("temperature cannot be None")
        self.temperature = float(temperature)

        if max_tokens is None:
            raise ValueError("max_tokens cannot be None")
        self.max_tokens = int(max_tokens)

        if modality is None:
            raise ValueError("modality cannot be None")
        self.modality = modality

    def __repr__(self):
        return (
            f"ModelConfig(provider={self.provider}, "
            f"model_name={self.model_name}, "
            f"temperature={self.temperature}, "
            f"max_tokens={self.max_tokens}, "
            f"modality={self.modality})"
        )