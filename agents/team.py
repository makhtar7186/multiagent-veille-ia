# agents/team.py — Compatible CrewAI >= 0.80
from crewai import Agent
from tools.search_tools import WebSearchTool
from config.llm_config import LLMConfig


## creation d'une classe TeamAgent pour regrouper les agents et outils
class TeamAgent:
    def __init__(self):
        self.llm_config = LLMConfig()
        # initialisation des LLMs pour chaque agent (peut être personnalisé) 
        # tous les agents utilisent le même LLM, mais on peut facilement changer ça en assignant des LLMs différents à chaque agent
        #self.scout_llm = self.llm_config.llama3_2
        #self.analyst_llm = self.llm_config.llama3_1
        #self.reporter_llm = self.llm_config.mistral_llm
        self.llm_general = self.llm_config.mistral_llm
        self.search_tool = WebSearchTool()

        self.ai_scout = self.create_aiscout()
        self.analyst = self.create_analyst()
        self.reporter = self.create_reporter()


    def create_aiscout(self):
        return Agent(
        role="Expert en Veille Technologique IA",
        goal="Collecter les actualités les plus récentes et pertinentes sur l'Intelligence Artificielle, les LLM et les agents IA",
        backstory="""Tu es un veilleur technologique senior spécialisé en IA.
        Tu sais identifier les informations vraiment importantes parmi
        la masse d'articles publiés chaque jour. Tu te concentres sur
        les percées techniques, les nouveaux modèles et les tendances émergentes.""",
        tools=[self.search_tool],
        llm= self.llm_general,
        verbose=True,
        max_iter=5
    )

    def create_analyst(self):
        return Agent(
        role="Analyste en Intelligence Artificielle",
        goal="Analyser les informations collectées, identifier les tendances majeures et évaluer leur impact sur l'industrie",
        backstory="""Tu es un analyste IA avec 10 ans d'expérience. Tu as une vision
        critique et nuancée. Tu sais distinguer le marketing du progrès réel.
        Tu contextualises chaque information dans les tendances plus larges.""",
        llm= self.llm_general,
        verbose=True,
        allow_delegation=False
    )

    def create_reporter(self):
        return Agent(
            role="Rédacteur Technique Spécialisé IA",
            goal="Produire un rapport de veille clair, structuré et actionnable "
                "à destination de professionnels de la tech",
            backstory="""Tu es un rédacteur technique expert qui vulgarise sans simplifier.
            Tu sais structurer l'information pour qu'elle soit immédiatement utile.
            Ton rapport doit être lisible en 5 minutes et complet.""",
            llm= self.llm_general,
            verbose=True,
            allow_delegation=False
        )




 