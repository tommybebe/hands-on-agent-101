from datetime import datetime
from typing import List, Dict, Any, Optional
from google.adk.agents import Agent
from dotenv import load_dotenv

load_dotenv()

def create_task(title: str, description: str = "", priority: str = "medium") -> Dict[str, Any]:
    """
    Creates a new task in the workflow system
    
    Args:
        title (str): The title of the task
        description (str): Optional description of the task
        priority (str): Priority level (low, medium, high)
    
    Returns:
        Dict[str, Any]: Task details including ID, status, and timestamp
    """
    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    return task

def update_task_status(task_id: str, status: str) -> Dict[str, Any]:
    """
    Updates the status of an existing task
    
    Args:
        task_id (str): The ID of the task to update
        status (str): New status (pending, in_progress, completed, blocked)
    
    Returns:
        Dict[str, Any]: Updated task details
    """
    valid_statuses = ["pending", "in_progress", "completed", "blocked"]
    if status not in valid_statuses:
        return {"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}
    
    updated_task = {
        "id": task_id,
        "status": status,
        "updated_at": datetime.now().isoformat(),
        "message": f"Task {task_id} status updated to {status}"
    }
    return updated_task

def create_workflow(name: str, tasks: List[str], description: str = "") -> Dict[str, Any]:
    """
    Creates a workflow with multiple interconnected tasks
    
    Args:
        name (str): Name of the workflow
        tasks (List[str]): List of task titles to include in the workflow
        description (str): Optional workflow description
    
    Returns:
        Dict[str, Any]: Workflow details with generated task IDs
    """
    workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    workflow_tasks = []
    
    for i, task_title in enumerate(tasks):
        task_id = f"{workflow_id}_task_{i+1}"
        workflow_tasks.append({
            "id": task_id,
            "title": task_title,
            "order": i + 1,
            "status": "pending"
        })
    
    workflow = {
        "id": workflow_id,
        "name": name,
        "description": description,
        "tasks": workflow_tasks,
        "status": "created",
        "created_at": datetime.now().isoformat()
    }
    return workflow

def get_workflow_status(workflow_id: str) -> Dict[str, Any]:
    """
    Gets the current status of a workflow and its tasks
    
    Args:
        workflow_id (str): The ID of the workflow to check
    
    Returns:
        Dict[str, Any]: Workflow status summary
    """
    return {
        "workflow_id": workflow_id,
        "checked_at": datetime.now().isoformat(),
        "message": f"Workflow {workflow_id} status retrieved",
        "note": "This is a simulated status check - in production this would query actual workflow data"
    }

def parse_markdown_manual(markdown_content: str) -> Dict[str, Any]:
    """
    Parses a markdown process manual and extracts teams, roles, tasks, and requirements
    
    Args:
        markdown_content (str): The markdown content of the process manual
    
    Returns:
        Dict[str, Any]: Parsed manual structure with teams, tasks, checklists, conditions
    """
    lines = markdown_content.split('\n')
    parsed_manual = {
        "title": "",
        "teams": [],
        "global_constraints": [],
        "data_requirements": []
    }
    
    current_team = None
    current_task = None
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Parse title (# header)
        if line.startswith('# '):
            parsed_manual["title"] = line[2:].strip()
            
        # Parse team sections (## Team: ...)
        elif line.startswith('## Team:') or line.startswith('## '):
            if current_team:
                parsed_manual["teams"].append(current_team)
            current_team = {
                "name": line.replace('## Team:', '').replace('##', '').strip(),
                "workers": [],
                "tasks": []
            }
            current_task = None
            
        # Parse workers (### Worker: ...)
        elif line.startswith('### Worker:') or line.startswith('### '):
            if current_team:
                worker_name = line.replace('### Worker:', '').replace('###', '').strip()
                current_team["workers"].append(worker_name)
                
        # Parse tasks (#### Task: ...)
        elif line.startswith('#### Task:') or line.startswith('#### '):
            if current_task and current_team:
                current_team["tasks"].append(current_task)
            current_task = {
                "title": line.replace('#### Task:', '').replace('####', '').strip(),
                "checklist": [],
                "conditions": [],
                "constraints": [],
                "data_required": [],
                "tools_needed": []
            }
            
        # Parse checklist items (- [ ] ...)
        elif line.startswith('- [ ]') or line.startswith('- [x]'):
            if current_task:
                item = line.replace('- [ ]', '').replace('- [x]', '').strip()
                current_task["checklist"].append(item)
                
        # Parse conditions (**Conditions:**)
        elif line.startswith('**Conditions:**'):
            current_section = 'conditions'
        elif line.startswith('**Constraints:**'):
            current_section = 'constraints'
        elif line.startswith('**Data Required:**'):
            current_section = 'data_required'
        elif line.startswith('**Tools:**'):
            current_section = 'tools_needed'
            
        # Parse list items under sections
        elif line.startswith('- ') and current_section and current_task:
            item = line[2:].strip()
            current_task[current_section].append(item)
            
    # Add final team and task
    if current_task and current_team:
        current_team["tasks"].append(current_task)
    if current_team:
        parsed_manual["teams"].append(current_team)
        
    return parsed_manual

def plan_workflow_from_manual(parsed_manual: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a workflow plan from a parsed manual structure
    
    Args:
        parsed_manual (Dict[str, Any]): Parsed manual from parse_markdown_manual
    
    Returns:
        Dict[str, Any]: Workflow plan with execution order and dependencies
    """
    workflow_plan = {
        "id": f"workflow_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "title": parsed_manual.get("title", "Untitled Workflow"),
        "execution_phases": [],
        "agent_assignments": [],
        "dependencies": [],
        "created_at": datetime.now().isoformat()
    }
    
    phase_counter = 1
    for team in parsed_manual.get("teams", []):
        team_phase = {
            "phase": phase_counter,
            "team_name": team["name"],
            "workers": team["workers"],
            "tasks": []
        }
        
        for task in team.get("tasks", []):
            planned_task = {
                "task_id": f"task_{phase_counter}_{len(team_phase['tasks']) + 1}",
                "title": task["title"],
                "checklist_items": len(task.get("checklist", [])),
                "conditions_count": len(task.get("conditions", [])),
                "tools_required": task.get("tools_needed", []),
                "estimated_duration": "TBD",
                "parallel_execution": len(team["workers"]) > 1
            }
            team_phase["tasks"].append(planned_task)
            
        workflow_plan["execution_phases"].append(team_phase)
        phase_counter += 1
        
    return workflow_plan

def generate_specialized_agents(workflow_plan: Dict[str, Any], parsed_manual: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates specialized agents for each team/role in the workflow
    
    Args:
        workflow_plan (Dict[str, Any]): Workflow plan from plan_workflow_from_manual
        parsed_manual (Dict[str, Any]): Original parsed manual
    
    Returns:
        Dict[str, Any]: Generated agents with their configurations
    """
    generated_agents = {
        "workflow_id": workflow_plan["id"],
        "agents": [],
        "agent_hierarchy": {},
        "generated_at": datetime.now().isoformat()
    }
    
    for phase in workflow_plan.get("execution_phases", []):
        team_name = phase["team_name"]
        
        # Find corresponding team in parsed manual for detailed info
        team_info = None
        for team in parsed_manual.get("teams", []):
            if team["name"] == team_name:
                team_info = team
                break
                
        if not team_info:
            continue
            
        # Generate team lead agent
        team_agent = {
            "agent_id": f"agent_{team_name.lower().replace(' ', '_')}_lead",
            "name": f"{team_name} Lead Agent",
            "role": "team_coordinator",
            "model": "gemini-2.0-flash",
            "description": f"Coordinates tasks and manages workflow for {team_name}",
            "responsibilities": [
                "Task assignment and tracking",
                "Progress monitoring",
                "Condition validation",
                "Inter-team communication"
            ],
            "managed_tasks": [task["title"] for task in team_info.get("tasks", [])],
            "team_workers": team_info.get("workers", []),
            "required_tools": list(set([
                tool for task in team_info.get("tasks", [])
                for tool in task.get("tools_needed", [])
            ]))
        }
        
        generated_agents["agents"].append(team_agent)
        
        # Generate worker-specific agents if needed
        for worker in team_info.get("workers", []):
            worker_tasks = []
            worker_tools = set()
            
            for task in team_info.get("tasks", []):
                # Assume all workers can handle all team tasks (could be refined)
                worker_tasks.append(task["title"])
                worker_tools.update(task.get("tools_needed", []))
                
            worker_agent = {
                "agent_id": f"agent_{worker.lower().replace(' ', '_')}",
                "name": f"{worker} Worker Agent",
                "role": "task_executor",
                "model": "gemini-2.0-flash",
                "description": f"Executes specific tasks assigned to {worker}",
                "supervisor": team_agent["agent_id"],
                "assigned_tasks": worker_tasks,
                "required_tools": list(worker_tools)
            }
            
            generated_agents["agents"].append(worker_agent)
            
    return generated_agents

def match_tools_to_agents(generated_agents: Dict[str, Any], available_tools: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Matches available tools to agent requirements and suggests missing tools
    
    Args:
        generated_agents (Dict[str, Any]): Generated agents from generate_specialized_agents
        available_tools (List[str]): List of available tool names
    
    Returns:
        Dict[str, Any]: Tool matching results and recommendations
    """
    if available_tools is None:
        # Default available tools in this workflow system
        available_tools = [
            "create_task", "update_task_status", "create_workflow", "get_workflow_status",
            "parse_markdown_manual", "plan_workflow_from_manual", "generate_specialized_agents",
            "validate_conditions", "send_notification", "log_progress", "file_operations"
        ]
    
    tool_matching = {
        "workflow_id": generated_agents["workflow_id"],
        "agent_tool_assignments": [],
        "missing_tools": set(),
        "tool_recommendations": [],
        "matched_at": datetime.now().isoformat()
    }
    
    for agent in generated_agents.get("agents", []):
        agent_tools = {
            "agent_id": agent["agent_id"],
            "agent_name": agent["name"],
            "required_tools": agent.get("required_tools", []),
            "matched_tools": [],
            "missing_tools": []
        }
        
        for required_tool in agent.get("required_tools", []):
            if required_tool.lower() in [t.lower() for t in available_tools]:
                agent_tools["matched_tools"].append(required_tool)
            else:
                agent_tools["missing_tools"].append(required_tool)
                tool_matching["missing_tools"].add(required_tool)
                
        tool_matching["agent_tool_assignments"].append(agent_tools)
        
    # Convert set to list for JSON serialization
    tool_matching["missing_tools"] = list(tool_matching["missing_tools"])
    
    # Generate recommendations for missing tools
    for missing_tool in tool_matching["missing_tools"]:
        recommendation = {
            "tool_name": missing_tool,
            "suggested_implementation": f"function for {missing_tool}",
            "priority": "high" if missing_tool in ["email", "database", "api"] else "medium"
        }
        tool_matching["tool_recommendations"].append(recommendation)
        
    return tool_matching

workflow_agent = Agent(
    name="manual_to_workflow_agent",
    model="gemini-2.0-flash",
    description="An agent that converts markdown process manuals into executable agent workflows with specialized team agents",
    instruction=(
        "You are a sophisticated workflow automation agent that transforms organizational process manuals "
        "into executable agent-based workflows. Your process is: "
        "1. PARSE MANUAL: Read and parse markdown process manuals to extract teams, workers, tasks, checklists, conditions, and constraints "
        "2. PLAN WORKFLOW: Analyze the manual structure and create an execution plan with phases, dependencies, and timing "
        "3. GENERATE AGENTS: Create specialized agents for each team and role with appropriate responsibilities "
        "4. MATCH TOOLS: Assign and match required tools to each agent, identifying missing capabilities "
        "When given a markdown manual, follow this sequence: parse_markdown_manual -> plan_workflow_from_manual -> generate_specialized_agents -> match_tools_to_agents. "
        "Always provide detailed feedback on the generated workflow structure and any recommendations for implementation."
    ),
    tools=[
        create_task, update_task_status, create_workflow, get_workflow_status,
        parse_markdown_manual, plan_workflow_from_manual, generate_specialized_agents, match_tools_to_agents
    ],
)

root_agent = workflow_agent