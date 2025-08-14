#!/usr/bin/env python3
"""
L5: Automate Event Planning

This module demonstrates advanced task features in crewAI for event planning automation.
It showcases various task configuration options including human input, output formatting,
async execution, and file output capabilities.

Key Concepts Covered:
- Advanced task configuration options
- Human input integration for task approval
- Output formatting with Pydantic models
- File output generation (JSON, Markdown)
- Asynchronous task execution
- Parallel task processing
- Tool integration for venue research and logistics

Author: CrewAI Course
Date: 2024
"""

# Standard library imports
import os
import json
import warnings
from pprint import pprint

# Third-party imports
from dotenv import load_dotenv
from pydantic import BaseModel
from crewai import Agent, Crew, Task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

# Local imports
from utils import get_openai_api_key, get_serper_api_key


def setup_environment():
    """
    Set up the environment variables and API keys.
    
    This function loads environment variables and sets up API configurations
    for OpenAI and Serper (search API) services.
    """
    # Suppress warnings for cleaner output
    warnings.filterwarnings('ignore')
    
    # Load environment variables from .env file
    _ = load_dotenv(override=True)
    
    # Get and set API keys
    openai_api_key = get_openai_api_key()
    serper_api_key = get_serper_api_key()
    
    # Set environment variables
    os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
    os.environ["SERPER_API_KEY"] = serper_api_key
    
    print("Environment setup completed successfully!")
    print(f"OpenAI API Key: {openai_api_key[:20]}...")
    print(f"Serper API Key: {serper_api_key[:20]}...")
    
    return openai_api_key, serper_api_key


def setup_tools():
    """
    Set up the tools that agents can use for event planning.
    
    This function configures search and web scraping tools that agents
    will use to gather information about venues, logistics, and marketing.
    
    Returns:
        tuple: A tuple containing (search_tool, scrape_tool)
    """
    
    # Initialize the tools
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()
    
    print("Tools configured successfully!")
    print("Available tools:")
    print("- Search Tool: For web search capabilities")
    print("- Scrape Tool: For extracting information from websites")
    
    return search_tool, scrape_tool


def create_agents(search_tool, scrape_tool):
    """
    Create the AI agents for event planning automation.
    
    This function creates specialized agents for:
    - Venue coordination and selection
    - Logistics management
    - Marketing and communications
    
    Args:
        search_tool: Tool for web search capabilities
        scrape_tool: Tool for web scraping
        
    Returns:
        tuple: A tuple containing (venue_coordinator, logistics_manager, marketing_communications_agent)
    """
    
    # Agent 1: Venue Coordinator
    # This agent identifies and books appropriate venues
    venue_coordinator = Agent(
        role="Venue Coordinator",
        goal="Identify and book an appropriate venue "
             "based on event requirements",
        tools=[search_tool, scrape_tool],
        verbose=True,
        backstory=(
            "With a keen sense of space and "
            "understanding of event logistics, "
            "you excel at finding and securing "
            "the perfect venue that fits the event's theme, "
            "size, and budget constraints."
        )
    )
    
    # Agent 2: Logistics Manager
    # This agent manages all logistical aspects of the event
    logistics_manager = Agent(
        role='Logistics Manager',
        goal=(
            "Manage all logistics for the event "
            "including catering and equipment"
        ),
        tools=[search_tool, scrape_tool],
        verbose=True,
        backstory=(
            "Organized and detail-oriented, "
            "you ensure that every logistical aspect of the event "
            "from catering to equipment setup "
            "is flawlessly executed to create a seamless experience."
        )
    )
    
    # Agent 3: Marketing and Communications Agent
    # This agent handles event promotion and attendee communication
    marketing_communications_agent = Agent(
        role="Marketing and Communications Agent",
        goal="Effectively market the event and "
             "communicate with participants",
        tools=[search_tool, scrape_tool],
        verbose=True,
        backstory=(
            "Creative and communicative, "
            "you craft compelling messages and "
            "engage with potential attendees "
            "to maximize event exposure and participation."
        )
    )
    
    return venue_coordinator, logistics_manager, marketing_communications_agent


def create_venue_model():
    """
    Create a Pydantic model for venue details.
    
    This function demonstrates how to use Pydantic BaseModel to define
    structured output formats for agents. The agents will populate this
    object with information about different venues.
    
    Returns:
        VenueDetails: A Pydantic model class for venue information
        
    Note:
        This demonstrates the output_json feature in crewAI tasks,
        allowing for structured, validated output from agents.
    """
    
    class VenueDetails(BaseModel):
        """
        Pydantic model for venue details.
        
        This model defines the structure for venue information that agents
        will populate when researching and selecting venues.
        """
        name: str
        address: str
        capacity: int
        booking_status: str
    
    return VenueDetails


