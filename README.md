# TechxchangeHackathonNeuralnexis Crew

Welcome to the TechxchangeHackathonNeuralnexis Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Configure your AWS Bedrock credentials in the `.env` file**

The project now uses AWS Bedrock instead of Watson LLM. You need to configure the following environment variables:

```bash
# AWS Bedrock Configuration
AWS_REGION=us-east-1
BEDROCK_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0

# AWS Credentials (set via AWS CLI, IAM roles, or environment variables)
# AWS_ACCESS_KEY_ID=your_access_key_here
# AWS_SECRET_ACCESS_KEY=your_secret_key_here

# Other required API keys
SERPER_API_KEY=your_serper_api_key_here
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_user_agent

# Email Configuration (for reminders)
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**Available Bedrock Models:**
- `anthropic.claude-3-5-sonnet-20241022-v2:0` (default)
- `anthropic.claude-3-haiku-20240307-v1:0`
- `anthropic.claude-3-opus-20240229-v1:0`
- `meta.llama-3-2-70b-instruct-v1:0`
- `meta.llama-3-2-11b-instruct-v1:0`
- `amazon.titan-text-express-v1`

**Email Setup for Reminders:**
1. For Gmail: Enable 2-factor authentication and create an App Password
2. Use the App Password (not your regular password) in EMAIL_PASSWORD
3. For other email providers, adjust SMTP_SERVER and SMTP_PORT accordingly

- Modify `src/techxchange_hackathon_neuralnexis/config/agents.yaml` to define your agents
- Modify `src/techxchange_hackathon_neuralnexis/config/tasks.yaml` to define your tasks
- Modify `src/techxchange_hackathon_neuralnexis/crew.py` to add your own logic, tools and specific args
- Modify `src/techxchange_hackathon_neuralnexis/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the TechXchange_Hackathon_NeuralNexis Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The TechXchange_Hackathon_NeuralNexis Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the TechxchangeHackathonNeuralnexis Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
