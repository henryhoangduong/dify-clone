from typing import Optional, Union

from langchain.callbacks import CallbackManager
from langchain.llms.fake import FakeListLLM

from core.constant import llm_constant
from core.llm.streamable_open_ai import StreamableOpenAI
from core.llm.streamable_chat_open_ai import StreamableChatOpenAI
from core.llm.provider.llm_provider_service import LLMProviderService


class LLMBuilder:
    @classmethod
    def to_llm(cls, tenant_id: str, model_name: str, **kwargs) -> Union[StreamableOpenAI, StreamableChatOpenAI, FakeListLLM]:
        if model_name == 'fake':
            return FakeListLLM(responses=[])

        mode = cls.get_mode_by_model(model_name)
        if mode == 'chat':
            # llm_cls = StreamableAzureChatOpenAI
            llm_cls = StreamableChatOpenAI
        elif mode == 'completion':
            llm_cls = StreamableOpenAI
        else:
            raise ValueError(f"model name {model_name} is not supported.")

        model_credentials = cls.get_model_credentials(tenant_id, model_name)

        return llm_cls(
            model_name=model_name,
            temperature=kwargs.get('temperature', 0),
            max_tokens=kwargs.get('max_tokens', 256),
            top_p=kwargs.get('top_p', 1),
            frequency_penalty=kwargs.get('frequency_penalty', 0),
            presence_penalty=kwargs.get('presence_penalty', 0),
            callback_manager=kwargs.get('callback_manager', None),
            streaming=kwargs.get('streaming', False),
            # request_timeout=None
            **model_credentials
        )

    @classmethod
    def to_llm_from_model(cls, tenant_id: str, model: dict, streaming: bool = False,
                          callback_manager: Optional[CallbackManager] = None) -> Union[StreamableOpenAI, StreamableChatOpenAI]:
        model_name = model.get("name")
        completion_params = model.get("completion_params", {})

        return cls.to_llm(
            tenant_id=tenant_id,
            model_name=model_name,
            temperature=completion_params.get('temperature', 0),
            max_tokens=completion_params.get('max_tokens', 256),
            top_p=completion_params.get('top_p', 0),
            frequency_penalty=completion_params.get('frequency_penalty', 0.1),
            presence_penalty=completion_params.get('presence_penalty', 0.1),
            streaming=streaming,
            callback_manager=callback_manager
        )

    @classmethod
    def get_mode_by_model(cls, model_name: str) -> str:
        if not model_name:
            raise ValueError(f"empty model name is not supported.")

        if model_name in llm_constant.models_by_mode['chat']:
            return "chat"
        elif model_name in llm_constant.models_by_mode['completion']:
            return "completion"
        else:
            raise ValueError(f"model name {model_name} is not supported.")

    @classmethod
    def get_model_credentials(cls, tenant_id: str, model_name: str) -> dict:
        """
        Returns the API credentials for the given tenant_id and model_name, based on the model's provider.
        Raises an exception if the model_name is not found or if the provider is not found.
        """
        if not model_name:
            raise Exception('model name not found')

        if model_name not in llm_constant.models:
            raise Exception('model {} not found'.format(model_name))

        model_provider = llm_constant.models[model_name]

        provider_service = LLMProviderService(
            tenant_id=tenant_id, provider_name=model_provider)
        return provider_service.get_credentials(model_name)