def create_tasks(venue_coordinator, logistics_manager, marketing_communications_agent, VenueDetails):
    """
    Create the tasks for event planning automation.
    
    This function demonstrates various advanced task features:
    - human_input: Tasks that require human approval before completion
    - output_json: Structured output using Pydantic models
    - output_file: File output generation (JSON, Markdown)
    - async_execution: Parallel task execution
    
    Args:
        venue_coordinator: The Venue Coordinator agent
        logistics_manager: The Logistics Manager agent
        marketing_communications_agent: The Marketing and Communications agent
        VenueDetails: The Pydantic model for venue information
        
    Returns:
        tuple: A tuple containing (venue_task, logistics_task, marketing_task)
    """
    
    # Task 1: Venue Selection
    # This task demonstrates human input and structured output
    venue_task = Task(
        description="Find a venue in {event_city} "
                    "that meets criteria for {event_topic}.",
        expected_output="All the details of a specifically chosen"
                        "venue you found to accommodate the event.",
        human_input=True,  # Requires human feedback before finalizing
        output_json=VenueDetails,  # Structured output using Pydantic model
        output_file="venue_details.json",  # Outputs venue details as JSON file
        agent=venue_coordinator
    )
    
    # Task 2: Logistics Coordination
    # This task demonstrates async execution for parallel processing
    logistics_task = Task(
        description="Coordinate catering and "
                     "equipment for an event "
                     "with {expected_participants} participants "
                     "on {tentative_date}.",
        expected_output="Confirmation of all logistics arrangements "
                        "including catering and equipment setup.",
        human_input=True,  # Requires human feedback before finalizing
        async_execution=True,  # Can run in parallel with subsequent tasks
        agent=logistics_manager
    )
    
    # Task 3: Marketing and Communications
    # This task demonstrates async execution and file output
    marketing_task = Task(
        description="Promote the {event_topic} "
                    "aiming to engage at least"
                    "{expected_participants} potential attendees.",
        expected_output="Report on marketing activities "
                        "and attendee engagement formatted as markdown.",
        async_execution=True,  # Can run in parallel with other tasks
        output_file="marketing_report.md",  # Outputs the report as a markdown file
        agent=marketing_communications_agent
    )
    
    return venue_task, logistics_task, marketing_task


def create_crew(agents, tasks):
    """
    Create the crew of agents to work on event planning tasks.
    
    This function demonstrates crew orchestration with multiple agents
    and tasks, including async execution capabilities.
    
    Args:
        agents: List of agents (venue_coordinator, logistics_manager, marketing_communications_agent)
        tasks: List of tasks (venue_task, logistics_task, marketing_task)
        
    Returns:
        Crew: A configured crew ready to execute tasks
        
    Note:
        Since async_execution=True is set for logistics_task and marketing_task,
        the order for them does not matter in the tasks list.
    """
    
    # Define the crew with agents and tasks
    event_management_crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True
    )
    
    return event_management_crew


def run_event_planning(event_topic="Tech Innovation Conference", 
                      event_description="A gathering of tech innovators and industry leaders to explore future technologies.",
                      event_city="San Francisco", tentative_date="2024-09-15",
                      expected_participants=500, budget=20000, venue_type="Conference Hall"):
    """
    Execute the complete event planning automation process.
    
    This function demonstrates the complete workflow of:
    - Venue research and selection
    - Logistics coordination
    - Marketing and communications planning
    - Human input integration
    - File output generation
    
    Args:
        event_topic (str): The topic/theme of the event
        event_description (str): Detailed description of the event
        event_city (str): City where the event will be held
        tentative_date (str): Tentative date for the event
        expected_participants (int): Expected number of participants
        budget (int): Budget for the event
        venue_type (str): Type of venue required
        
    Returns:
        CrewOutput: The result of the crew execution
    """
    
    # Set up environment
    setup_environment()
    
    # Set up tools
    search_tool, scrape_tool = setup_tools()
    
    # Create agents
    venue_coordinator, logistics_manager, marketing_communications_agent = create_agents(
        search_tool, scrape_tool
    )
    
    # Create venue model
    VenueDetails = create_venue_model()
    
    # Create tasks
    venue_task, logistics_task, marketing_task = create_tasks(
        venue_coordinator, logistics_manager, marketing_communications_agent, VenueDetails
    )
    
    # Create crew
    event_management_crew = create_crew(
        [venue_coordinator, logistics_manager, marketing_communications_agent],
        [venue_task, logistics_task, marketing_task]
    )
    
    # Prepare event details for the crew
    event_details = {
        'event_topic': event_topic,
        'event_description': event_description,
        'event_city': event_city,
        'tentative_date': tentative_date,
        'expected_participants': expected_participants,
        'budget': budget,
        'venue_type': venue_type
    }
    
    # Execute the crew
    print(f"Starting event planning for: {event_topic}")
    print(f"Location: {event_city}")
    print(f"Date: {tentative_date}")
    print(f"Expected Participants: {expected_participants}")
    print(f"Budget: ${budget:,}")
    print("\nExecuting crew...")
    
    result = event_management_crew.kickoff(inputs=event_details)
    
    return result


