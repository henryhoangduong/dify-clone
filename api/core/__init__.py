from typing import Optional

from pydantic import BaseModel


class HostedOpenAICredential(BaseModel):
    api_key: str


class HostedLLMCredentials(BaseModel):
    openai: Optional[HostedOpenAICredential] = None


hosted_llm_credentials = HostedLLMCredentials()
