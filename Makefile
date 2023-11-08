.PHONY: test env setup

# Run tests with a human-friendly output format
test:
	pytest --verbose

# Set up a conda environment with all the requirements
conda:
	conda create --name meeting_muncher --file requirements.txt

# Set up the package without conda, using system Python and pip
setup:
	python3 -m pip install -r requirements.txt
