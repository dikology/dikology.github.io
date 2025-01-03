---
layout: ../../layouts/MarkdownPostLayout.astro
title: SQLFluff for a dbt Project
description: Step-by-Step Guide to Setting Up SQLFluff with Pre-Commit Hooks for a dbt Project
date: 2024-12-27
image:
  src: https://cdn.midjourney.com/f1f1d54a-8740-4594-a9bb-a1c9f4c49478/0_0.png
  alt: Anki cards about retention
featured: false
draft: true
category: data
---

### Step-by-Step Guide to Setting Up SQLFluff with Pre-Commit Hooks for a dbt Project

SQLFluff is an excellent tool for linting and formatting SQL. Starting with pre-commit hooks allows you to focus on incremental improvements without being overwhelmed by fixing all existing files at once. Here’s a guide to help you set it up:

---

#### 1. **Install SQLFluff and Pre-Commit**

Make sure you have Python installed. Then, install SQLFluff and Pre-Commit:

```bash
pip install sqlfluff pre-commit
```

---

#### 2. **Initialize Pre-Commit in Your Repository**

If Pre-Commit isn’t already set up in your project, initialize it:

```bash
pre-commit install
```

This creates a `.pre-commit-config.yaml` file if it doesn’t already exist.

---

#### 3. **Add SQLFluff to Pre-Commit Config**

Edit the `.pre-commit-config.yaml` file to include SQLFluff. Use the following configuration:

```yaml
repos:
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: v2.2.0 # Use the latest version or the one you're targeting
    hooks:
      - id: sqlfluff-lint
        stages: [commit] # Only run during commits
        files: "\\.sql$|\\.yml$|\\.yaml$" # Check SQL and YAML files
```

---

#### 4. **Configure SQLFluff**

SQLFluff requires a configuration file. Add a `.sqlfluff` file to the root of your dbt project:

```ini
[sqlfluff]
dialect = jinja  # Use dbt's Jinja dialect
templater = dbt  # Use dbt as the templater
exclude_rules = L003,L009  # Exclude rules you don't want initially
persist_outputs = True  # Helpful for debugging

[sqlfluff:templater:dbt]
profiles_dir = ~/.dbt  # Path to your dbt profiles.yml

[sqlfluff:rules]
max_line_length = 80  # Example: Set max line length
```

Adjust the rules and settings to fit your project.

---

#### 5. **Test Pre-Commit Locally**

Before pushing your changes, test the hook locally on a file you’re working on:

```bash
pre-commit run --files path/to/file.sql
```

This ensures the file conforms to SQLFluff’s rules. If issues are detected, SQLFluff will try to fix them automatically.

---

#### 6. **Limit Hooks to Modified Files**

Pre-commit automatically runs only on staged files. This ensures that only the files you are trying to commit are checked.

---

#### 7. **Run SQLFluff Manually (Optional)**

To check the entire project without committing, run:

```bash
sqlfluff lint models/  # Replace `models/` with your dbt model directory
```

You can also fix all fixable issues:

```bash
sqlfluff fix models/
```

---

#### 8. **Iterate and Expand**

Once you're comfortable with the basics:

- Expand rules in `.sqlfluff` to enforce stricter linting.
- Use `sqlfluff fix` to incrementally clean up older files.
- Add a CI/CD step for SQLFluff checks to enforce standards in pull requests.

---

#### 9. **Resources and References**

- [SQLFluff Documentation](https://docs.sqlfluff.com/)
- [Pre-Commit Documentation](https://pre-commit.com/)

By starting with Pre-Commit and focusing on modified files, you avoid being overwhelmed while ensuring consistent SQL quality for all new code. 🚀
