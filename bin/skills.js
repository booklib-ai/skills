#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const args = process.argv.slice(2);
const command = args[0];
const skillsRoot = path.join(__dirname, '..');

// ANSI color helpers
const c = {
  bold: s => `\x1b[1m${s}\x1b[0m`,
  dim: s => `\x1b[2m${s}\x1b[0m`,
  green: s => `\x1b[32m${s}\x1b[0m`,
  cyan: s => `\x1b[36m${s}\x1b[0m`,
  yellow: s => `\x1b[33m${s}\x1b[0m`,
  red: s => `\x1b[31m${s}\x1b[0m`,
  blue: s => `\x1b[34m${s}\x1b[0m`,
  line: (len = 60) => c.dim('─'.repeat(len)),
};

function parseSkillFrontmatter(skillName) {
  const skillMdPath = path.join(skillsRoot, skillName, 'SKILL.md');
  try {
    const content = fs.readFileSync(skillMdPath, 'utf8');
    const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (!fmMatch) return { name: skillName, description: '' };

    const fm = fmMatch[1];

    // Handle block scalar (description: >\n  line1\n  line2)
    const blockMatch = fm.match(/^description:\s*>\s*\n((?:[ \t]+.+\n?)+)/m);
    // Handle quoted string
    const quotedMatch = fm.match(/^description:\s*["'](.+?)["']\s*$/m);
    // Handle plain single-line
    const plainMatch = fm.match(/^description:\s*(?!>)(.+)$/m);

    let description = '';
    if (blockMatch) {
      description = blockMatch[1]
        .split('\n')
        .map(l => l.trim())
        .filter(Boolean)
        .join(' ');
    } else if (quotedMatch) {
      description = quotedMatch[1];
    } else if (plainMatch) {
      description = plainMatch[1].trim();
    }

    return { name: skillName, description };
  } catch {
    return { name: skillName, description: '' };
  }
}

function getAvailableSkills() {
  return fs.readdirSync(skillsRoot)
    .filter(name => {
      const skillPath = path.join(skillsRoot, name);
      return (
        fs.statSync(skillPath).isDirectory() &&
        fs.existsSync(path.join(skillPath, 'SKILL.md'))
      );
    })
    .sort();
}

function firstSentence(text, maxLen = 65) {
  const end = text.search(/[.!?](\s|$)/);
  const sentence = end >= 0 ? text.slice(0, end + 1) : text;
  return sentence.length <= maxLen ? sentence : sentence.slice(0, maxLen - 1) + '…';
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src)) {
    const srcPath = path.join(src, entry);
    const destPath = path.join(dest, entry);
    if (fs.statSync(srcPath).isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function copySkill(skillName, targetDir) {
  const src = path.join(skillsRoot, skillName);
  if (!fs.existsSync(src)) {
    console.error(c.red(`✗ Skill "${skillName}" not found.`) + ' Run ' + c.cyan('skills list') + ' to see available skills.');
    process.exit(1);
  }
  const dest = path.join(targetDir, skillName);
  copyDir(src, dest);
  console.log(c.green('✓') + ` ${c.bold(skillName)} → ${c.dim(dest)}`);
}

const isGlobal = args.includes('--global');
const targetDir = isGlobal
  ? path.join(os.homedir(), '.claude', 'skills')
  : path.join(process.cwd(), '.claude', 'skills');

switch (command) {
  case 'list': {
    const skills = getAvailableSkills();
    const nameWidth = Math.max(...skills.map(s => s.length)) + 2;
    console.log('');
    console.log(c.bold(`  Skills`) + c.dim(` (${skills.length} available)`));
    console.log('  ' + c.line(nameWidth + 67));
    for (const s of skills) {
      const { description } = parseSkillFrontmatter(s);
      const summary = description ? firstSentence(description) : '';
      console.log(`  ${c.cyan(s.padEnd(nameWidth))}${c.dim(summary)}`);
    }
    console.log('  ' + c.line(nameWidth + 67));
    console.log(c.dim(`\n  npx @booklib/skills add <name>      install to .claude/skills/`));
    console.log(c.dim(`  npx @booklib/skills info <name>     full description`));
    console.log(c.dim(`  npx @booklib/skills demo <name>     before/after example\n`));
    break;
  }

  case 'info': {
    const skillName = args.find(a => !a.startsWith('--') && a !== 'info');
    if (!skillName) {
      console.error(c.red('Usage: skills info <skill-name>'));
      process.exit(1);
    }
    const skills = getAvailableSkills();
    if (!skills.includes(skillName)) {
      console.error(c.red(`✗ Skill "${skillName}" not found.`) + ' Run ' + c.cyan('skills list') + ' to see available skills.');
      process.exit(1);
    }
    const { description } = parseSkillFrontmatter(skillName);
    const skillMdPath = path.join(skillsRoot, skillName, 'SKILL.md');
    const hasEvals = fs.existsSync(path.join(skillsRoot, skillName, 'evals'));
    const hasExamples = fs.existsSync(path.join(skillsRoot, skillName, 'examples'));
    const hasRefs = fs.existsSync(path.join(skillsRoot, skillName, 'references'));

    // Count lines in SKILL.md as a proxy for depth
    const lines = fs.readFileSync(skillMdPath, 'utf8').split('\n').length;

    console.log('');
    console.log(c.bold(`  ${skillName}`));
    console.log('  ' + c.line(60));

    // Word-wrap description at ~72 chars
    const words = description.split(' ');
    let line = '  ';
    for (const word of words) {
      if (line.length + word.length > 74) {
        console.log(line);
        line = '  ' + word + ' ';
      } else {
        line += word + ' ';
      }
    }
    if (line.trim()) console.log(line);

    console.log('');
    console.log(c.dim(`  Includes: `) +
      [
        hasEvals ? c.green('evals') : null,
        hasExamples ? c.green('examples') : null,
        hasRefs ? c.green('references') : null,
        `${lines} lines`,
      ].filter(Boolean).join(c.dim(' · ')));
    console.log('');
    console.log(`  ${c.cyan('Install:')} npx @booklib/skills add ${skillName}`);
    if (hasExamples) {
      console.log(`  ${c.cyan('Demo:')}    npx @booklib/skills demo ${skillName}`);
    }
    console.log('');
    break;
  }

  case 'demo': {
    const skillName = args.find(a => !a.startsWith('--') && a !== 'demo');
    if (!skillName) {
      console.error(c.red('Usage: skills demo <skill-name>'));
      process.exit(1);
    }
    const skills = getAvailableSkills();
    if (!skills.includes(skillName)) {
      console.error(c.red(`✗ Skill "${skillName}" not found.`) + ' Run ' + c.cyan('skills list') + ' to see available skills.');
      process.exit(1);
    }

    const beforePath = path.join(skillsRoot, skillName, 'examples', 'before.md');
    const afterPath = path.join(skillsRoot, skillName, 'examples', 'after.md');

    if (!fs.existsSync(beforePath) || !fs.existsSync(afterPath)) {
      console.log(c.yellow(`  No demo available for "${skillName}" yet.`));
      console.log(c.dim(`  Try: npx @booklib/skills info ${skillName}\n`));
      process.exit(0);
    }

    const before = fs.readFileSync(beforePath, 'utf8').trim();
    const after = fs.readFileSync(afterPath, 'utf8').trim();

    console.log('');
    console.log(c.bold(`  ${skillName}`) + c.dim(' — before/after example'));
    console.log('  ' + c.line(60));
    console.log('');
    console.log(c.bold(c.yellow('  BEFORE')));
    console.log('');
    before.split('\n').forEach(l => console.log('  ' + l));
    console.log('');
    console.log(c.bold(c.green('  AFTER')));
    console.log('');
    after.split('\n').forEach(l => console.log('  ' + l));
    console.log('');
    console.log(c.dim(`  Install: npx @booklib/skills add ${skillName}\n`));
    break;
  }

  case 'add': {
    const addAll = args.includes('--all');
    const skillName = args.find(a => !a.startsWith('--') && a !== 'add');

    if (addAll) {
      const skills = getAvailableSkills();
      skills.forEach(s => copySkill(s, targetDir));
      console.log(c.dim(`\nInstalled ${skills.length} skills to ${targetDir}`));
    } else if (skillName) {
      copySkill(skillName, targetDir);
      console.log(c.dim(`\nInstalled to ${targetDir}`));
    } else {
      console.error(c.red('Usage: skills add <skill-name> | skills add --all'));
      process.exit(1);
    }
    break;
  }

  default:
    console.log(`
${c.bold('  @booklib/skills')} — book knowledge distilled into AI agent skills

${c.bold('  Usage:')}
    ${c.cyan('skills list')}                       list all available skills
    ${c.cyan('skills info')} ${c.dim('<name>')}                full description of a skill
    ${c.cyan('skills demo')} ${c.dim('<name>')}                before/after example
    ${c.cyan('skills add')}  ${c.dim('<name>')}                install to .claude/skills/
    ${c.cyan('skills add --all')}                  install all skills
    ${c.cyan('skills add')}  ${c.dim('<name> --global')}       install to ~/.claude/skills/
`);
}
