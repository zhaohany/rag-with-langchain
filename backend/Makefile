PYTEST ?= python3 -m pytest
TEST ?=

.PHONY: test test-unit test-one

test:
	$(PYTEST)

test-unit:
	$(PYTEST) tests/exercises/pytest_examples.py tests/exercises/chunking_unit_exercise.py tests/exercises/health_service_unit_exercise.py -v

test-one:
	@if [ -z "$(TEST)" ]; then \
		echo "Usage: make test-one TEST=tests/exercises/chunking_unit_exercise.py::test_split_markdown_chunks_returns_empty_list_for_blank_text"; \
		exit 1; \
	fi
	$(PYTEST) $(TEST) -v
