#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const args = process.argv.slice(2);
const command = args[0];
const skillsRoot = path.join(__dirname, '..');

function getAvailableSkills() {
  return fs.readdirSync(skillsRoot).filter(name => {
    const skillPath = path.join(skillsRoot, name);
    return (
      fs.statSync(skillPath).isDirectory() &&
      fs.existsSync(path.join(skillPath, 'SKILL.md'))
    );
  });
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
    console.error(`Skill "${skillName}" not found. Run "skills list" to see available skills.`);
    process.exit(1);
  }
  const dest = path.join(targetDir, skillName);
  copyDir(src, dest);
  console.log(`✓ ${skillName} → ${dest}`);
}

const isGlobal = args.includes('--global');
const targetDir = isGlobal
  ? path.join(os.homedir(), '.claude', 'skills')
  : path.join(process.cwd(), '.claude', 'skills');

switch (command) {
  case 'list': {
    const skills = getAvailableSkills();
    console.log('Available skills:\n');
    skills.forEach(s => console.log(`  ${s}`));
    break;
  }

  case 'add': {
    const addAll = args.includes('--all');
    const skillName = args.find(a => !a.startsWith('--') && a !== 'add');

    if (addAll) {
      const skills = getAvailableSkills();
      skills.forEach(s => copySkill(s, targetDir));
      console.log(`\nInstalled ${skills.length} skills to ${targetDir}`);
    } else if (skillName) {
      copySkill(skillName, targetDir);
      console.log(`\nInstalled to ${targetDir}`);
    } else {
      console.error('Usage: skills add <skill-name> | skills add --all');
      process.exit(1);
    }
    break;
  }

  default:
    console.log(`
Usage:
  skills list                      List all available skills
  skills add <name>                Add a skill to .claude/skills/ in current project
  skills add --all                 Add all skills to current project
  skills add <name> --global       Add a skill to ~/.claude/skills/ (global)
  skills add --all --global        Add all skills globally
`);
}
