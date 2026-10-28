# Contributing Guidelines

## All coding and documentation will be done in english

## Python:
* We build the code structure according to OOP-principles.
* Type hinting  `variable_name: string`
* Docstrings `""" comment """`
* Use Inline comments when explaining a specific solution  `#Comment on line`
* For indentation use: 4 spaces
* Use `.env` and gitignore `.env`

## Naming Convension:
* Variables and `functions()` = `snake_case`
* `GLOABL_VARIABLES` and `CONSTANTS` = `UPPER_SNAKE_CASE`
* `Class` = `PascalCase`

## Error handling:
Specify exception errors:

* **Bad: Too generic**
  ```python
  try: 
    result = 10 / number 
  except: 
    Pass
  ```

* **Good: Handle the exact error you anticipate**
  ```python
  def example(input: str) -> float | None: 
    try: 
      number: int = int(input) 
      return 10 / number 

    except ValueError: print("Input must be a valid number.") 
       return None 

    except ZeroDivisionError: print("Cannot divide by zero.") 
      return None
  ```

## Commits:
* Always document code before commits. There should be descriptive docstrings. 
* Branches should not be older than 3 days, try to update the branch with a merge into. If the work is not finished.
* One branch for each issue.
* Pull Request should not be managed by the committee

## Conventional Commit Types
Commits must follow the format: 
Use YouTrack Issue ID when committing (t.ex HU-50) 
`<ISSUE-ID> <type>: <description>`

| Type | Purpose |
| :--- | :--- |
| `feat` | Adds a new feature or functionality |
| `fix` | Resolves a bug or unintended behavior |
| `docs` | Documentation changes only (README, docstrings) |
| `test` | Adds or refactors unit/integration tests |
| `refactor` | Code changes that neither fix a bug nor add a feature |
| `chore` | Tooling, dependencies, or configuration updates |

## Testing:
* Pytest? (pytest & unit testing)
* Testing before main branch? (ci pipeline)
* Unittesting? (unittests in the pytest file)
* Use fixtures to set up common test data 
* Leverage parametrization in pytest to cover more cases
* Run tests frequently during development
* Aim for reasonable test coverage 
* Keep unit tests fast and deterministic 
* Use mocks for external dependencies 
* Complement unit tests with integration and end-to-end tests

## Cohesion:
* Single-responsibility Principle

## Security:
* Input validation? (what input is expected)
* Authentication – salt passwords using bcrypt →
* Authorization?

## Architecture:

```text
my-project/
├── .gitignore                # Ignores both .venv/ and frontend/node_modules/
├── README.md
│
├── .venv/                    # Python virtual environment (ignored by Git)
│
├── backend/                  # Python backend root
│   ├── pyproject.toml        # Python dependencies, Ruff, and Pytest configuration
│   ├── .env.example          # Backend environment template
│   ├── src/
│   │   └── my_project/
│   │       ├── __init__.py
│   │       ├── __main__.py
│   │       ├── config.py
│   │       ├── exceptions.py
│   │       ├── models/      # What is this shape of data?
│   │       ├── repositories/# Where/how do we read or write it?
│   │       └── services/    # What do we do with the data?
│   └── tests/
│       ├── conftest.py
│       └── unit/
│
└── frontend/                 # React application (e.g., Vite + React)
    ├── package.json          # Node dependencies & npm scripts
    ├── package-lock.json
    ├── vite.config.js        # Vite configuration (includes API proxy)
    ├── .env.example          # Frontend environment template (e.g., VITE_API_URL)
    ├── node_modules/         # Frontend dependencies (ignored by Git)
    ├── public/
    └── src/
        ├── assets/
        ├── components/
        ├── App.jsx
        └── main.jsx
```
