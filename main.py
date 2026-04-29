# main.py
from crewai import Crew, Process
from agents.team import TeamAgent
from tasks.workflow import Workflow
from config.llm_config import LLMConfig
import time
llm_config = LLMConfig()

def run_veille_ia():
    workflow = Workflow()
    team_agent = TeamAgent()

    crew = Crew(
        agents=[team_agent.ai_scout, team_agent.analyst, team_agent.reporter],
        tasks=[workflow.collect_task, workflow.analysis_task, workflow.report_task],
        process=Process.sequential,
        verbose=True,
        memory=False,  # ← commentez cette ligne pour l'instance si true configuré avec embedder local
        tracing=True
    
       
    )
    
    result = crew.kickoff()
    print("\n" + "="*50)
    print("✅ Rapport généré : rapport_veille_ia.md")
    print(result)
    return result

import time

if __name__ == "__main__":
    start_time = time.time()

    run_veille_ia()

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Temps d'exécution : {execution_time:.2f} secondes")