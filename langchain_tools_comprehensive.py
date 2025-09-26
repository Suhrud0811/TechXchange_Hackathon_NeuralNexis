#!/usr/bin/env python3
"""
Mental Health Support Crew with LangChain tools integration
"""

from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import SerperDevTool
from langchain.tools import DuckDuckGoSearchRun, WikipediaQueryRun, YouTubeSearchTool
from langchain_community.utilities import WikipediaAPIWrapper
import os
import smtplib
import json
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class EmailReminderTool:
    """Custom tool for sending email reminders"""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")
    
    def send_reminder_email(self, to_email: str, subject: str, message: str, task_details: dict = None) -> str:
        """Send an email reminder with task details"""
        try:
            if not self.email or not self.password:
                return "Email configuration missing. Please set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables."
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Create HTML body
            html_body = f"""
            <html>
            <body>
                <h2>🎯 Task Reminder</h2>
                <p>{message}</p>
                
                {self._format_task_details(task_details) if task_details else ''}
                
                <hr>
                <p><small>This is an automated reminder from your Mental Health Support Crew.</small></p>
                <p><small>Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            text = msg.as_string()
            server.sendmail(self.email, to_email, text)
            server.quit()
            
            return f"Email reminder sent successfully to {to_email}"
            
        except Exception as e:
            return f"Failed to send email: {str(e)}"
    
    def _format_task_details(self, task_details: dict) -> str:
        """Format task details for HTML email"""
        if not task_details:
            return ""
        
        html = "<h3>📋 Task Details:</h3><ul>"
        
        if 'name' in task_details:
            html += f"<li><strong>Task:</strong> {task_details['name']}</li>"
        if 'time_hours' in task_details:
            html += f"<li><strong>Estimated Time:</strong> {task_details['time_hours']} hours</li>"
        if 'priority_score' in task_details:
            html += f"<li><strong>Priority Score:</strong> {task_details['priority_score']}</li>"
        if 'impact_pct' in task_details:
            html += f"<li><strong>Impact:</strong> {task_details['impact_pct']}%</li>"
        if 'rationale' in task_details:
            html += f"<li><strong>Why Important:</strong> {task_details['rationale']}</li>"
        
        html += "</ul>"
        return html

class MentalHealthSupportCrew:
    """Mental Health Support Crew with LangChain tools integration"""

    def _get_bedrock_llm(self) -> LLM:
        """Configure and return AWS Bedrock LLM"""
        model = os.getenv("BEDROCK_MODEL", "anthropic.claude-3-5-sonnet-20241022-v2:0")
        region = os.getenv("AWS_REGION", "us-east-1")
        
        # Configure Bedrock LLM
        bedrock_llm = LLM(
            model=model,
            config={
                "region_name": region,
                "temperature": 0.7,
                "max_tokens": 512,
                "top_p": 0.9,
                "top_k": 50,
                "stop_sequences": []
            }
        )
        
        return bedrock_llm

    def create_comprehensive_agent(self):
        """Create a single comprehensive agent that handles all aspects"""
        email_tool = EmailReminderTool()
        tools = [
            DuckDuckGoSearchRun(),
            WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
            YouTubeSearchTool(),
            SerperDevTool(),
            email_tool
        ]
        
        return Agent(
            role="Comprehensive Mental Health & Goal Planning Specialist",
            goal="Provide complete mental health support, goal planning, and execution monitoring with email reminders",
            backstory="""You're a professional Therapist/Goal Planner with comprehensive capabilities to:
            - Analyze user conversations to identify mental health challenges
            - Conduct research using multiple sources for relevant resources and solutions
            - Break complex goals into <=7 outcome-based tasks with dependencies
            - Estimate realistic time requirements with 0.25h granularity
            - Assign impact percentages considering mental health and therapeutic value
            - Calculate priority scores and create logical task sequences
            - Build day-by-day schedules respecting capacity and mental health needs
            - Create email reminders and suggest adjustments for sustainable execution
            - Send personalized email reminders with task details and mental health considerations
            - Synthesize all findings into actionable, comprehensive reports""",
            llm=self._get_bedrock_llm(),
            verbose=True,
            tools=tools
        )

    def create_requirements_agent(self):
        """Create a requirements gathering agent"""
        return Agent(
            role="Requirements Specialist",
            goal="Gather clear requirements and goals from the user",
            backstory="""You're a professional Therapist/Goal Planner who specializes in gathering requirements from users. 
            You ask thoughtful questions to understand what the user wants to achieve, clarify their needs and objectives, 
            and create a clear summary of their goals and requirements.""",
            llm=self._get_bedrock_llm(),
            verbose=True
        )

    def create_analyst_agent(self):
        """Create a comprehensive analyst agent"""
        tools = [
            DuckDuckGoSearchRun(),
            WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
            YouTubeSearchTool(),
            SerperDevTool()
        ]
        
        return Agent(
            role="Mental Health Support Analyst",
            goal="Create comprehensive analysis, research, and action plans for mental health support",
            backstory="""You're a professional Therapist/Goal Planner with comprehensive capabilities to:
            - Analyze user conversations to identify mental health challenges
            - Conduct research using multiple sources for relevant resources and solutions
            - Create detailed task lists and action plans
            - Synthesize findings into actionable reports with clear recommendations""",
            llm=self._get_bedrock_llm(),
            verbose=True,
            tools=tools
        )

    def create_goal_planner_agent(self):
        """Create a goal planning agent that breaks down goals into structured tasks"""
        return Agent(
            role="Goal Planning Specialist",
            goal="Break down user goals into structured, actionable tasks with dependencies and assumptions",
            backstory="""You're a professional Goal Planning Specialist who excels at:
            - Breaking complex goals into <=7 outcome-based tasks
            - Identifying task dependencies and relationships
            - Making realistic assumptions about requirements and constraints
            - Creating structured task plans with clear deliverables
            - Ensuring tasks are specific, measurable, and achievable""",
            llm=self._get_bedrock_llm(),
            verbose=True
        )

    def create_time_analyzer_agent(self):
        """Create a time estimation agent"""
        return Agent(
            role="Time Estimation Specialist",
            goal="Provide accurate time estimates for tasks with 0.25h granularity",
            backstory="""You're a Time Estimation Specialist who:
            - Estimates realistic time requirements for tasks
            - Prefers smaller, manageable time chunks (0.25h granularity)
            - Considers task complexity, dependencies, and user capabilities
            - Provides conservative but achievable time estimates
            - Accounts for potential obstacles and learning curves""",
            llm=self._get_bedrock_llm(),
            verbose=True
        )

    def create_impact_agent(self):
        """Create an impact assessment agent"""
        return Agent(
            role="Impact Assessment Specialist",
            goal="Assign impact percentages to tasks with clear rationale",
            backstory="""You're an Impact Assessment Specialist who:
            - Evaluates the relative importance and impact of each task
            - Assigns impact percentages that total approximately 100%
            - Provides clear, one-line rationale for each impact assessment
            - Considers both short-term and long-term value of tasks
            - Balances immediate needs with strategic goals""",
            llm=self._get_bedrock_llm(),
            verbose=True
        )

    def create_prioritizer_agent(self):
        """Create a task prioritization agent"""
        return Agent(
            role="Task Prioritization Specialist",
            goal="Prioritize tasks based on impact, time, and dependencies",
            backstory="""You're a Task Prioritization Specialist who:
            - Calculates priority scores using impact_pct / max(time_hours, 0.25)
            - Sorts tasks by priority score in descending order
            - Ensures dependencies appear earlier in the sequence
            - Balances high-impact tasks with time constraints
            - Creates logical, executable task sequences""",
            llm=self._get_bedrock_llm(),
            verbose=True
        )

    def create_scheduler_agent(self):
        """Create a scheduling agent"""
        return Agent(
            role="Schedule Planning Specialist",
            goal="Build day-by-day schedules from prioritized tasks respecting capacity and buffer",
            backstory="""You're a Schedule Planning Specialist who:
            - Creates realistic day-by-day schedules from prioritized tasks
            - Respects daily capacity limits and includes buffer time
            - Considers task dependencies and optimal sequencing
            - Identifies when capacity is exceeded and provides warnings
            - Balances workload across available time periods
            - Accounts for weekends, holidays, and personal constraints""",
            llm=self._get_bedrock_llm(),
            verbose=True
        )

    def create_monitor_agent(self):
        """Create a monitoring and reminder agent"""
        return Agent(
            role="Progress Monitoring Specialist",
            goal="Create reminders and suggest adjustments for task execution",
            backstory="""You're a Progress Monitoring Specialist who:
            - Creates timely reminders for today's top priority items
            - Monitors schedule adherence and identifies potential issues
            - Suggests adjustments when capacity is exceeded or delays occur
            - Provides proactive recommendations for schedule optimization
            - Tracks progress and suggests course corrections
            - Ensures realistic expectations and sustainable pacing""",
            llm=self._get_bedrock_llm(),
            verbose=True
        )

    def create_optimized_tasks(self, requirements_agent: Agent, comprehensive_agent: Agent):
        """Create optimized tasks for the comprehensive crew"""
        requirements_task = Task(
            description="""Gather requirements from the user about their goals and what they want to achieve. 
            Also collect their email address for sending personalized reminders.
            Ask clarifying questions if needed.""",
            expected_output="A clear summary of the user's goals, requirements, and email address for reminders.",
            agent=requirements_agent
        )
        
        comprehensive_task = Task(
            description="""Create a complete comprehensive solution that includes ALL of the following in one integrated report:

            1. MENTAL HEALTH ANALYSIS:
               - Analyze user conversations to identify potential mental health challenges or issues
               - Research relevant resources and solutions using available tools
               - Provide insights on how mental health factors may impact goal achievement

            2. GOAL PLANNING:
               - Break the user's goal into <=7 outcome-based tasks with dependencies and assumptions
               - Consider mental health factors when creating the plan
               - Include clear task definitions with specific outcomes

            3. TIME & IMPACT ANALYSIS:
               - Estimate time_hours for each task with 0.25h granularity, considering mental health factors
               - Assign impact_pct to each task (total ≈ 100%) with rationale
               - Consider mental health benefits and therapeutic value in impact assessment

            4. PRIORITIZATION:
               - Calculate priority_score = impact_pct / max(time_hours, 0.25)
               - Sort tasks by priority score in descending order
               - Ensure dependencies appear earlier in the sequence

            5. SCHEDULING:
               - Build day-by-day schedule respecting daily capacity (default 4 hours) and buffer (15%)
               - Consider mental health accommodations and pacing
               - Include stress management and recovery time
               - Identify capacity warnings if exceeded

            6. MONITORING & EMAIL REMINDERS:
               - Create reminders for today's top priority items
               - Send personalized email reminders with task details and mental health considerations
               - Include mental health check-ins and wellness reminders in emails
               - Suggest adjustments for any capacity warnings
               - Provide proactive recommendations for schedule optimization
               - Use email_tool.send_reminder_email() to send formatted HTML emails

            Perform all analysis, planning, and scheduling within this single comprehensive task.""",
            expected_output="""A complete JSON report with the following structure:
            {
                "mental_health_analysis": {
                    "challenges_identified": [],
                    "research_findings": [],
                    "recommendations": []
                },
                "goal_planning": {
                    "tasks": [
                        {
                            "name": "task_name",
                            "description": "task_description",
                            "dependencies": [],
                            "assumptions": []
                        }
                    ]
                },
                "time_impact_analysis": {
                    "tasks": [
                        {
                            "name": "task_name",
                            "time_hours": 0.25,
                            "impact_pct": 15,
                            "rationale": "why this task is important"
                        }
                    ]
                },
                "prioritization": {
                    "tasks": [
                        {
                            "name": "task_name",
                            "time_hours": 0.25,
                            "impact_pct": 15,
                            "priority_score": 60,
                            "dependencies": []
                        }
                    ]
                },
                "schedule": {
                    "timeline": [
                        {
                            "date": "YYYY-MM-DD",
                            "tasks": ["task_name"],
                            "total_hours": 4,
                            "buffer_hours": 0.6
                        }
                    ],
                    "warnings": []
                },
                "monitoring": {
                    "reminders": [
                        {
                            "time": "09:00",
                            "task": "task_name",
                            "message": "reminder_message",
                            "email_sent": true,
                            "email_subject": "Daily Task Reminder",
                            "email_recipient": "user@example.com"
                        }
                    ],
                    "email_reminders": [
                        {
                            "recipient": "user@example.com",
                            "subject": "Daily Task Reminder",
                            "message": "Personalized reminder message with mental health considerations",
                            "task_details": {
                                "name": "task_name",
                                "time_hours": 0.25,
                                "priority_score": 60,
                                "impact_pct": 15,
                                "rationale": "why this task is important"
                            }
                        }
                    ],
                    "adjustments": []
                }
            }""",
            agent=comprehensive_agent,
            context=[requirements_task]
        )
        
        return requirements_task, comprehensive_task

    def create_goal_planning_tasks(self, goal_planner: Agent, time_analyzer: Agent, impact_agent: Agent, prioritizer: Agent, scheduler: Agent, monitor: Agent):
        """Create the structured goal planning workflow tasks"""
        
        # Task 1: Plan Goal
        plan_goal_task = Task(
            description="""Break the user's goal into <=7 outcome-based tasks with dependencies and assumptions.
            Create a structured plan that includes:
            - Clear task definitions with specific outcomes
            - Task dependencies and relationships
            - Realistic assumptions about requirements and constraints
            - Deliverables for each task""",
            expected_output="JSON with tasks[] array and assumptions object. Each task should have name, description, dependencies, and assumptions.",
            agent=goal_planner
        )
        
        # Task 2: Estimate Time
        estimate_time_task = Task(
            description="""For each task from the goal plan, estimate time_hours with 0.25h granularity.
            Prefer smaller chunks and consider:
            - Task complexity and scope
            - User capabilities and experience level
            - Potential obstacles and learning curves
            - Dependencies and prerequisites""",
            expected_output="JSON with tasks[name, time_hours] where time_hours is in 0.25h increments.",
            agent=time_analyzer,
            context=[plan_goal_task]
        )
        
        # Task 3: Assign Impact
        assign_impact_task = Task(
            description="""Assign impact_pct to each task so that total ≈ 100% and include a one-line rationale per task.
            Consider:
            - Relative importance of each task
            - Short-term vs long-term value
            - Strategic vs tactical impact
            - User's immediate needs vs future goals""",
            expected_output="JSON with tasks[name, impact_pct, why] where impact_pct totals approximately 100%.",
            agent=impact_agent,
            context=[plan_goal_task]
        )
        
        # Task 4: Prioritize
        prioritize_task = Task(
            description="""Merge time_hours and impact_pct data and compute priority_score = impact_pct / max(time_hours, 0.25).
            Sort tasks by priority_score in descending order and ensure dependencies appear earlier.
            Create a final prioritized task list with:
            - Priority scores
            - Execution order
            - Dependency relationships
            - Time and impact data""",
            expected_output="JSON with tasks[name, time_hours, impact_pct, priority_score, dependencies] sorted by priority_score desc.",
            agent=prioritizer,
            context=[plan_goal_task, estimate_time_task, assign_impact_task]
        )
        
        # Task 5: Schedule
        schedule_task = Task(
            description="""Build a day-by-day schedule from the prioritized tasks, respecting daily capacity and buffer.
            Consider the following parameters:
            - Start date: Use current date or specified start date
            - Daily capacity: Default 4 hours per day (adjustable)
            - Buffer percentage: Default 15% buffer time
            - Task dependencies and optimal sequencing
            - Weekends, holidays, and personal constraints
            
            Identify when capacity is exceeded and provide warnings.""",
            expected_output="JSON timeline with schedule[] array containing daily tasks, plus optional warnings[] when capacity is exceeded.",
            agent=scheduler,
            context=[prioritize_task]
        )
        
        # Task 6: Monitor
        monitor_task = Task(
            description="""Create reminders for today's top items and suggest adjustments if any warnings were produced.
            Consider:
            - First reminder time: Default 09:00 (adjustable)
            - Today's priority tasks from the schedule
            - Any capacity warnings or scheduling conflicts
            - Proactive recommendations for schedule optimization
            - Progress tracking and course correction suggestions""",
            expected_output="JSON with reminders[] array for today's tasks and adjustments[] array with suggestions if needed.",
            agent=monitor,
            context=[schedule_task, prioritize_task]
        )
        
        return plan_goal_task, estimate_time_task, assign_impact_task, prioritize_task, schedule_task, monitor_task

    def optimized_crew(self) -> Crew:
        """Create and return the optimized comprehensive crew"""
        requirements_agent = self.create_requirements_agent()
        comprehensive_agent = self.create_comprehensive_agent()
        
        requirements_task, comprehensive_task = self.create_optimized_tasks(requirements_agent, comprehensive_agent)
        
        return Crew(
            agents=[requirements_agent, comprehensive_agent],
            tasks=[requirements_task, comprehensive_task],
            process=Process.sequential,
            verbose=True
        )
        
    def legacy_comprehensive_crew(self) -> Crew:
        """Legacy method - kept for comparison (8 agents, 8 tasks)"""
        # Create all agents for legacy approach
        requirements_agent = self.create_requirements_agent()
        analyst = self.create_analyst_agent()
        goal_planner = self.create_goal_planner_agent()
        time_analyzer = self.create_time_analyzer_agent()
        impact_agent = self.create_impact_agent()
        prioritizer = self.create_prioritizer_agent()
        scheduler = self.create_scheduler_agent()
        monitor = self.create_monitor_agent()
        
        # Create legacy tasks
        requirements_task = Task(
            description="Gather requirements from the user about their goals and what they want to achieve. Ask clarifying questions if needed.",
            expected_output="A clear summary of the user's goals and requirements.",
            agent=requirements_agent
        )
        
        mental_health_analysis_task = Task(
            description="""Conduct comprehensive mental health analysis and research:
            1. Analyze user conversations to identify potential mental health challenges or issues
            2. Research relevant resources and solutions using available tools
            3. Provide insights on how mental health factors may impact goal achievement
            4. Suggest mental health considerations for the goal planning process""",
            expected_output="A comprehensive mental health analysis with research findings and recommendations for goal planning.",
            agent=analyst,
            context=[requirements_task]
        )
        
        plan_goal_task = Task(
            description="""Break the user's goal into <=7 outcome-based tasks with dependencies and assumptions.
            Consider the mental health analysis and research findings when creating the plan.""",
            expected_output="JSON with tasks[] array and assumptions object, incorporating mental health insights.",
            agent=goal_planner,
            context=[requirements_task, mental_health_analysis_task]
        )
        
        estimate_time_task = Task(
            description="""For each task from the goal plan, estimate time_hours with 0.25h granularity.
            Consider mental health factors and user capabilities.""",
            expected_output="JSON with tasks[name, time_hours] where time_hours accounts for mental health considerations.",
            agent=time_analyzer,
            context=[plan_goal_task]
        )
        
        assign_impact_task = Task(
            description="""Assign impact_pct to each task so that total ≈ 100% and include a one-line rationale per task.
            Consider mental health impact and therapeutic value.""",
            expected_output="JSON with tasks[name, impact_pct, why] where impact_pct considers mental health value.",
            agent=impact_agent,
            context=[plan_goal_task]
        )
        
        prioritize_task = Task(
            description="""Merge time_hours and impact_pct data and compute priority_score = impact_pct / max(time_hours, 0.25).
            Sort tasks by priority score in descending order and ensure dependencies appear earlier.""",
            expected_output="JSON with tasks[name, time_hours, impact_pct, priority_score, dependencies] sorted by priority_score desc.",
            agent=prioritizer,
            context=[plan_goal_task, estimate_time_task, assign_impact_task]
        )
        
        schedule_task = Task(
            description="""Build a day-by-day schedule from the prioritized tasks, respecting daily capacity and buffer.
            Consider mental health factors in scheduling.""",
            expected_output="JSON timeline with schedule[] array containing daily tasks, plus optional warnings[] when capacity is exceeded.",
            agent=scheduler,
            context=[prioritize_task]
        )
        
        monitor_task = Task(
            description="""Create reminders for today's top items and suggest adjustments if any warnings were produced.
            Consider mental health monitoring and support.""",
            expected_output="JSON with reminders[] array for today's tasks and adjustments[] array with mental health considerations.",
            agent=monitor,
            context=[schedule_task, prioritize_task]
        )
        
        return Crew(
            agents=[requirements_agent, analyst, goal_planner, time_analyzer, impact_agent, prioritizer, scheduler, monitor],
            tasks=[requirements_task, mental_health_analysis_task, plan_goal_task, estimate_time_task, assign_impact_task, prioritize_task, schedule_task, monitor_task],
            process=Process.sequential,
            verbose=True
        )

def main():
    """Run the optimized mental health support crew"""
    print("🚀 Optimized Mental Health Support Crew")
    
    crew_instance = MentalHealthSupportCrew()
    
    # Choose which crew to run
    print("\nChoose crew type:")
    print("1. Optimized Comprehensive Crew (recommended - all features in one)")
    print("2. Legacy Multi-Agent Crew (8 agents, 8 tasks)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        print("\n🔄 Starting Legacy Multi-Agent Process...")
        print("   (8 agents: requirements, analyst, goal_planner, time_analyzer, impact_agent, prioritizer, scheduler, monitor)")
        crew = crew_instance.legacy_comprehensive_crew()
    else:
        print("\n⚡ Starting Optimized Comprehensive Process...")
        print("   (2 agents: requirements + comprehensive specialist)")
        print("   (All features: mental health analysis, goal planning, scheduling, monitoring)")
        crew = crew_instance.optimized_crew()
    
    result = crew.kickoff()
    
    print("\n✅ RESULT:")
    print("="*60)
    print(result)
    print("="*60)

if __name__ == "__main__":
    main()
