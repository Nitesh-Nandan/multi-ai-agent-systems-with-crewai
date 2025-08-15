# Multi-AI Agent Systems with CrewAI - Python Implementation

This directory contains comprehensive Python implementations of the CrewAI course lessons, converted from Jupyter notebooks for better learning and future reference.

## 📚 Overview

These Python files demonstrate the complete implementation of multi-agent systems using the CrewAI framework. Each file is self-contained, well-documented, and includes comprehensive examples that can be run independently or used as reference material.

## 🗂️ File Structure

### Core Lesson Files

1. **`L2_research_write_article.py`** - Foundational multi-agent concepts
2. **`L3_customer_support.py`** - Customer support automation with advanced agent features
3. **`L4_tools_customer_outreach.py`** - Advanced tool integration and custom tool creation
4. **`L5_tasks_event_planning.py`** - Advanced task features and automation

### Supporting Files

- **`utils.py`** - Utility functions and helper classes
- **`README.md`** - This comprehensive guide

## 🚀 Getting Started

### Prerequisites

1. **Python Environment**: Python 3.8+ recommended
2. **Dependencies**: Install required packages using the project's dependency manager
3. **API Keys**: Set up your OpenAI and Serper API keys

### Installation

```bash
# Navigate to the project directory
cd multi-ai-agent-systems-with-crewai

# Install dependencies (using uv or pip)
uv sync
# or
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the project root with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

## 📖 Lesson Details

### L2: Research and Article Writing (`L2_research_write_article.py`)

**Key Concepts:**
- Basic agent creation with roles, goals, and backstories
- Task definition and management
- Crew orchestration
- Sequential task execution

**What You'll Learn:**
- How to create AI agents for content planning, writing, and editing
- Task workflow design and execution
- Crew management and coordination
- Different LLM integration options

**Usage:**
```python
from L2_research_write_article import run_article_creation

# Run with default topic (Artificial Intelligence)
result = run_article_creation()

# Run with custom topic
result = run_article_creation("Machine Learning in Healthcare")
```

### L3: Customer Support Automation (`L3_customer_support.py`)

**Key Concepts:**
- Role playing and character development
- Tool integration and utilization
- Agent cooperation and delegation
- Memory and context retention
- Guardrails for controlled responses

**What You'll Learn:**
- How to create specialized support agents
- Tool integration for enhanced capabilities
- Quality assurance workflows
- Memory management for context retention

**Usage:**
```python
from L3_customer_support import run_customer_support

# Run with default parameters
result = run_customer_support()

# Run with custom parameters
result = run_customer_support(
    customer="TechCorp",
    person="Sarah Johnson",
    inquiry="How do I integrate CrewAI with my existing workflow?"
)
```

### L4: Tools for Customer Outreach (`L4_tools_customer_outreach.py`)

**Key Concepts:**
- Tool versatility and configuration
- Custom tool creation using BaseTool
- Tool assignment strategies
- Fault tolerance and caching

**What You'll Learn:**
- How to create custom tools for specialized functionality
- Tool integration at agent and task levels
- Search and data gathering capabilities
- Sentiment analysis for communication optimization

**Usage:**
```python
from L4_tools_customer_outreach import run_customer_outreach

# Run with default parameters
result = run_customer_outreach()

# Run with custom parameters
result = run_customer_outreach(
    lead_name="InnovationTech",
    industry="Software Development",
    key_decision_maker="Michael Chen",
    position="CTO",
    milestone="Series A funding"
)
```

### L5: Event Planning Automation (`L5_tasks_event_planning.py`)

**Key Concepts:**
- Advanced task configuration
- Human input integration
- Structured output with Pydantic models
- File output generation
- Asynchronous task execution

**What You'll Learn:**
- How to create tasks that require human approval
- Structured data output and validation
- File generation in various formats
- Parallel task processing for efficiency

**Usage:**
```python
from L5_tasks_event_planning import run_event_planning

# Run with default parameters
result = run_event_planning()

# Run with custom parameters
result = run_event_planning(
    event_topic="AI Ethics Conference",
    event_city="New York",
    expected_participants=300,
    budget=15000
)
```

## 🛠️ Utility Functions (`utils.py`)

The `utils.py` file contains helper functions and classes that support the main lesson implementations:

- **API Key Management**: Functions to retrieve and validate API keys
- **SKU Findability System**: Example data management classes
- **Helper Functions**: Utility functions for common operations

## 🔧 Running the Examples

### Individual Execution

Each Python file can be run independently:

```bash
# Run L2 (Article Writing)
python src/L2_research_write_article.py

# Run L3 (Customer Support)
python src/L3_customer_support.py

# Run L4 (Customer Outreach)
python src/L4_tools_customer_outreach.py

# Run L5 (Event Planning)
python src/L5_tasks_event_planning.py
```

### Interactive Usage

Import and use functions in your own code:

```python
# Import specific functions
from L2_research_write_article import create_agents, create_tasks

# Create agents and tasks
planner, writer, editor = create_agents()
plan_task, write_task, edit_task = create_tasks(planner, writer, editor)

# Use them in your own crew
from crewai import Crew
crew = Crew(agents=[planner, writer, editor], tasks=[plan_task, write_task, edit_task])
```

## 📚 Learning Path

### Beginner Level
1. Start with **L2** to understand basic concepts
2. Study agent creation and task definition
3. Run examples and experiment with parameters

### Intermediate Level
1. Move to **L3** for advanced agent features
2. Explore tool integration and memory
3. Understand agent cooperation patterns

### Advanced Level
1. Study **L4** for custom tool creation
2. Master **L5** for advanced task features
3. Combine concepts from all lessons

## 🎯 Best Practices

### Code Organization
- Each lesson is self-contained with clear separation of concerns
- Functions are well-documented with docstrings
- Error handling and validation are included
- Configuration is separated from logic

### Agent Design
- Define clear roles, goals, and backstories
- Use appropriate delegation settings
- Implement proper tool assignments
- Consider memory requirements

### Task Configuration
- Set clear expected outputs
- Use appropriate task dependencies
- Implement human input when needed
- Structure outputs for consistency

## 🔍 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure your `.env` file is properly configured
   - Check that API keys are valid and have sufficient credits

2. **Import Errors**
   - Verify all dependencies are installed
   - Check Python path and virtual environment

3. **Tool Errors**
   - Ensure tools are properly configured
   - Check API rate limits and quotas

### Debug Mode

Most functions include verbose logging. Enable it by setting `verbose=True` in agent and crew configurations.

## 📖 Additional Resources

- **CrewAI Documentation**: [https://docs.crewai.com](https://docs.crewai.com)
- **CrewAI GitHub**: [https://github.com/joaomdmoura/crewAI](https://github.com/joaomdmoura/crewAI)
- **LangChain Community**: [https://github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain)

## 🤝 Contributing

These implementations are designed for learning and reference. Feel free to:

- Modify parameters and experiment with different scenarios
- Extend functionality with additional tools and agents
- Create new examples based on the patterns shown
- Share improvements and additional use cases


---

**Happy Learning! 🚀**

Use these Python files to deepen your understanding of multi-agent systems and build upon the concepts for your own projects.
