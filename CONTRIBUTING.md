# Contributing Guidelines

## All coding and documentation will be done in english

## Python:
* We build the code structure according to OOP-principles.
* Type hinting `variable_name: str`
* Docstrings `""" comment """`
* Use Inline comments when explaining a specific solution `#Comment on line`
* For indentation use: 4 spaces
* Use `.env` and gitignore `.env`

## Naming Convension:
* Variables and `functions()` = `snake_case`
* `GLOABL_VARIABLES` and `CONSTANTS` = `UPPER_SNAKE_CASE`
* `Class` = `PascalCase`

## Error handling:
Specify exception errors:

**Bad: Too generic**
```python
try: 
  result = 10 / number 
except: 
  Pass
