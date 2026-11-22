# Scan Timing API

Analyze timing gaps in a synthetic sequence of scan commands. Given a series of timestamps and an allowed interval, the API reports how often the next command arrived late. This standalone portfolio project processes submitted traces offline.

## Try it

Start the service with `docker compose up --build api`. Interactive documentation is at http://localhost:8000/docs.

```sh
curl -s http://localhost:8000/analyze -H 'Content-Type: application/json' \
  -d '{"timestamps_us":[0,100,260,350],"deadline_us":100}'
```

```json
{"interval_count":3,"deadline_misses":1,"miss_rate_pct":33.333,"max_gap_us":160,"p95_gap_us":160}
```

The three intervals are 100, 160 and 90 microseconds. Only 160 exceeds the deadline. The 95th percentile uses nearest rank. Submit 2 to 10,000 strictly increasing nonnegative integer timestamps from one clock, in microseconds. Invalid traces return HTTP 422.

## Run the tests

Run `docker compose run --build --rm tests`. The same command runs in GitHub Actions on pushes and pull requests, followed by an HTTP health check against the runtime container.

Without Docker, use Python 3.12 in a virtual environment, install `pip install -r requirements-test.txt`, then run `python -m pytest -q` or start the server with `uvicorn main:app`.

Run `python check_synthetic.py` for a dependency-free check of all 1,024 five-interval traces whose gaps range from 1 to 4 microseconds, using a 2-microsecond deadline.
