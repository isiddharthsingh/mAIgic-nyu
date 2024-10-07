# mAIgic

## Project Description
**mAIgic** is a project focused on setting up testing, static analysis, and continuous integration (CI) using tools such as `pytest`, `ruff`, `mypy`, and CircleCI. It aims to automate quality checks, ensuring code correctness and adherence to best practices.

## Features
- Unit testing with `pytest`
- Static code analysis with `ruff` (linter)
- Type checking with `mypy`
- Continuous Integration (CI) pipeline with CircleCI, running both tests and static analysis automatically on every push.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/mAIgic.git
cd mAIgic
```

### 2. Install Dependencies
This project uses `pytest`, `ruff`, and `mypy`. Install them using `pip`:
```bash
pip install pytest ruff mypy
```

Alternatively, if using the `uv` package manager:
```bash
uv sync
```

The above command will create a virtual environment `.venv` and install all the dependencies from the `uv.lock` file. Activate the environment by executing
```bash
source ./.venv/bin/activate
```

---

## Running Tests

### 1. Pytest
You can run unit tests using `pytest` by running the following command:
```bash
pytest tests
```

**Example Tests in `tests/test_samples.py`:**
- Basic arithmetic (addition, subtraction, multiplication, division)
- String operations (case-insensitive checks)
- List and dictionary operations
- Exception handling tests (checking for specific exceptions)

### 2. Ruff (Linter)
Use `ruff` to run static analysis (linting) on your code:
```bash
ruff check .
```

### 3. Mypy (Type Checking)
To perform static type checking using `mypy`, run:
```bash
mypy .
```

---

## CircleCI Configuration

The project is integrated with CircleCI for continuous integration. Every push to the repository automatically triggers the following steps:
1. **Install dependencies**: Installs `pytest`, `ruff`, and `mypy`.
2. **Run tests**: Executes all tests in the `tests/` folder using `pytest`.
3. **Run static analysis**: Runs `ruff` for linting and `mypy` for type checking.

### CircleCI Configuration in `.circleci/config.yml`:
```yaml
version: 2.1

jobs:
  test:
    docker:
      - image: circleci/python:3.8
    steps:
      - checkout
      - run:
          name: Install dependencies
          command: |
            pip install pytest ruff mypy
      - run:
          name: Run pytest tests
          command: pytest tests
      - run:
          name: Run ruff for linting
          command: ruff check .
      - run:
          name: Run mypy for type checking
          command: mypy .

workflows:
  version: 2
  test_and_static_analysis:
    jobs:
      - test
```

This configuration ensures that every commit automatically goes through testing and static analysis.

### View CircleCI Status:
The latest CircleCI build can be viewed [here](https://app.circleci.com/pipelines/circleci/L7kpZ5X2tZyEgUBhR4SB2j/NxWta8V9bEwRzTNu9Vzc3c/9/workflows/be567b6f-0c9c-41c8-91f7-e4789784b41f).

---

## Troubleshooting

### Common Errors:
1. **Missing Dependencies**: If any dependency-related issues arise, ensure all dependencies are installed by running:
   ```bash
   pip install -r requirements.txt
   ```
   or
   ```bash
   uv init
   ```


## License
This project is licensed under the MIT License.


### Explanation of the Sections:

1. **Project Description**: Provides an overview of what the project does.
2. **Features**: Highlights the major tools and features used.
3. **Setup Instructions**: Guides users on how to clone the repo, install dependencies, and initialize the project.
4. **Running Tests**: Explains how to run unit tests, static analysis, and type checks.
5. **CircleCI Configuration**: Outlines how CircleCI automates the process of testing and analysis, including the YAML configuration.
6. **Troubleshooting**: Offers solutions for common errors like string comparison and missing dependencies.
7. **License**: A placeholder for your project's license type.

## Teammates
- Siddharth Singh - sms10221@nyu.edu
- Adittya Mittal - am14079@nyu.edu
- Anushka Tawte - at5849@nyu.edu
- Rafael de Leon - rdl404@nyu.edu
- Alex Ying - aty2009@nyu.edu
- Mridul Mittal - mm13171@nyu.edu
