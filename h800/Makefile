
TESTS = punchcard_test.py arguscard_test.py bitfield_test.py word_test.py instruction_test.py instructions_test.py

default: tests

tests: $(TESTS)
	pytest -x punchcard_test.py 
	pytest -x arguscard_test.py 
	pytest -x bitfield_test.py 
	pytest -x word_test.py 
	pytest -x registers_test.py 
	pytest -x instruction_test.py 
	pytest -x instructions_test.py

