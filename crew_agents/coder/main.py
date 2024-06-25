from coder_agent import CoderAgent, web_scraping_task
from crewai import Crew

agent = CoderAgent()
task = web_scraping_task(agent, "https://movie.douban.com/top250")

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

crew.kickoff()
