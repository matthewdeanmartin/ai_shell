poetry run pip3 install pdoc3
poetry run pdoc ai_shell ai_todo --html -o docs
poetry lock && poetry install --with dev --sync