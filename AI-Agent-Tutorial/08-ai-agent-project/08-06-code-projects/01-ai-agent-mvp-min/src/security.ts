import * as readline from 'readline';
import chalk from 'chalk';

const BLOCKED_PATTERNS: Array<{ pattern: RegExp; reason: string }> = [
  { pattern: /rm\s+(-rf|-fr)\s+[\/~]/, reason: '禁止递归删除根目录或用户目录' },
  { pattern: />(>)?\s*\/etc\//, reason: '禁止写入系统配置目录' },
  { pattern: /\.env\b/, reason: '禁止涉及 .env 文件的操作' },
  { pattern: /DROP\s+(DATABASE|TABLE)/i, reason: '禁止删除数据库/表' },
];

export function checkSecurity(command: string): string | null {
  for (const { pattern, reason } of BLOCKED_PATTERNS) {
    if (pattern.test(command)) {
      return reason;
    }
  }
  return null;
}

export function confirmExecution(command: string): Promise<boolean> {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    const prompt = [
      '',
      chalk.yellow('  ┌─ 命令确认 ────────────────────────'),
      chalk.yellow(`  │ ${chalk.bold(command)}`),
      chalk.yellow('  └──────────────────────────────────'),
      chalk.yellow('  执行? (Y/n): '),
    ].join('\n');

    rl.question(prompt, (answer) => {
      rl.close();
      resolve(answer.trim().toLowerCase() !== 'n');
    });
  });
}
