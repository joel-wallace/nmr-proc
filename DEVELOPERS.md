# Developer Guide

This guide is for contributors working on the codebase. It covers structure, conventions, and collaboration practices.

## 📁 Project Structure

```
project-root/
├── src/          # Main Python source files
├── tests/        # Unit tests
├── requirements.txt
└── DEVELOPERS.md
```

## 🔁 Git & Branching

- Use `feature/`, `bugfix/`, or `refactor/` prefixes:
  ```
  git checkout -b feature/short-description
  ```
- Open pull requests against `main`.
- Write clear, focused commit messages.

## 🧹 Code Style

- Follow [PEP8](https://peps.python.org/pep-0008/)
- Use tools like `black` and `ruff`:
  ```
  black src/ tests/
  ruff .
  ```

## 🧑‍💻 Contact

For development questions, reach out to:

- [@joel-wallace](https://github.com/joel-wallace)
- [@dandanaher](https://github.com/dandanaher)

