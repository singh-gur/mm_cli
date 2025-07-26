
install:
    @uv sync

add *packages:
    @uv add {{ packages }}

check:
    @.venv/bin/ruff check --fix

sync *message:
    @git add .
    @git commit -am "{{ message }}"
    @git push

run *args:
    @uv run mm-cli {{ args }}