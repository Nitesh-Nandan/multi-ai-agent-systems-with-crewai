#!/usr/bin/env python3
"""
L4: Tools for a Customer Outreach Campaign

This module demonstrates advanced tool usage in crewAI for customer outreach campaigns.
It focuses on three key elements of Tools: Versatility, Fault Tolerance, and Caching.

Key Concepts Covered:
- Tool integration and configuration
- Custom tool creation using BaseTool
- Tool assignment at agent and task levels
- Search and data gathering tools
- Sentiment analysis for communication optimization
- Lead profiling and personalized outreach

Author: CrewAI Course
Date: 2024
"""

# Standard library imports
import os
import warnings

# Third-party imports
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool, BaseTool

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
    
    # Set the OpenAI model to use
    os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
    
    # Get and set Serper API key for search functionality
    serper_api_key = get_serper_api_key()
    os.environ["SERPER_API_KEY"] = serper_api_key
    
    # Verify OpenAI API key is available
    openai_api_key = get_openai_api_key()
    if not openai_api_key:
        raise ValueError("OpenAI API key not found")
    
    print("Environment setup completed successfully!")
    print(f"OpenAI API Key: {openai_api_key[:20]}...")
    print(f"Serper API Key: {serper_api_key[:20]}...")
    
    return openai_api_key, serper_api_key


