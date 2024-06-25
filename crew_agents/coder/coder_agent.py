from crewai import Agent, Task
from textwrap import dedent


class CoderAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Software Developer',
            goal='Write high-quality code based on given specifications',
            backstory=dedent("""\
                You are a skilled software developer with a strong background in Python.
                Your primary task is to write clean, efficient, and maintainable code.
                You are proficient in various programming paradigms and design patterns."""),
            allow_delegation=False,
            verbose=True
        )


def web_scraping_task(self, agent, url):
    return Task(description=dedent(f"""\
			You are tasked with creating a web scraping program to fetch the top 250 movies from Douban.
			The URL for the data is: {url}

			Instructions
			------------
			Write a Python script using libraries like requests and BeautifulSoup to scrape the data.
			Ensure the script handles pagination to collect all 250 movie entries.

			Your Final answer must be the full python code, only the python code and nothing else.
			"""),
                agent=agent,
                expected_output="full python code, only the python code and nothing else"
            )


