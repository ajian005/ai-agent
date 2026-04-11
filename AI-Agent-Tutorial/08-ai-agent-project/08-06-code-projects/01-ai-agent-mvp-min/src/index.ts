import 'dotenv/config';
import * as readline from 'readline';
import chalk from 'chalk';
import type { CoreMessage } from 'ai';
import { runAgent } from './agent.js';

function printBanner() {
  console.log();
  console.log(chalk.bold('  AI Agent MVP-MIN'));
  console.log(
    chalk.dim(
      `  Provider: ${process.env.AGENT_PROVIDER || 'anthropic'} | Model: ${process.env.AGENT_MODEL || 'claude-sonnet-4-20250514'}`
    )
  );
  console.log(chalk.dim('  命令: /exit 退出 | /clear 清空对话'));
  console.log();
}

async function main() {
  printBanner();

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  let history: CoreMessage[] = [];

  const askQuestion = () => {
    rl.question(chalk.blue('You: '), async (input) => {
      const trimmed = input.trim();

      if (!trimmed) {
        askQuestion();
        return;
      }

      if (trimmed === '/exit' || trimmed === '/quit') {
        console.log(chalk.dim('\n  再见！\n'));
        rl.close();
        process.exit(0);
      }

      if (trimmed === '/clear') {
        history = [];
        console.log(chalk.dim('  对话已清空\n'));
        askQuestion();
        return;
      }

      if (trimmed === '/help') {
        console.log(chalk.dim('  /exit   - 退出'));
        console.log(chalk.dim('  /clear  - 清空对话历史'));
        console.log(chalk.dim('  /help   - 显示帮助\n'));
        askQuestion();
        return;
      }

      try {
        history = await runAgent(trimmed, history);
      } catch (err: any) {
        console.error(chalk.red(`\n  错误: ${err.message}`));
        if (err.cause) {
          console.error(chalk.dim(`  原因: ${err.cause}`));
        }
        console.log();
      }

      askQuestion();
    });
  };

  askQuestion();
}

main().catch((err) => {
  console.error(chalk.red(`启动失败: ${err.message}`));
  process.exit(1);
});