def display_generated_files():
    """
    Display the generated output files from the event planning process.
    
    This function demonstrates how to access and display the files
    generated by the crewAI tasks, including JSON and Markdown outputs.
    """
    
    print("\n" + "="*60)
    print("GENERATED OUTPUT FILES")
    print("="*60)
    
    # Display venue details JSON file
    try:
        print("\n1. Venue Details (venue_details.json):")
        with open('venue_details.json') as f:
            data = json.load(f)
        pprint(data)
    except FileNotFoundError:
        print("venue_details.json not found. The file may not have been generated yet.")
    except Exception as e:
        print(f"Error reading venue_details.json: {e}")
    
    # Display marketing report markdown file
    try:
        print("\n2. Marketing Report (marketing_report.md):")
        with open('marketing_report.md', 'r') as f:
            content = f.read()
        print(content)
    except FileNotFoundError:
        print("marketing_report.md not found. The file may not have been generated yet.")
        print("Note: After kickoff execution has successfully run, wait an extra 45 seconds")
        print("for the marketing_report.md file to be generated.")
    except Exception as e:
        print(f"Error reading marketing_report.md: {e}")


def demonstrate_task_features():
    """
    Demonstrate the advanced task features used in event planning.
    
    This function explains the key task configuration options:
    - human_input: For human approval and feedback
    - output_json: For structured, validated output
    - output_file: For file generation
    - async_execution: For parallel task processing
    """
    print("\n" + "="*60)
    print("ADVANCED TASK FEATURES IN CREWAI")
    print("="*60)
    print("""
1. HUMAN INPUT INTEGRATION:
   - human_input=True: Tasks pause for human feedback before completion
   - Allows for approval, rejection, or modification of agent outputs
   - Ensures human oversight in critical decision-making processes
   - Useful for tasks requiring human judgment or approval

2. STRUCTURED OUTPUT:
   - output_json: Specifies Pydantic model for structured output
   - Ensures consistent, validated data format from agents
   - Reduces parsing errors and improves data quality
   - Enables type checking and validation

3. FILE OUTPUT GENERATION:
   - output_file: Generates files in various formats (JSON, Markdown, etc.)
   - Automates documentation and report generation
   - Enables easy sharing and archiving of results
   - Supports multiple output formats for different use cases

4. ASYNCHRONOUS EXECUTION:
   - async_execution=True: Allows tasks to run in parallel
   - Improves overall execution time for independent tasks
   - Enables efficient resource utilization
   - Order of async tasks in the list doesn't matter

5. TASK DEPENDENCIES:
   - Sequential tasks: Dependent on each other, order matters
   - Parallel tasks: Independent, can run simultaneously
   - Mixed workflows: Combine both approaches for optimal performance
    """)


def main():
    """
    Main function to demonstrate the event planning automation system.
    """
    print("🚀 L5: Automate Event Planning")
    print("=" * 60)
    
    try:
        # Run the event planning process
        result = run_event_planning()
        
        # Display results
        print("\n" + "="*60)
        print("EVENT PLANNING COMPLETED!")
        print("="*60)
        print(f"Result type: {type(result)}")
        print(f"Result content:\n{result}")
        
        # Display generated files
        display_generated_files()
        
        # Demonstrate task features
        demonstrate_task_features()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        print("Please check your API keys and environment setup.")
        print("\nNote: Some tasks require human input. When prompted:")
        print("- Use your mouse pointer to click in the text box before typing")
        print("- Provide feedback on whether you like the results or not")
        print("- Wait for the system to process your input before continuing")


if __name__ == "__main__":
    main()
