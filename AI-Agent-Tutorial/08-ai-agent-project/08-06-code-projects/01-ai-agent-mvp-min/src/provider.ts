import { createAnthropic } from '@ai-sdk/anthropic';
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';

export function createProvider() {
  const provider = process.env.AGENT_PROVIDER || 'anthropic';
  const apiKey = process.env.AGENT_API_KEY;

  if (!apiKey) {
    throw new Error(
      'AGENT_API_KEY 未设置。请复制 .env.example 为 .env 并填入 API Key。'
    );
  }

  switch (provider) {
    case 'anthropic':
      return createAnthropic({ apiKey });

    case 'qwen':
      return createOpenAICompatible({
        name: 'qwen',
        apiKey,
        baseURL:
          process.env.DASHSCOPE_BASE_URL ||
          'https://dashscope.aliyuncs.com/compatible-mode/v1',
      });

    case 'deepseek':
      return createOpenAICompatible({
        name: 'deepseek',
        apiKey,
        baseURL: 'https://api.deepseek.com/v1',
      });

    default:
      return createOpenAICompatible({
        name: provider,
        apiKey,
        baseURL: process.env.AGENT_BASE_URL || 'https://api.openai.com/v1',
      });
  }
}

export function getModelId(): string {
  return process.env.AGENT_MODEL || 'claude-sonnet-4-20250514';
}
