import base64
from abc import ABC, abstractmethod
from typing import Optional

from core import hosted_llm_credentials
from core.llm.error import (ModelCurrentlyNotSupportError,
                            ProviderTokenNotInitError, QuotaExceededError)
from extensions.ext_database import db
from models.account import Tenant
from models.provider import Provider, ProviderName, ProviderType


class BaseProvider(ABC):
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id

    def get_provider_api_key(self, model_id: Optional[str] = None, prefer_custom: bool = True) -> str:
        provider = self.get_provider(prefer_custom)
        if not provider:
            raise ProviderTokenNotInitError()
        
        if provider.provider_type == ProviderType.SYSTEM.value:
            quota_used = provider.quota_used if provider.quota_used is not None else 0
            quota_limit = provider.quota_limit if provider.quota_limit is not None else 0

            if model_id and model_id == 'gpt-4':
                raise ModelCurrentlyNotSupportError()

            if quota_used >= quota_limit:
                raise QuotaExceededError()

            return self.get_hosted_credentials()
        else:
            return self.get_decrypted_token(provider.encrypted_config)

    def get_provider(self, prefer_custom: bool) -> Optional[Provider]:
        providers = db.session.query(Provider).filter(
            Provider.tenant_id == self.tenant_id,
            Provider.provider_name == self.get_provider_name().value
        ).order_by(Provider.provider_type.desc() if prefer_custom else Provider.provider_type).all()

        custom_provider = None
        system_provider = None

        for provider in providers:
            if provider.provider_type == ProviderType.CUSTOM.value:
                custom_provider = provider
            elif provider.provider_type == ProviderType.SYSTEM.value:
                system_provider = provider

        if custom_provider and custom_provider.is_valid and custom_provider.encrypted_config:
            return custom_provider
        elif system_provider and system_provider.is_valid:
            return system_provider
        else:
            return None

    def get_hosted_credentials(self) -> str:
        if self.get_provider_name() != ProviderName.OPENAI:
            raise ProviderTokenNotInitError()

        if not hosted_llm_credentials.openai or not hosted_llm_credentials.openai.api_key:
            raise ProviderTokenNotInitError()

        return hosted_llm_credentials.openai.api_key

    @abstractmethod
    def get_provider_name(self):
        raise NotImplementedError

    @abstractmethod
    def get_credentials(self, model_id: Optional[str] = None) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_models(self, model_id: Optional[str] = None) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    def config_validate(self, config: str):
        raise NotImplementedError
