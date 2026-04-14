import type { CoreMessage } from 'ai';
import type {
  JSONSchema7,
  LanguageModelV1FunctionTool,
  LanguageModelV1Prompt,
} from '@ai-sdk/provider';
import chalk from 'chalk';
import { createProvider, getModelId } from './provider.js';
import { agentTools } from './tools.js';
import { buildSystemPrompt } from './prompt.js';

const MAX_STEPS = 20;
const MAX_MESSAGES = 30;

const languageModelTools: LanguageModelV1FunctionTool[] = [
  {
    type: 'function',
    name: 'read_file',
    description:
      'Read file content. ALWAYS read a file before modifying it.',
    parameters: {
      type: 'object',
      properties: {
        path: {
          type: 'string',
          description: 'File path relative to working directory',
        },
      },
      required: ['path'],
    } as JSONSchema7,
  },
  {
    type: 'function',
    name: 'write_file',
    description:
      'Write content to a file. Creates parent directories automatically.',
    parameters: {
      type: 'object',
      properties: {
        path: {
          type: 'string',
          description: 'File path relative to working directory',
        },
        content: {
          type: 'string',
          description: 'Complete file content to write',
        },
      },
      required: ['path', 'content'],
    } as JSONSchema7,
  },
  {
    type: 'function',
    name: 'run_command',
    description:
      'Execute a shell command. Used for running tests, installing dependencies, git operations, etc. Requires user confirmation.',
    parameters: {
      type: 'object',
      properties: {
        command: {
          type: 'string',
          description: 'Shell command to execute',
        },
      },
      required: ['command'],
    } as JSONSchema7,
  },
];

function coreMessagesToLanguageModelPrompt(
  system: string,
  messages: CoreMessage[]
): LanguageModelV1Prompt {
  const out: LanguageModelV1Prompt = [{ role: 'system', content: system }];

  for (const m of messages) {
    if (m.role === 'system') {
      continue;
    }
    if (m.role === 'user') {
      if (typeof m.content === 'string') {
        out.push({
          role: 'user',
          content: [{ type: 'text', text: m.content }],
        });
      } else {
        const parts = m.content
          .filter((p): p is { type: 'text'; text: string } => p.type === 'text')
          .map((p) => ({ type: 'text' as const, text: p.text }));
        if (parts.length === 0) {
          out.push({ role: 'user', content: [{ type: 'text', text: '' }] });
        } else {
          out.push({ role: 'user', content: parts });
        }
      }
      continue;
    }
    if (m.role === 'assistant') {
      if (typeof m.content === 'string') {
        out.push({
          role: 'assistant',
          content: [{ type: 'text', text: m.content }],
        });
      } else {
        out.push({
          role: 'assistant',
          content: m.content.map((p) => {
            if (p.type === 'text') {
              return { type: 'text' as const, text: p.text };
            }
            if (p.type === 'tool-call') {
              return {
                type: 'tool-call' as const,
                toolCallId: p.toolCallId,
                toolName: p.toolName,
                args: p.args,
              };
            }
            if (p.type === 'reasoning') {
              return {
                type: 'reasoning' as const,
                text: p.text,
                signature: p.signature,
              };
            }
            if (p.type === 'redacted-reasoning') {
              return { type: 'redacted-reasoning' as const, data: p.data };
            }
            return {
              type: 'file' as const,
              data: p.data as string,
              mimeType: p.mimeType,
              filename: p.filename,
            };
          }),
        });
      }
      continue;
    }
    if (m.role === 'tool') {
      out.push({
        role: 'tool',
        content: m.content.map((p) => ({
          type: 'tool-result' as const,
          toolCallId: p.toolCallId,
          toolName: p.toolName,
          result: p.result,
          isError: p.isError,
        })),
      });
    }
  }

  return out;
}

