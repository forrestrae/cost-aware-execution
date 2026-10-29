"""Offline packaging checks. These do not validate agent runtime behavior."""
import json
import os
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'
SKILL_DIR = SKILLS / 'cost-aware-execution'
SKILL = SKILL_DIR / 'SKILL.md'
SPEC_KEYS = {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'}
NAME_RE = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
PLATFORMS = {'any', 'claude-code', 'codex', 'cursor', 'github-copilot', 'opencode', 'gemini-cli'}
HOST_ONLY_TOKENS = ['ExitPlanMode', 'CLAUDE_CODE_', 'code.claude.com', '/workflow-authoring',
                    'Dynamic Workflow', 'ANTHROPIC_MODEL', 'opusplan', 'claude --',
                    'Haiku', 'Sonnet', 'Opus', 'config.toml', 'opencode.json']
SKIP_DIRS = {'.git', '.venv', '.idea', 'node_modules', '__pycache__'}
RESULTS = ROOT / 'development' / 'results'  # gitignored run records, never published
LINK_RE = r'\[[^\]]*\]\(([^)]+)\)'


def walk(suffix=None):
    """Yield files under ROOT, skipping tooling directories and unpublished run records."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS and Path(dirpath) / d != RESULTS]
        for name in filenames:
            path = Path(dirpath) / name
            if suffix is None or path.suffix == suffix:
                yield path


def frontmatter(text):
    match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    return yaml.safe_load(match.group(1)) if match else None


class PackageTests(unittest.TestCase):
    def required(self, path):
        self.assertTrue(path.is_file(), f'Missing file: {path.relative_to(ROOT)}')
        return path.read_text(encoding='utf-8')

    def test_discovery_layout_exposes_exactly_one_skill(self):
        files = list(SKILLS.glob('*/SKILL.md'))
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].parent.name, 'cost-aware-execution')
        self.assertFalse((ROOT / 'SKILL.md').exists())
        self.assertFalse((ROOT / 'skills.sh.json').exists())
        for dirpath, dirnames, _ in os.walk(ROOT):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            here = Path(dirpath)
            for name in dirnames:
                rel = (here / name).relative_to(ROOT).as_posix()
                self.assertNotIn(name, {'.claude-plugin', 'plugins', '.agents'}, rel)
                self.assertNotEqual(rel, '.claude/skills')

    def test_skill_frontmatter_conforms_to_agent_skills_spec(self):
        data = frontmatter(self.required(SKILL))
        self.assertIsInstance(data, dict)
        self.assertLessEqual(set(data), SPEC_KEYS)
        self.assertRegex(data['name'], NAME_RE)
        self.assertTrue(1 <= len(data['name']) <= 64)
        self.assertEqual(data['name'], SKILL_DIR.name)
        self.assertTrue(1 <= len(data['description'].strip()) <= 1024)
        if 'license' in data:
            self.assertIsInstance(data['license'], str)
            self.assertTrue(data['license'].strip())
        if 'compatibility' in data:
            self.assertTrue(1 <= len(data['compatibility']) <= 500)
        if 'metadata' in data:
            for key, value in data['metadata'].items():
                self.assertIsInstance(key, str)
                self.assertIsInstance(value, str)
        self.assertRegex(data['metadata']['version'], r'^\d+\.\d+\.\d+$')

    def test_skill_size_within_spec_recommendation(self):
        lines = self.required(SKILL).splitlines()
        self.assertLessEqual(len(lines), 500)

    def test_skill_directory_is_instruction_only(self):
        for path in SKILL_DIR.rglob('*'):
            self.assertFalse(path.is_symlink(), str(path))
            if path.is_file():
                self.assertIn(path.suffix, {'.md', '.json'})

    def test_skill_links_resolve_inside_skill_directory(self):
        files = list(SKILL_DIR.rglob('*.md'))
        self.assertTrue(files)
        for path in files:
            for link in re.findall(LINK_RE, path.read_text(encoding='utf-8')):
                if '://' in link or link.startswith('#'):
                    continue
                resolved = (path.parent / link.split('#', 1)[0]).resolve()
                with self.subTest(file=path.name, link=link):
                    self.assertTrue(resolved.is_relative_to(SKILL_DIR.resolve()))
                    self.assertTrue(resolved.is_file())

    def test_distribution_links(self):
        self.required(ROOT / 'README.md')
        for path in walk('.md'):
            for link in re.findall(LINK_RE, path.read_text(encoding='utf-8')):
                if '://' in link or link.startswith('#'):
                    continue
                resolved = (path.parent / link.split('#', 1)[0]).resolve()
                with self.subTest(file=path.name, link=link):
                    self.assertTrue(resolved.is_relative_to(ROOT.resolve()))
                    self.assertTrue(resolved.exists())

    def test_markdown_integrity(self):
        self.required(ROOT / 'README.md')
        for path in walk('.md'):
            text = path.read_text(encoding='utf-8')
            self.assertTrue(text.endswith('\n'), str(path))
            active = None
            for line in text.splitlines():
                m = re.match(r'^(`{3,}|~{3,})(.*)$', line)
                if m:
                    marker, suffix = m.groups()
                    if active is None:
                        active = marker
                    elif marker[0] == active[0] and len(marker) >= len(active) and not suffix.strip():
                        active = None
            self.assertIsNone(active, str(path))

    def test_skill_body_is_host_neutral_outside_platform_notes(self):
        """Layout invariant about where host names may live, not a behavioral check."""
        lines = self.required(SKILL).splitlines()
        start = next((i for i, l in enumerate(lines) if l.strip() == '### Platform notes'), None)
        self.assertIsNotNone(start, 'Missing ### Platform notes heading')
        end = next((i for i in range(start + 1, len(lines))
                    if re.match(r'^#{1,3} ', lines[i])), len(lines))
        outside = '\n'.join(lines[:start] + lines[end:])
        for token in HOST_ONLY_TOKENS:
            with self.subTest(token=token):
                self.assertNotIn(token, outside)

    def test_smoke_cases_have_distinct_observable_outcomes(self):
        data = json.loads(self.required(ROOT / 'development/scenarios.json'))
        self.assertEqual(data['schema_version'], 1)
        cases = data['cases']
        self.assertTrue(cases)
        self.assertEqual(len(cases), len({c['id'] for c in cases}))
        for case in cases:
            self.assertIn(case['platform'], PLATFORMS)
            self.assertIsInstance(case['should_trigger'], bool)
            self.assertTrue(case['prompt'])
            self.assertTrue(case['must_observe'])
            self.assertTrue(case['must_not_observe'])
        self.assertTrue(any(not c['should_trigger'] for c in cases))


if __name__ == '__main__':
    unittest.main()
