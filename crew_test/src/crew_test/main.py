#!/usr/bin/env python
from crew_test.crew import CrewTestCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'AI LLMs'
    }
    CrewTestCrew().crew().kickoff(inputs=inputs)