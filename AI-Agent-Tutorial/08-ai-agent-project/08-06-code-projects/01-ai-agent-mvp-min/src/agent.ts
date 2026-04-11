import { streamText, type CoreMessage } from 'ai';
import chalk from 'chalk';
import { createProvider, getModelId } from './provider.js';
import { agentTools } from './tools.js';
import { buildSystemPrompt } from './prompt.js';

const MAX_STEPS = 20;
const MAX_MESSAGES = 30;

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

  const result = streamText({
    model,
    system: buildSystemPrompt(),
    messages: history,
    tools: agentTools,
    maxSteps: MAX_STEPS,
    onStepFinish: ({ stepType, toolCalls, toolResults }) => {
      if (stepType === 'tool-result' && toolCalls) {
        for (const tc of toolCalls) {
          console.log(chalk.cyan(`\n  [工具调用] ${tc.toolName}`));

          if (tc.args && typeof tc.args === 'object') {
            const argsStr = JSON.stringify(tc.args, null, 2)
              .split('\n')
              .map((l) => `    ${l}`)
              .join('\n');
            console.log(chalk.dim(argsStr));
          }

          const tr = toolResults?.find(
            (r) => r.toolCallId === tc.toolCallId
          );
          if (tr) {
            const output = String(tr.result);
            const lines = output.split('\n');
            const truncated =
              lines.length > 20
                ? lines.slice(0, 20).join('\n') +
                  `\n  ...(${lines.length} 行，已截断显示)`
                : output;
            console.log(
              chalk.dim(
                `  ─── 结果 ───\n  ${truncated.split('\n').join('\n  ')}`
              )
            );
          }
        }
      }
    },
  });

  let fullResponse = '';
  process.stdout.write(chalk.green('\nAgent: '));

  for await (const chunk of result.textStream) {
    process.stdout.write(chunk);
    fullResponse += chunk;
  }
  console.log('\n');

  if (fullResponse) {
    history.push({ role: 'assistant', content: fullResponse });
  }

  return history;
}
