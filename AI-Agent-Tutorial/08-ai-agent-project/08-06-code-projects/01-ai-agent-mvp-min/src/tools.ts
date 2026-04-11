import { tool } from 'ai';
import { z } from 'zod';
import { readFile, writeFile, mkdir } from 'fs/promises';
import { existsSync } from 'fs';
import { exec } from 'child_process';
import { dirname, resolve } from 'path';
import { checkSecurity, confirmExecution } from './security.js';

function resolvePath(p: string): string {
  return resolve(process.cwd(), p);
}

export const agentTools = {
  read_file: tool({
    description: 'Read file content. ALWAYS read a file before modifying it.',
    parameters: z.object({
      path: z.string().describe('File path relative to working directory'),
    }),
    execute: async ({ path }) => {
      const absPath = resolvePath(path);
      if (!existsSync(absPath)) {
        return `[错误] 文件不存在: ${path}`;
      }
      try {
        const content = await readFile(absPath, 'utf-8');
        if (content.length > 10000) {
          return (
            content.slice(0, 10000) +
            `\n\n...[文件截断，总长 ${content.length} 字符]`
          );
        }
        return content;
      } catch (err: any) {
        return `[错误] 读取失败: ${err.message}`;
      }
    },
  }),

  write_file: tool({
    description:
      'Write content to a file. Creates parent directories automatically.',
    parameters: z.object({
      path: z.string().describe('File path relative to working directory'),
      content: z.string().describe('Complete file content to write'),
    }),
    execute: async ({ path, content }) => {
      const absPath = resolvePath(path);
      try {
        await mkdir(dirname(absPath), { recursive: true });
        await writeFile(absPath, content, 'utf-8');
        return `文件已写入: ${path} (${content.length} 字符)`;
      } catch (err: any) {
        return `[错误] 写入失败: ${err.message}`;
      }
    },
  }),

  run_command: tool({
    description:
      'Execute a shell command. Used for running tests, installing dependencies, git operations, etc. Requires user confirmation.',
    parameters: z.object({
      command: z.string().describe('Shell command to execute'),
    }),
    execute: async ({ command }) => {
      const violation = checkSecurity(command);
      if (violation) {
        return `[安全阻止] ${violation}`;
      }

      const confirmed = await confirmExecution(command);
      if (!confirmed) {
        return '[用户取消] 命令未执行';
      }

      return new Promise<string>((resolve) => {
        exec(
          command,
          {
            encoding: 'utf-8',
            timeout: 30_000,
            cwd: process.cwd(),
            maxBuffer: 1024 * 1024,
          },
          (error, stdout, stderr) => {
            if (error) {
              const msg = stderr || error.message;
              resolve(
                `[退出码 ${error.code ?? 1}]\n${msg}${stdout ? '\n--- stdout ---\n' + stdout : ''}`
              );
              return;
            }
            resolve(stdout || '(命令执行成功，无输出)');
          }
        );
      });
    },
  }),
};
