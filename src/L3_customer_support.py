#!/usr/bin/env python3
"""
L3: Multi-agent Customer Support Automation

This module demonstrates how to create a multi-agent system for customer support
using the crewAI framework. It showcases the six key elements that make agents
perform better: Role Playing, Focus, Tools, Cooperation, Guardrails, and Memory.

Key Concepts Covered:
- Role playing and character development for agents
- Focus and goal-oriented agent behavior
- Tool integration for enhanced capabilities
- Agent cooperation and delegation
- Guardrails for controlled responses
- Memory for context retention across interactions

Author: CrewAI Course
Date: 2024
"""

# Standard library imports
import os
import warnings

# Third-party imports
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool


def setup_environment():
    """
    Set up the environment variables and API keys.
    
    This function loads environment variables from a .env file and sets up
    the OpenAI API configuration for the agents to use.
    """
    # Suppress warnings for cleaner output
    warnings.filterwarnings('ignore')
    
    # Load environment variables from .env file
    _ = load_dotenv(override=True)
    
    # Set the OpenAI model to use
    os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
    
    # Verify API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    print(f"API Key loaded: {api_key[:20]}...")
    return api_key


def create_agents():
    """
    Create the AI agents for customer support automation.
    
    This function demonstrates the key concepts of:
    - Role Playing: Agents are given specific roles, goals, and backstories
    - Focus: Agents are prompted to get into character of their roles
    - Cooperation: Agents can delegate work to each other
    
    Returns:
        tuple: A tuple containing (support_agent, support_quality_assurance_agent)
    """
    
    # Agent 1: Senior Support Representative
    # This agent handles the primary customer inquiry
    support_agent = Agent(
        role="Senior Support Representative",
        goal="Be the most friendly and helpful "
             "support representative in your team",
        backstory=(
            "You work at crewAI (https://crewai.com) and "
            "are now working on providing "
            "support to {customer}, a super important customer "
            "for your company."
            "You need to make sure that you provide the best support!"
            "Make sure to provide full complete answers, "
            "and make no assumptions."
        ),
        allow_delegation=False,  # This agent cannot delegate work
        verbose=True
    )
    
    # Agent 2: Support Quality Assurance Specialist
    # This agent reviews and improves the support responses
    support_quality_assurance_agent = Agent(
        role="Support Quality Assurance Specialist",
        goal="Get recognition for providing the "
             "best support quality assurance in your team",
        backstory=(
            "You work at crewAI (https://crewai.com) and "
            "are now working with your team "
            "on a request from {customer} ensuring that "
            "the support representative is "
            "providing the best support possible.\n"
            "You need to make sure that the support representative "
            "is providing full"
            "complete answers, and make no assumptions."
        ),
        verbose=True
        # Note: By not setting allow_delegation=False, it defaults to True
        # This means the agent CAN delegate its work to another agent
    )
    
    return support_agent, support_quality_assurance_agent


def setup_tools():
    """
    Set up the tools that agents can use to enhance their capabilities.
    
    This function demonstrates:
    - Tool integration for enhanced agent capabilities
    - Different ways to provide tools to agents
    - Tool configuration and customization
    
    Returns:
        ScrapeWebsiteTool: A configured web scraping tool
    """
    
    # Initialize a document scraper tool
    # This tool will scrape a specific page of the CrewAI documentation
    docs_scrape_tool = ScrapeWebsiteTool(
        website_url="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/"
    )
    
    print("Tools configured successfully!")
    print("Note: Task Tools override Agent Tools when specified at the task level.")
    
    return docs_scrape_tool