function logToolStep(
  toolCalls: Array<{
    toolCallId: string;
    toolName: string;
    args: string;
  }>,
  toolResults: Array<{ toolCallId: string; result: unknown }>
): void {
  for (const tc of toolCalls) {
    console.log(chalk.cyan(`\n  [工具调用] ${tc.toolName}`));

    let parsedArgs: unknown;
    try {
      parsedArgs = JSON.parse(tc.args) as unknown;
    } catch {
      parsedArgs = tc.args;
    }
    if (parsedArgs && typeof parsedArgs === 'object') {
      const argsStr = JSON.stringify(parsedArgs, null, 2)
        .split('\n')
        .map((l) => `    ${l}`)
        .join('\n');
      console.log(chalk.dim(argsStr));
    }

    const tr = toolResults.find((r) => r.toolCallId === tc.toolCallId);
    if (tr) {
      const output = String(tr.result);
      const lines = output.split('\n');
      const truncated =
        lines.length > 20
          ? lines.slice(0, 20).join('\n') +
            `\n  ...(${lines.length} 行，已截断显示)`
          : output;
      console.log(
        chalk.dim(`  ─── 结果 ───\n  ${truncated.split('\n').join('\n  ')}`)
      );
    }
  }
}

export async function runAgent(
  userMessage: string,
  history: CoreMessage[]
): Promise<CoreMessage[]> {
  const provider = createProvider();
  const modelId = getModelId();
  const model = provider(modelId);

  history.push({ role: 'user', content: userMessage });

  if (history.length > MAX_MESSAGES) {
    history.splice(0, history.length - MAX_MESSAGES);
  }

  const systemPrompt = buildSystemPrompt();
  const apiMessages: CoreMessage[] = [...history];

  let fullResponse = '';
  let step = 0;

  process.stdout.write(chalk.green('\nAgent: '));

  while (step < MAX_STEPS) {
    step += 1;

    const prompt = coreMessagesToLanguageModelPrompt(systemPrompt, apiMessages);

    const result = await model.doGenerate({
      inputFormat: 'messages',
      mode: {
        type: 'regular',
        tools: languageModelTools,
        toolChoice: { type: 'auto' },
      },
      prompt,
    });

    if (result.text) {
      fullResponse += result.text;
      process.stdout.write(result.text);
    }

    const calls = result.toolCalls;
    const hasToolCalls = calls !== undefined && calls.length > 0;

    if (hasToolCalls) {
      const content: Array<
        | { type: 'text'; text: string }
        | {
            type: 'tool-call';
            toolCallId: string;
            toolName: string;
            args: unknown;
          }
      > = [];

      if (result.text) {
        content.push({ type: 'text', text: result.text });
      }
      for (const tc of calls) {
        let args: unknown;
        try {
          args = JSON.parse(tc.args) as unknown;
        } catch {
          args = tc.args;
        }
        content.push({
          type: 'tool-call',
          toolCallId: tc.toolCallId,
          toolName: tc.toolName,
          args,
        });
      }

      apiMessages.push({ role: 'assistant', content });

      const toolResults: Array<{ toolCallId: string; result: unknown }> = [];

      for (const tc of calls) {
        const name = tc.toolName as keyof typeof agentTools;
        const toolDef = agentTools[name];
        if (!toolDef?.execute) {
          toolResults.push({
            toolCallId: tc.toolCallId,
            result: `[错误] 未知工具: ${tc.toolName}`,
          });
          continue;
        }

        let parsed: unknown;
        try {
          parsed = JSON.parse(tc.args) as unknown;
        } catch {
          toolResults.push({
            toolCallId: tc.toolCallId,
            result: '[错误] 工具参数不是合法 JSON',
          });
          continue;
        }

        let execResult: unknown;
        try {
          const validated = toolDef.parameters.parse(parsed) as Record<
            string,
            unknown
          >;
          execResult = await toolDef.execute(validated as never, {
            toolCallId: tc.toolCallId,
            messages: apiMessages
              .slice(0, -1)
              .filter((m) => m.role !== 'system'),
          });
        } catch (err: unknown) {
          execResult = `[错误] ${err instanceof Error ? err.message : String(err)}`;
        }
        toolResults.push({ toolCallId: tc.toolCallId, result: execResult });
      }

      logToolStep(calls, toolResults);

      apiMessages.push({
        role: 'tool',
        content: calls.map((tc) => {
          const tr = toolResults.find((r) => r.toolCallId === tc.toolCallId);
          return {
            type: 'tool-result' as const,
            toolCallId: tc.toolCallId,
            toolName: tc.toolName,
            result:
              tr !== undefined
                ? tr.result
                : '[错误] 工具结果缺失（toolCallId 不匹配）',
          };
        }),
      });

      continue;
    }

    break;
  }

  console.log('\n');

  if (fullResponse) {
    history.push({ role: 'assistant', content: fullResponse });
  }

  return history;
}
