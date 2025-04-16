### Setup Virtual Environment

Create Virtual Env. Please use Python3
- python -m venv py3env

Activate Virtual Env
- source py3env/bin/activate

### Setup Dockerfile

Build Docker Image
- docker build -t challenge-b .

### Run Dockerfile

- docker run --rm -v $(pwd):/app challenge-b