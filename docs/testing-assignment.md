# Pytest Unit Testing Assignment

## Goal

Practice writing focused pytest unit tests for small backend functions without starting FastAPI, calling LLMs, building FAISS indexes, or using the network.

## What Students Should Edit

Only edit:

- `backend/tests/student_unit_assignment.py`

Do not edit production code unless the instructor explicitly asks you to.

## Setup

From `backend/`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Tests

From `backend/`:

```bash
make test-unit
```

Run one scenario:

```bash
make test-one TEST=tests/student_unit_assignment.py::test_split_markdown_chunks_returns_empty_list_for_blank_text
```

Run all backend tests:

```bash
make test
```

## Assignment Scenarios

Replace each `pytest.fail(...)` placeholder in `backend/tests/student_unit_assignment.py` with the production function call and assertions. The setup data is already provided for each scenario.

Required scenarios:

- `split_markdown_chunks(...)` returns `[]` for blank text
- `split_markdown_chunks(...)` raises `ValueError` for invalid chunk settings
- `split_markdown_chunks(...)` keeps a small markdown document as one clean chunk
- `HealthService.get_status()` returns defaults when the metadata file is missing
- `HealthService.get_status()` reads valid system metadata JSON
- `HealthService.get_status()` falls back to defaults when metadata JSON is invalid

Reference examples already included in the test file:

- `test_example_plain_assertion` shows a basic function call plus `assert`
- `test_example_pytest_raises` shows `pytest.raises(...)`

## Expected Student Outcome

Before implementation, `make test-unit` should show the two reference examples passing and the student placeholders failing intentionally.

After students complete the tests, `make test-unit` should pass.
