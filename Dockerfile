FROM python:3.10-slim

WORKDIR /app

COPY challenge_b.py .
COPY challenge_a_output.txt .

CMD ["python", "challenge_b.py", "challenge_a_output.txt", "challenge_c_output.txt"]