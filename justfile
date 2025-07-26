
install:
    @uv sync

add *packages:
    @uv add {{ packages }}

check:
    @ruff check --fix

sync *message:
    @git add .
    @git commit -m "{{ message }}"
    @git push