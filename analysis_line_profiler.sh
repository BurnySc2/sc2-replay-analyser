poetry run kernprof -l main.py
poetry run python -m line_profiler main.py.lprof > line_profiler_result.txt
rm main.py.lprof
