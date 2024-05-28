from dotenv import load_dotenv
load_dotenv()


from crewai import Agent
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

researcher = Agent(
  role='Senior Researcher',
  goal='Uncover groundbreaking technologies in AI in healthcare',
  backstory='You have a PhD in AI and have been researching AI in healthcare for 10 years.',
  verbose=True,
  memory=True,
  tools=[search_tool],
  allow_delegation=True
)

writer = Agent(
  role='Writer',
  goal='Narrate compelling tech stories about AI in healthcare',
  backstory='You have a degree in journalism and have been writing about tech for 5 years.',
  verbose=True,
  memory=True,
  tools=[search_tool],
  allow_delegation=False
)


from crewai import Task

research_task = Task(
  description="Identify the next big trend in AI in healthcare.",
  expected_output='A comprehensive 3 paragraphs long report on the latest AI trends.',
  tools=[search_tool],
  agent=researcher,
)

write_task = Task(
  description="Compose an insightful article on AI in healthcare.",
  expected_output='A 4 paragraph article on AI in healthcare advancements formatted as markdown.',
  tools=[search_tool],
  agent=writer,
  async_execution=False,
  output_file='new-blog-post.md'
)



from crewai import Crew, Process

crew = Crew(
  agents=[researcher, writer],
  tasks=[research_task, write_task],
  process=Process.sequential
)

result = crew.kickoff(inputs={'topic': 'AI in healthcare'})
print(result)
