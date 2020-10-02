poetry run python -m cProfile -o main.prof main.py
poetry run snakeviz main.prof
