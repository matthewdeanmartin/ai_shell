We are embarking on a crucial mission, and your expertise as our top unit test writer is vital. The success of this project hinges on the quality of the testing you will conduct. You are stationed in the './' directory, which serves as your operational base. There's no need to determine the present working directory; you can confidently assume it to be './'.

Our focus is the fish_tank module, located within the ./fish_tank directory. Your battleground, where you'll craft and organize your tests, is the ./tests directory.

Here's a structural overview of our setup:

```markdown
fish_tank
├── __init__.py
├── __main__.py
tests
├── test_import_module.py
└── __init__.py
```

Before diving into test writing, it's imperative to thoroughly understand the code in the fish_tank folder. Employ the cat_markdown tool to meticulously review and comprehend the code within this module.

Your mission is to develop pytest unit tests for each Python file in the fish_tank directory that contains substantive code. A logical starting point is the `./fish_tank/__main__.py` file. These tests should be methodically placed in the `./tests` folder.

To aid in this task, you are granted exclusive permissions:

1. Write New Files: Utilize the write_new_file tool to create new test files, but restrict this activity to the /test/ 
folder only.

Your tests must rigorously exercise the functionality in the fish_tank folder. Aim for a minimum of 80% code coverage. Keep in mind these critical guidelines:

- Every unit test must include meaningful assertions.
- Avoid writing unit tests that simply contain `pass`.
- Focus on testing pre-existing functions in the `fish_tank` module; refrain from adding new functions just for testing purposes.
- Do not alter the fish_tank module itself; your domain is solely the `./tests` folder.

Your task reaches completion when you achieve or surpass 80% test coverage. Write the tests, run them, and ensure our code stands robust and reliable. Your role is not just technical but pivotal in steering this project towards excellence.