def create_tasks(support_agent, support_quality_assurance_agent, docs_scrape_tool):
    """
    Create the tasks for customer support automation.
    
    This function demonstrates:
    - Task-level tool assignment
    - Task dependencies and workflow
    - Expected output specifications
    
    Args:
        support_agent: The Senior Support Representative agent
        support_quality_assurance_agent: The QA Specialist agent
        docs_scrape_tool: The web scraping tool for documentation
        
    Returns:
        tuple: A tuple containing (inquiry_resolution, quality_assurance_review) tasks
    """
    
    # Task 1: Resolve customer inquiry
    # This task uses the docs_scrape_tool to provide comprehensive support
    inquiry_resolution = Task(
        description=(
            "{customer} just reached out with a super important ask:\n"
            "{inquiry}\n\n"
            "{person} from {customer} is the one that reached out. "
            "Make sure to use everything you know "
            "to provide the best support possible."
            "You must strive to provide a complete "
            "and accurate response to the customer's inquiry."
        ),
        expected_output=(
            "A detailed, informative response to the "
            "customer's inquiry that addresses "
            "all aspects of their question.\n"
            "The response should include references "
            "to everything you used to find the answer, "
            "including external data or solutions. "
            "Ensure the answer is complete, "
            "leaving no questions unanswered, and maintain a helpful and friendly "
            "tone throughout."
        ),
        tools=[docs_scrape_tool],  # Tool assigned at task level
        agent=support_agent,
    )
    
    # Task 2: Quality assurance review
    # This task doesn't use any tools - it only reviews the work of the support agent
    quality_assurance_review = Task(
        description=(
            "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
            "Ensure that the answer is comprehensive, accurate, and adheres to the "
            "high-quality standards expected for customer support.\n"
            "Verify that all parts of the customer's inquiry "
            "have been addressed "
            "thoroughly, with a helpful and friendly tone.\n"
            "Check for references and sources used to "
            "find the information, "
            "ensuring the response is well-supported and "
            "leaves no questions unanswered."
        ),
        expected_output=(
            "A final, detailed, and informative response "
            "ready to be sent to the customer.\n"
            "This response should fully address the "
            "customer's inquiry, incorporating all "
            "relevant feedback and improvements.\n"
            "Don't be too formal, we are a chill and cool company "
            "but maintain a professional and friendly tone throughout."
        ),
        agent=support_quality_assurance_agent,
    )
    
    return inquiry_resolution, quality_assurance_review


def create_crew(agents, tasks):
    """
    Create the crew of agents to work on customer support tasks.
    
    This function demonstrates:
    - Memory: Setting memory=True enables context retention across interactions
    - Crew orchestration and task management
    
    Args:
        agents: List of agents (support_agent, support_quality_assurance_agent)
        tasks: List of tasks (inquiry_resolution, quality_assurance_review)
        
    Returns:
        Crew: A configured crew ready to execute tasks
    """
    
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True,
        memory=True  # Enable memory for context retention
    )
    
    return crew


def run_customer_support(customer="DeepLearningAI", person="Andrew Ng", 
                        inquiry="I need help with setting up a Crew and kicking it off, specifically how can I add memory to my crew? Can you provide guidance?"):
    """
    Execute the complete customer support automation process.
    
    This function demonstrates the complete workflow of:
    - Agent creation and configuration
    - Tool setup and integration
    - Task execution and workflow
    - Quality assurance and review process
    
    Args:
        customer (str): The customer company name
        person (str): The person from the customer company
        inquiry (str): The customer's inquiry or question
        
    Returns:
        CrewOutput: The result of the crew execution
    """
    
    # Set up environment
    setup_environment()
    
    # Create agents
    support_agent, support_quality_assurance_agent = create_agents()
    
    # Set up tools
    docs_scrape_tool = setup_tools()
    
    # Create tasks
    inquiry_resolution, quality_assurance_review = create_tasks(
        support_agent, support_quality_assurance_agent, docs_scrape_tool
    )
    
    # Create crew
    crew = create_crew(
        [support_agent, support_quality_assurance_agent],
        [inquiry_resolution, quality_assurance_review]
    )
    
    # Prepare inputs for the crew
    inputs = {
        "customer": customer,
        "person": person,
        "inquiry": inquiry
    }
    
    # Execute the crew
    print(f"Starting customer support for {customer}...")
    print(f"Person: {person}")
    print(f"Inquiry: {inquiry}")
    print("\nExecuting crew...")
    
    result = crew.kickoff(inputs=inputs)
    
    return result


def demonstrate_guardrails():
    """
    Demonstrate how guardrails work in the customer support system.
    
    This function explains how the system ensures that:
    - Agents stay within their defined roles and responsibilities
    - Responses are appropriate and professional
    - Quality standards are maintained
    """
    print("\n" + "="*60)
    print("GUARDRAILS IN ACTION")
    print("="*60)
    print("""
The customer support system includes several guardrails:
    
1. Role-based Access: Each agent has a specific role and cannot exceed their scope
2. Quality Assurance: A dedicated QA agent reviews all responses
3. Tool Limitations: Agents can only use approved tools and resources
4. Response Guidelines: Clear expectations for response quality and tone
5. Memory Management: Context is maintained but controlled
    
These guardrails ensure that customer interactions remain:
- Professional and helpful
- Accurate and complete
- Within company guidelines
- Consistent with brand voice
    """)


def main():
    """
    Main function to demonstrate the customer support automation system.
    """
    print("🚀 L3: Multi-agent Customer Support Automation")
    print("=" * 60)
    
    try:
        # Run the customer support process
        result = run_customer_support()
        
        # Display results
        print("\n" + "="*60)
        print("CUSTOMER SUPPORT COMPLETED!")
        print("="*60)
        print(f"Result type: {type(result)}")
        print(f"Result content:\n{result}")
        
        # Demonstrate guardrails
        demonstrate_guardrails()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        print("Please check your API keys and environment setup.")


if __name__ == "__main__":
    main()
