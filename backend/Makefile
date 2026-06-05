PYTEST ?= python3 -m pytest
TEST ?=

.PHONY: test test-unit test-one

test:
	$(PYTEST)

test-unit:
	$(PYTEST) tests/student_unit_assignment.py -v

test-one:
	@if [ -z "$(TEST)" ]; then \
		echo "Usage: make test-one TEST=tests/student_unit_assignment.py::test_split_markdown_chunks_returns_empty_list_for_blank_text"; \
		exit 1; \
	fi
	$(PYTEST) $(TEST) -v
