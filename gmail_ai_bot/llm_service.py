import logging
from typing import Dict, List, Optional, Union, Any

# Import config
from .config import LLM_PROVIDER, LLM_CONFIG, LOG_LEVEL, LOG_FORMAT

# Set up logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class LLMService:
    """
    A service for interacting with various LLM providers.
    Supports Ollama, OpenAI, Google Gemini, and HuggingFace.
    """

    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the LLM service with the specified provider and model.

        Args:
            provider: The LLM provider to use. If None, uses the configured provider.
            model: The model to use. If None, uses the configured model for the provider.
        """
        self.provider = provider or LLM_PROVIDER
        self.config = LLM_CONFIG.get(self.provider, {})
        self.model = model or self.config.get('model')
        self.client = None
        
        logger.info(f"Initializing LLM service with provider: {self.provider}, model: {self.model}")
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate client based on the provider."""
        try:
            if self.provider == 'ollama':
                import ollama
                self.client = ollama
                logger.info("Initialized Ollama client")
                
            elif self.provider == 'openai':
                from openai import OpenAI
                api_key = self.config.get('api_key')
                if not api_key:
                    raise ValueError("OpenAI API key is required")
                self.client = OpenAI(api_key=api_key)
                logger.info("Initialized OpenAI client")
                
            elif self.provider == 'google':
                import google.generativeai as genai
                api_key = self.config.get('api_key')
                if not api_key:
                    raise ValueError("Google API key is required")
                genai.configure(api_key=api_key)
                self.client = genai
                logger.info("Initialized Google Gemini client")
                
            elif self.provider == 'huggingface':
                from huggingface_hub import InferenceClient
                api_key = self.config.get('api_key')
                provider = self.config.get('provider')
                self.client = InferenceClient(token=api_key)
                logger.info(f"Initialized HuggingFace client with provider: {provider}")
                
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}")
                
        except ImportError as e:
            logger.error(f"Error importing module for provider {self.provider}: {e}")
            raise ImportError(f"Please install the required package for {self.provider}. Error: {e}")
        except Exception as e:
            logger.error(f"Error initializing client for provider {self.provider}: {e}")
            raise

    def generate_text(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Generate text using the configured LLM provider.

        Args:
            prompt: The prompt to send to the LLM.
            max_tokens: Maximum number of tokens to generate.

        Returns:
            The generated text response.
        """
        try:
            logger.info(f"Generating text with provider: {self.provider}, model: {self.model}")
            
            if self.provider == 'ollama':
                response = self.client.generate(
                    model=self.model,
                    prompt=prompt,
                    options={"num_predict": max_tokens}
                )
                return response['response']
                
            elif self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
                
            elif self.provider == 'google':
                model = self.client.GenerativeModel(self.model)
                response = model.generate_content(prompt)
                return response.text
                
            elif self.provider == 'huggingface':
                try:
                    response = self.client.text_generation(
                        prompt,
                        model=self.model,
                        max_new_tokens=max_tokens,
                        # Remove provider parameter entirely as it's not supported by InferenceClient
                    )
                except ValueError as e:
                    # Handle provider-related errors that might come from a different client implementation
                    if "Provider 'nscale' not supported" in str(e):
                        logger.warning(f"Caught error about unsupported provider: {e}")
                        error_msg = (
                            "Unable to generate text due to a provider configuration issue. "
                            "The 'nscale' provider is not supported by HuggingFace. "
                            "Please check your HuggingFace configuration and ensure you're using "
                            "a supported provider. Valid providers include: 'auto', 'black-forest-labs', "
                            "'cerebras', 'cohere', 'fal-ai', 'fireworks-ai', 'hf-inference', 'hyperbolic', "
                            "'nebius', 'novita', 'openai', 'replicate', 'sambanova', 'together'."
                        )
                        logger.error(error_msg)
                        return error_msg
                    else:
                        raise
                except TypeError as e:
                    # Handle case where provider parameter is not accepted
                    if "unexpected keyword argument 'provider'" in str(e):
                        logger.warning("Provider parameter not supported by this client implementation")
                        # Retry without provider parameter
                        response = self.client.text_generation(
                            prompt,
                            model=self.model,
                            max_new_tokens=max_tokens
                        )
                    else:
                        raise
                return response

        except Exception as e:
            logger.error(f"Error generating text with {self.provider}: {str(e)}")
            # Fallback to a simpler response if the LLM fails
            return f"I apologize, but I'm unable to generate a response at this time due to a technical issue: {str(e)}"

    def get_available_models(self) -> List[str]:
        """
        Get a list of available models for the current provider.

        Returns:
            A list of available model names.
        """
        try:
            if self.provider == 'ollama':
                models = self.client.list()
                return [model['name'] for model in models['models']]

            elif self.provider == 'openai':
                models = self.client.models.list()
                return [model.id for model in models.data]

            elif self.provider == 'google':
                models = self.client.list_models()
                return [model.name for model in models]

            elif self.provider == 'huggingface':
                # HuggingFace doesn't have a simple API for listing models
                # Return the currently configured model
                return [self.model]

        except Exception as e:
            logger.error(f"Error getting available models for {self.provider}: {str(e)}")
            return []