def create_agents():
    """
    Create the AI agents for customer outreach campaigns.
    
    This function creates specialized agents for:
    - Sales representation and lead identification
    - Lead nurturing and personalized communication
    
    Returns:
        tuple: A tuple containing (sales_rep_agent, lead_sales_rep_agent)
    """
    
    # Agent 1: Sales Representative
    # This agent identifies high-value leads and conducts initial research
    sales_rep_agent = Agent(
        role="Sales Representative",
        goal="Identify high-value leads that match "
             "our ideal customer profile",
        backstory=(
            "As a part of the dynamic sales team at CrewAI, "
            "your mission is to scour "
            "the digital landscape for potential leads. "
            "Armed with cutting-edge tools "
            "and a strategic mindset, you analyze data, "
            "trends, and interactions to "
            "unearth opportunities that others might overlook. "
            "Your work is crucial in paving the way "
            "for meaningful engagements and driving the company's growth."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    # Agent 2: Lead Sales Representative
    # This agent nurtures leads with personalized communications
    lead_sales_rep_agent = Agent(
        role="Lead Sales Representative",
        goal="Nurture leads with personalized, compelling communications",
        backstory=(
            "Within the vibrant ecosystem of CrewAI's sales department, "
            "you stand out as the bridge between potential clients "
            "and the solutions they need."
            "By creating engaging, personalized messages, "
            "you not only inform leads about our offerings "
            "but also make them feel seen and heard."
            "Your role is pivotal in converting interest "
            "into action, guiding leads through the journey "
            "from curiosity to commitment."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    return sales_rep_agent, lead_sales_rep_agent


def setup_tools():
    """
    Set up the tools that agents can use for customer outreach.
    
    This function demonstrates:
    - Built-in crewAI tools for file and directory operations
    - Search tools for gathering information
    - Custom tool creation for specialized functionality
    
    Returns:
        tuple: A tuple containing all configured tools
    """
    
    # Built-in crewAI Tools
    # These tools provide versatile file and directory access capabilities
    directory_read_tool = DirectoryReadTool(directory='./instructions')
    file_read_tool = FileReadTool()
    search_tool = SerperDevTool()
    
    # Custom Tool: Sentiment Analysis
    # This demonstrates how to create custom tools using crewAI's BaseTool class
    class SentimentAnalysisTool(BaseTool):
        """
        Custom tool for analyzing text sentiment to ensure positive communication.
        
        This tool demonstrates custom tool creation and can be extended
        with more sophisticated sentiment analysis logic.
        """
        name: str = "Sentiment Analysis Tool"
        description: str = ("Analyzes the sentiment of text "
             "to ensure positive and engaging communication.")
        
        def _run(self, text: str) -> str:
            """
            Analyze the sentiment of the provided text.
            
            Args:
                text (str): The text to analyze
                
            Returns:
                str: The sentiment analysis result
                
            Note:
                For simplicity and classroom purposes, this tool returns 'positive'
                for every text. In production, you would integrate with a proper
                sentiment analysis service or model.
            """
            # Your custom code tool goes here
            # This is where you would implement actual sentiment analysis
            return "positive"
    
    # Instantiate the custom sentiment analysis tool
    sentiment_analysis_tool = SentimentAnalysisTool()
    
    print("Tools configured successfully!")
    print("Available tools:")
    print("- Directory Read Tool: For reading directory contents")
    print("- File Read Tool: For reading individual files")
    print("- Search Tool: For web search capabilities")
    print("- Sentiment Analysis Tool: Custom tool for sentiment analysis")
    
    return directory_read_tool, file_read_tool, search_tool, sentiment_analysis_tool


def create_tasks(sales_rep_agent, lead_sales_rep_agent, tools):
    """
    Create the tasks for customer outreach campaigns.
    
    This function demonstrates:
    - Tool assignment at the task level
    - Task dependencies and workflow
    - Expected output specifications
    
    Args:
        sales_rep_agent: The Sales Representative agent
        lead_sales_rep_agent: The Lead Sales Representative agent
        tools: Tuple of available tools
        
    Returns:
        tuple: A tuple containing (lead_profiling_task, personalized_outreach_task)
    """
    
    # Unpack tools for easier access
    directory_read_tool, file_read_tool, search_tool, sentiment_analysis_tool = tools
    
    # Task 1: Lead Profiling
    # This task uses crewAI tools to gather comprehensive lead information
    lead_profiling_task = Task(
        description=(
            "Conduct an in-depth analysis of {lead_name}, "
            "a company in the {industry} sector "
            "that recently showed interest in our solutions. "
            "Utilize all available data sources "
            "to compile a detailed profile, "
            "focusing on key decision-makers, recent business "
            "developments, and potential needs "
            "that align with our offerings. "
            "This task is crucial for tailoring "
            "our engagement strategy effectively.\n"
            "Don't make assumptions and "
            "only use information you absolutely sure about."
        ),
        expected_output=(
            "A comprehensive report on {lead_name}, "
            "including company background, "
            "key personnel, recent milestones, and identified needs. "
            "Highlight potential areas where "
            "our solutions can provide value, "
            "and suggest personalized engagement strategies."
        ),
        tools=[directory_read_tool, file_read_tool, search_tool],
        agent=sales_rep_agent,
    )
    
    # Task 2: Personalized Outreach
    # This task uses the custom sentiment analysis tool and search capabilities
    personalized_outreach_task = Task(
        description=(
            "Using the insights gathered from "
            "the lead profiling report on {lead_name}, "
            "craft a personalized outreach campaign "
            "aimed at {key_decision_maker}, "
            "the {position} of {lead_name}. "
            "The campaign should address their recent {milestone} "
            "and how our solutions can support their goals. "
            "Your communication must resonate "
            "with {lead_name}'s company culture and values, "
            "demonstrating a deep understanding of "
            "their business and needs.\n"
            "Don't make assumptions and only "
            "use information you absolutely sure about."
        ),
        expected_output=(
            "A series of personalized email drafts "
            "tailored to {lead_name}, "
            "specifically targeting {key_decision_maker}."
            "Each draft should include "
            "a compelling narrative that connects our solutions "
            "with their recent achievements and future goals. "
            "Ensure the tone is engaging, professional, "
            "and aligned with {lead_name}'s corporate identity."
        ),
        tools=[sentiment_analysis_tool, search_tool],
        agent=lead_sales_rep_agent,
    )
    
    return lead_profiling_task, personalized_outreach_task


def create_crew(agents, tasks):
    """
    Create the crew of agents to work on customer outreach tasks.
    
    This function demonstrates:
    - Crew orchestration with multiple agents
    - Memory-enabled context retention
    - Verbose logging for detailed execution tracking
    
    Args:
        agents: List of agents (sales_rep_agent, lead_sales_rep_agent)
        tasks: List of tasks (lead_profiling_task, personalized_outreach_task)
        
    Returns:
        Crew: A configured crew ready to execute tasks
    """
    
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=2,  # Detailed logging for better understanding
        memory=True  # Enable memory for context retention across tasks
    )
    
    return crew


def run_customer_outreach(lead_name="DeepLearningAI", industry="Online Learning Platform",
                         key_decision_maker="Andrew Ng", position="CEO", milestone="product launch"):
    """
    Execute the complete customer outreach campaign process.
    
    This function demonstrates the complete workflow of:
    - Lead profiling and research
    - Personalized outreach campaign creation
    - Tool integration and utilization
    - Multi-agent collaboration
    
    Args:
        lead_name (str): The name of the target company
        industry (str): The industry sector of the company
        key_decision_maker (str): The key person to target
        position (str): The position of the key decision maker
        milestone (str): Recent milestone to reference in outreach
        
    Returns:
        CrewOutput: The result of the crew execution
    """
    
    # Set up environment
    setup_environment()
    
    # Create agents
    sales_rep_agent, lead_sales_rep_agent = create_agents()
    
    # Set up tools
    tools = setup_tools()
    
    # Create tasks
    lead_profiling_task, personalized_outreach_task = create_tasks(
        sales_rep_agent, lead_sales_rep_agent, tools
    )
    
    # Create crew
    crew = create_crew(
        [sales_rep_agent, lead_sales_rep_agent],
        [lead_profiling_task, personalized_outreach_task]
    )
    
    # Prepare inputs for the crew
    inputs = {
        "lead_name": lead_name,
        "industry": industry,
        "key_decision_maker": key_decision_maker,
        "position": position,
        "milestone": milestone
    }
    
    # Execute the crew
    print(f"Starting customer outreach campaign for {lead_name}...")
    print(f"Industry: {industry}")
    print(f"Target: {key_decision_maker} ({position})")
    print(f"Milestone: {milestone}")
    print("\nExecuting crew...")
    
    result = crew.kickoff(inputs=inputs)
    
    return result


def demonstrate_tool_features():
    """
    Demonstrate the key features of tools in crewAI.
    
    This function explains the three key elements of tools:
    - Versatility: Tools can be used across different agents and tasks
    - Fault Tolerance: Tools handle errors gracefully
    - Caching: Tools can cache results for efficiency
    """
    print("\n" + "="*60)
    print("TOOL FEATURES IN CREWAI")
    print("="*60)
    print("""
1. VERSATILITY:
   - Tools can be assigned at the agent level (available for all tasks)
   - Tools can be assigned at the task level (specific to that task)
   - Task-level tools override agent-level tools
   - Multiple tools can be combined for complex operations

2. FAULT TOLERANCE:
   - Tools handle API failures gracefully
   - Fallback mechanisms for when tools are unavailable
   - Error logging and reporting for debugging
   - Retry mechanisms for transient failures

3. CACHING:
   - Tool results can be cached to avoid redundant API calls
   - Cache invalidation strategies for fresh data
   - Memory-efficient storage of tool outputs
   - Performance optimization for repeated operations

4. CUSTOM TOOL CREATION:
   - Extend BaseTool class for specialized functionality
   - Implement _run method for custom logic
   - Add validation and error handling
   - Integrate with external services and APIs
    """)


def main():
    """
    Main function to demonstrate the customer outreach campaign system.
    """
    print("🚀 L4: Tools for a Customer Outreach Campaign")
    print("=" * 60)
    
    try:
        # Run the customer outreach process
        result = run_customer_outreach()
        
        # Display results
        print("\n" + "="*60)
        print("CUSTOMER OUTREACH COMPLETED!")
        print("="*60)
        print(f"Result type: {type(result)}")
        print(f"Result content:\n{result}")
        
        # Demonstrate tool features
        demonstrate_tool_features()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        print("Please check your API keys and environment setup.")


if __name__ == "__main__":
    main()
