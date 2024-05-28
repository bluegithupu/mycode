from textwrap import dedent
from crewai import Agent

class GameAgents():
	def senior_engineer_agent(self):
		return Agent(
			role='Senior Software Engineer',
			goal='Create software as needed',
			backstory=dedent("""\
				You are a Senior Software Engineer at a leading tech think tank.
				Your expertise in programming in python. and do your best to
				produce perfect code"""),
			allow_delegation=False,
			verbose=True
		)

	def qa_engineer_agent(self):
		return Agent(
			role='Software Quality Control Engineer',
  		goal='create prefect code, by analizing the code that is given for errors',
  		backstory=dedent("""\
				You are a software engineer that specializes in checking code
  			for errors. You have an eye for detail and a knack for finding
				hidden bugs.
  			You check for missing imports, variable declarations, mismatched
				brackets and syntax errors.
  			You also check for security vulnerabilities, and logic errors"""),
			allow_delegation=False,
			verbose=True
		)

	def chief_qa_engineer_agent(self):
		return Agent(
			role='Chief Software Quality Control Engineer',
  		goal='Ensure that the code does the job that it is supposed to do',
  		backstory=dedent("""\
				You feel that programmers always do only half the job, so you are
				super dedicate to make high quality code."""),
			allow_delegation=False,
			verbose=True
		)




from textwrap import dedent
from crewai import Task

class GameTasks():
	def code_task(self, agent, game):
		return Task(description=dedent(f"""You will create a game using python, these are the instructions:

			Instructions
			------------
    	{game}

			Your Final answer must be the full python code, only the python code and nothing else.
			"""),
			agent=agent,
            expected_output="full python code, only the python code and nothing else"

		)

	def review_task(self, agent, game):
		return Task(description=dedent(f"""\
			You are helping create a game using python, these are the instructions:

			Instructions
			------------
			{game}

			Using the code you got, check for errors. Check for logic errors,
			syntax errors, missing imports, variable declarations, mismatched brackets,
			and security vulnerabilities.

			Your Final answer must be the full python code, only the python code and nothing else.
			"""),
			agent=agent,
            expected_output="full python code, only the python code and nothing else"

		)

	def evaluate_task(self, agent, game):
		return Task(description=dedent(f"""\
			You are helping create a game using python, these are the instructions:

			Instructions
			------------
			{game}

			You will look over the code to insure that it is complete and
			does the job that it is supposed to do.

			Your Final answer must be the full python code, only the python code and nothing else.
			"""),
			agent=agent,
            expected_output="full python code, only the python code and nothing else"
            
		)




from dotenv import load_dotenv
load_dotenv()

from crewai import Crew


tasks = GameTasks()
agents = GameAgents()

print("## Welcome to the Game Crew")
print('-------------------------------')
# game = input("What is the game you would like to build? What will be the mechanics?\n")

# game = {"game":"2048"}
game = "2048"

# Create Agents
senior_engineer_agent = agents.senior_engineer_agent()
qa_engineer_agent = agents.qa_engineer_agent()
chief_qa_engineer_agent = agents.chief_qa_engineer_agent()

# Create Tasks
code_game = tasks.code_task(senior_engineer_agent, game)
review_game = tasks.review_task(qa_engineer_agent, game)
approve_game = tasks.evaluate_task(chief_qa_engineer_agent, game)

# Create Crew responsible for Copy
crew = Crew(
	agents=[
		senior_engineer_agent,
		qa_engineer_agent,
		chief_qa_engineer_agent
	],
	tasks=[
		code_game,
		review_game,
		approve_game
	],
	verbose=True
)

game1 = crew.kickoff()


# Print results
print("\n\n########################")
print("## Here is the result")
print("########################\n")
print("final code for the game:")
print(game1)