# LEAVE REQUEST PARSING

This project is a simple application of llm to parse information from leave requests.

## INSTALLATION

1. Clone the repository.

```bash
git clone -b newone https://github.com/toggle-corp/summary-_tech.git
cd summary-_tech
```

2. Build and run the Docker container:

```bash
docker compose up --build
```

## API USAGE

To hit the endpoint, you can send a POST request to http://127.0.0.1:8000/leave/ from postman.

For example,

```python
{
    "leave_request": "Ranjan: I will be late for standup or on first half leave tomorrow depending on how quickly the car issues will be resolved at the service center."
}
```

The llm model will give output in json format

```python
{
    "name": "Ranjan",
    "late": true,
    "leave": true,
    "WFH": false,
    "start_date": "2024-11-08",
    "end_date": null,
    "reason": "Car issues"
}
```

## REQUIREMENT

Ollama service should be running.
If there are no models in ollama you should use the

```bash
ollama pull "model-name"
```

To start the ollama service

```bash
service ollama start
```
