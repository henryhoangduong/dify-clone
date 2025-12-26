from llama_index import QueryKeywordExtractPrompt

CONVERSATION_TITLE_PROMPT = (
    "Human:{query}\n-----\n"
    "Help me summarize the intent of what the human said and provide a title, the title should not exceed 20 words.\n"
    "If the human said is conducted in Chinese, you should return a Chinese title.\n"
    "If the human said is conducted in English, you should return an English title.\n"
    "title:"
)


CONVERSATION_SUMMARY_PROMPT=()