from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SeleniumScrapingTool

@CrewBase
class ComplianceQaAutomationAndDocumentationCrew():
    """ComplianceQaAutomationAndDocumentation crew"""

    @agent
    def web_app_test_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['web_app_test_specialist'],
            
        )

    @agent
    def mobile_app_test_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['mobile_app_test_specialist'],
            
        )

    @agent
    def documentation_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['documentation_expert'],
            
        )

    @agent
    def summary_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['summary_analyst'],
            
        )


    @task
    def execute_web_app_test_cases(self) -> Task:
        return Task(
            config=self.tasks_config['execute_web_app_test_cases'],
            tools=[SeleniumScrapingTool()],
        )

    @task
    def capture_web_app_documentation(self) -> Task:
        return Task(
            config=self.tasks_config['capture_web_app_documentation'],
            
        )

    @task
    def execute_mobile_app_test_cases(self) -> Task:
        return Task(
            config=self.tasks_config['execute_mobile_app_test_cases'],
            
        )

    @task
    def capture_mobile_app_documentation(self) -> Task:
        return Task(
            config=self.tasks_config['capture_mobile_app_documentation'],
            
        )

    @task
    def summarize_results(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_results'],
      
        )


    @crew
    def crew(self) -> Crew:
        """Creates the ComplianceQaAutomationAndDocumentation crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )



from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import MultiOnTool

# Initialize the tool from a MultiOn Tool
multion_tool = MultiOnTool(api_key='ba48ee23026044b89d02322a3b91dbee', local=False)

Browser = Agent(
    role="Browser Agent",
    goal="control web browsers using natural language ",
    backstory="An expert browsing agent.",
    tools=[multion_remote_tool],
    verbose=True,
)

# example task to search and summarize news
browse = Task(
    description="Summarize the top 3 trending AI News headlines",
    expected_output="A summary of the top 3 trending AI News headlines",
    agent=Browser,
)

crew = Crew(agents=[Browser], tasks=[browse])

crew.kickoff()

# Uncomment the following line to use an example of a custom tool
# from quell.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class Quell():
	"""Quell crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@before_kickoff # Optional hook to be executed before the crew starts
	def pull_data_example(self, inputs):
		# Example of pulling data from an external API, dynamically changing the inputs
		inputs['extra_data'] = "This is extra data"
		return inputs

	@after_kickoff # Optional hook to be executed after the crew has finished
	def log_results(self, output):
		# Example of logging results, dynamically changing the output
		print(f"Results: {output}")
		return output

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Quell crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
