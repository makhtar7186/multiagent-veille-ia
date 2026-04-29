from crewai import Task
from agents.team import TeamAgent
from datetime import datetime

TODAY = datetime.now().strftime("%d %B %Y")

class Workflow:
    def __init__(self):

        self.team_agent = TeamAgent()
        self.ai_scout = self.team_agent.ai_scout
        self.analyst = self.team_agent.analyst
        self.reporter = self.team_agent.reporter
        self.search_tool = self.team_agent.search_tool

        self.collect_task = self.create_collect_task()
        self.analysis_task = self.create_analysis_task()
        self.report_task = self.create_report_task()

    # task 1 : collecte d'informations
    def create_collect_task(self):
        return Task(
            description=f""" Nous somme le {self.get_date()}
            
            Effectue des recherches approfondies sur les actualités IA 
            de cette semaine. Cherche sur :
            1. Les nouveaux modèles de langage publiés
            2. Les avancées en agents IA et systèmes multi-agents
            3. Les applications industrielles émergentes
            4. Les publications de recherche marquantes
            
            Pour chaque domaine, fais au moins 2 recherches distinctes.""",
            expected_output="""Une liste structurée de 10 à 15 informations clés avec :
            - Titre de l'événement/découverte
            - Description en 2-3 phrases
            - Source et date approximative
            - Niveau d'importance (Haute/Moyenne/Basse)""",
            agent=self.ai_scout,
            tools=[self.search_tool]
        )
    
    # task 2 : analyse des informations
    def create_analysis_task(self):
        return Task(
            description="""À partir des informations collectées par l'AI Scout,
            effectue une analyse approfondie :
            1. Identifie les 3-5 tendances majeures de la semaine
            2. Évalue l'impact potentiel de chaque découverte
            3. Identifie les connexions entre les différentes informations
            4. Dégage une vue d'ensemble du mouvement de l'industrie""",
            expected_output="""Un document d'analyse structuré contenant :
            - Les tendances majeures avec explication
            - Une évaluation de l'impact (court/moyen terme)
            - Les connexions identifiées entre les événements
            - Une conclusion sur la direction de l'industrie""",
            agent=self.analyst,
            context=[self.collect_task]  # dépend du résultat précédent
        )
    
    # task 3 : création du rapport
    def create_report_task(self):
        return Task(
            description="""Rédige un rapport de veille IA hebdomadaire professionnel
            basé sur la collecte et l'analyse précédentes. 
            Le rapport doit être en Markdown, prêt à être publié en langue française, et structuré de manière claire et engageante.""",
            expected_output="""Un rapport Markdown complet avec :
            # 🤖 Rapport de Veille IA — [Semaine]
            ## 📌 Faits Saillants (3 bullets max)
            ## 🔍 Actualités Détaillées (sections par thème)
            ## 📈 Tendances & Analyse
            ## 🎯 Ce qu'il faut retenir
            ## 📚 Sources (l'ensemble des liens où on a recuperer les informations) """,
            agent=self.reporter,
            context=[self.collect_task, self.analysis_task],
            output_file=f"rapport_veille_ia_{self.get_date()}.md"  # sauvegarde automatique
        )
    
    def get_date(self):
        return  datetime.now().strftime("%d %B %Y")

    

    

    