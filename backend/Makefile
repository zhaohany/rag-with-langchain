PYTEST ?= python3 -m pytest
TEST ?=

.PHONY: test test-ci test-unit test-one

test:
	$(PYTEST)

# CI-friendly target: only the tests expected to pass (health service + health API).
# Chunking tests are a separate student exercise and are not part of CI.
test-ci:
	$(PYTEST) tests/test_health_api.py tests/test_health_service.py -v

test-unit:
	$(PYTEST) tests/test_chunking.py tests/test_health_service.py -v

test-one:
	@if [ -z "$(TEST)" ]; then \
		echo "Usage: make test-one TEST=tests/test_chunking.py::test_split_markdown_chunks_returns_empty_list_for_blank_text"; \
		exit 1; \
	fi
	$(PYTEST) $(TEST) -v
