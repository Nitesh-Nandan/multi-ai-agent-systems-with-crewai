#!/usr/bin/env python3
"""
L2: Create Agents to Research and Write an Article

This module demonstrates the foundational concepts of multi-agent systems using the crewAI framework.
It shows how to create a team of AI agents that work together to research, write, and edit articles.

Key Concepts Covered:
- Agent creation with roles, goals, and backstories
- Task definition and management
- Crew orchestration
- Sequential task execution
- Different LLM integration options

Author: CrewAI Course
Date: 2024
"""

# Standard library imports
import os
import warnings

# Third-party imports
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')


def setup_environment():
    """
    Set up the environment variables and API keys.
    
    This function loads environment variables from a .env file and sets up
    the OpenAI API configuration for the agents to use.
    """
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
    Create the AI agents for the article writing process.
    
    Returns:
        tuple: A tuple containing (planner, writer, editor) agents
        
    Note:
        The benefit of using multiple strings vs triple quote docstrings is that
        it avoids adding whitespaces and newline characters, making it better
        formatted to be passed to the LLM.
    """
    
    # Agent 1: Content Planner
    # This agent is responsible for researching and planning the article structure
    planner = Agent(
        role="Content Planner",
        goal="Plan engaging and factually accurate content on {topic}",
        backstory="You're working on planning a blog article "
                  "about the topic: {topic}."
                  "You collect information that helps the "
                  "audience learn something "
                  "and make informed decisions. "
                  "Your work is the basis for "
                  "the Content Writer to write an article on this topic.",
        allow_delegation=False,
        verbose=True
    )
    
    # Agent 2: Content Writer
    # This agent writes the actual article based on the planner's outline
    writer = Agent(
        role="Content Writer",
        goal="Write insightful and factually accurate "
             "opinion piece about the topic: {topic}",
        backstory="You're working on a writing "
                  "a new opinion piece about the topic: {topic}. "
                  "You base your writing on the work of "
                  "the Content Planner, who provides an outline "
                  "and relevant context about the topic. "
                  "You follow the main objectives and "
                  "direction of the outline, "
                  "as provide by the Content Planner. "
                  "You also provide objective and impartial insights "
                  "and back them up with information "
                  "provide by the Content Planner. "
                  "You acknowledge in your opinion piece "
                  "when your statements are opinions "
                  "as opposed to objective statements.",
        allow_delegation=False,
        verbose=True
    )
    
    # Agent 3: Editor
    # This agent reviews and refines the written article
    editor = Agent(
        role="Editor",
        goal="Edit a given blog post to align with "
             "the writing style of the organization. ",
        backstory="You are an editor who receives a blog post "
                  "from the Content Writer. "
                  "Your goal is to review the blog post "
                  "to ensure that it follows journalistic best practices,"
                  "provides balanced viewpoints "
                  "when providing opinions or assertions, "
                  "and also avoids major controversial topics "
                  "or opinions when possible.",
        allow_delegation=False,
        verbose=True
    )
    
    return planner, writer, editor


def create_tasks(planner, writer, editor):
    """
    Create the tasks for the article writing process.
    
    Args:
        planner: The Content Planner agent
        writer: The Content Writer agent
        editor: The Editor agent
        
    Returns:
        tuple: A tuple containing (plan, write, edit) tasks
        
    Note:
        Tasks are performed sequentially and are dependent on each other,
        so the order in the list matters.
    """
    
    # Task 1: Plan the article content
    plan = Task(
        description=(
            "1. Prioritize the latest trends, key players, "
                "and noteworthy news on {topic}.\n"
            "2. Identify the target audience, considering "
                "their interests and pain points.\n"
            "3. Develop a detailed content outline including "
                "an introduction, key points, and a call to action.\n"
            "4. Include SEO keywords and relevant data or sources."
        ),
        expected_output="A comprehensive content plan document "
            "with an outline, audience analysis, "
            "SEO keywords, and resources.",
        agent=planner,
    )
    
    # Task 2: Write the article
    write = Task(
        description=(
            "1. Use the content plan to craft a compelling "
                "blog post on {topic}.\n"
            "2. Incorporate SEO keywords naturally.\n"
            "3. Sections/Subtitles are properly named "
                "in an engaging manner.\n"
            "4. Ensure the post is structured with an "
                "engaging introduction, insightful body, "
                "and a summarizing conclusion.\n"
            "5. Proofread for grammatical errors and "
                "alignment with the brand's voice.\n"
        ),
        expected_output="A well-written blog post "
            "in markdown format, ready for publication, "
            "each section should have 2 or 3 paragraphs.",
        agent=writer,
    )
    
    # Task 3: Edit and refine the article
    edit = Task(
        description=("Proofread the given blog post for "
                     "grammatical errors and "
                     "alignment with the brand's voice."),
        expected_output="A well-written blog post in markdown format, "
                        "ready for publication, "
                        "each section should have 2 or 3 paragraphs.",
        agent=editor
    )
    
    return plan, write, edit


def create_crew(agents, tasks):
    """
    Create the crew of agents to work on the article writing tasks.
    
    Args:
        agents: List of agents (planner, writer, editor)
        tasks: List of tasks (plan, write, edit)
        
    Returns:
        Crew: A configured crew ready to execute tasks
        
    Note:
        verbose=2 allows you to see all the logs of the execution.
        For this simple example, tasks are performed sequentially.
    """
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True
    )
    return crew


def run_article_creation(topic="Artificial Intelligence"):
    """
    Execute the complete article creation process.
    
    Args:
        topic (str): The topic for the article to be written about
        
    Returns:
        CrewOutput: The result of the crew execution
        
    Note:
        LLMs can provide different outputs for the same input, so results
        may vary between executions.
    """
    # Set up environment
    setup_environment()
    
    # Create agents
    planner, writer, editor = create_agents()
    
    # Create tasks
    plan, write, edit = create_tasks(planner, writer, editor)
    
    # Create crew
    crew = create_crew([planner, writer, editor], [plan, write, edit])
    
    # Execute the crew
    print(f"Starting article creation for topic: {topic}")
    result = crew.kickoff(inputs={"topic": topic})
    
    return result


def demonstrate_other_llm_options():
    """
    Demonstrate how to use different LLM providers with crewAI.
    
    This function shows examples of integrating with various LLM services
    including Hugging Face, Mistral, and Cohere.
    """
    print("\n" + "="*60)
    print("OTHER POPULAR MODELS AS LLM FOR YOUR AGENTS")
    print("="*60)
    
    # Example 1: Hugging Face
    print("\n1. Hugging Face (HuggingFaceHub endpoint):")
    print("""
