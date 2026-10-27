// GOV-070: vitest prints only problem lines, `path:line:col: vitest <test> - <message>`,
// the same format ./scripts/problems prints for every check. Every vitest config
// uses this reporter, so `npm test` run anywhere shows these lines and nothing
// else; `no problems` when nothing failed.
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');

function relative(file) {
  return path.relative(ROOT, file).split(path.sep).join('/');
}

function firstLine(text) {
  return String(text ?? '').trim().split('\n')[0].trim();
}

function where(file, line, column) {
  if (!line) return file;
  return column ? `${file}:${line}:${column}` : `${file}:${line}`;
}

function describe(error) {
  if (!error) return 'failed';
  const message = firstLine(error.message);
  return error.name ? `${error.name}: ${message}` : message;
}

export default class ProblemsReporter {
  onTestRunEnd(testModules, unhandledErrors) {
    const lines = [];
    for (const module of testModules) {
      const file = module.moduleId;
      const moduleErrors = typeof module.errors === 'function' ? module.errors() : [];
      for (const error of moduleErrors) {
        lines.push(`${relative(file)}: vitest ${describe(error)}`);
      }
      for (const test of module.children.allTests('failed')) {
        const error = (test.result().errors ?? [])[0];
        // The failing line is the first stack frame in the test's own file.
        const frame = (error?.stacks ?? []).find((stack) => stack.file === file);
        const line = frame?.line ?? test.location?.line;
        const column = frame?.column ?? test.location?.column;
        lines.push(`${where(relative(file), line, column)}: vitest ${test.fullName} - ${describe(error)}`);
      }
    }
    for (const error of unhandledErrors ?? []) {
      lines.push(`frontend: vitest unhandled error - ${describe(error)}`);
    }
    const prefix = process.env.GITHUB_ACTIONS === 'true' ? '::error::' : '';
    process.stdout.write(lines.length ? `${lines.map((l) => prefix + l).join('\n')}\n` : 'no problems\n');
  }
}