from langchain_community.llms import HuggingFaceHub

llm = HuggingFaceHub(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token="<HF_TOKEN_HERE>",
    task="text-generation",
)

# You will pass "llm" to your agent function
""")
    
    # Example 2: Mistral API
    print("\n2. Mistral API:")
    print("""
OPENAI_API_KEY=your-mistral-api-key
OPENAI_API_BASE=https://api.mistral.ai/v1
OPENAI_MODEL_NAME="mistral-small"
""")
    
    # Example 3: Cohere
    print("\n3. Cohere:")
    print("""
from langchain_community.chat_models import ChatCohere
# Initialize language model
os.environ["COHERE_API_KEY"] = "your-cohere-api-key"
llm = ChatCohere()

# You will pass "llm" to your agent function
""")
    
    print("\nFor using Llama locally with Ollama and more, checkout the crewAI documentation on [Connecting to any LLM](https://docs.crewai.com/how-to/LLM-Connections/).")


def main():
    """
    Main function to demonstrate the article creation process.
    """
    print("🚀 L2: Create Agents to Research and Write an Article")
    print("=" * 60)
    
    try:
        # Run the article creation process
        result = run_article_creation("Artificial Intelligence")
        
        # Display results
        print("\n" + "="*60)
        print("ARTICLE CREATION COMPLETED!")
        print("="*60)
        print(f"Result type: {type(result)}")
        print(f"Result content:\n{result}")
        
        # Show other LLM options
        demonstrate_other_llm_options()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        print("Please check your API keys and environment setup.")


if __name__ == "__main__":
    run_article_creation()
