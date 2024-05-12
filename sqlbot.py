import os
import sqlite3
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate
)

class CourseScheduler:
    def __init__(self):
        os.environ["OPENAI_API_KEY"] = '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'
        self.db = SQLDatabase.from_uri("sqlite:///course_schedule.db")
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.agent = self.create_agent()
        self.create_database()

    def create_database(self):
        """ Create the database and table if not exists """
        conn = sqlite3.connect('course_schedule.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                course_code TEXT,
                course_name TEXT,
                section TEXT,
                time TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def create_agent(self):
        """ Configure and return the SQL agent """
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            self.load_examples(),
            OpenAIEmbeddings(),
            FAISS,
            k=5,
            input_keys=["input"],
        )

        system_prefix = self.define_system_prefix()

        few_shot_prompt = FewShotPromptTemplate(
            example_selector=example_selector,
            example_prompt=PromptTemplate.from_template(
                "User input: {input}\nSQL query: {query}"
            ),
            input_variables=["input", "dialect", "top_k"],
            prefix=system_prefix,
            suffix="",
        )

        full_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate(prompt=few_shot_prompt),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )

        return create_sql_agent(
            llm=self.llm,
            db=self.db,
            prompt=full_prompt,
            verbose=True,
            agent_type="openai-tools",
        )

    def define_system_prefix(self):
        """ Define and return the system prefix for the SQL agent """
        return """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct SQL INSERT query to add data to the database, ensuring to only insert data into tables as specified by the user's request. Your role is to construct and execute INSERT queries based on the given instructions.
You must not perform any other database operations like SELECT, UPDATE, DELETE, or DROP. Only use the provided tools to interact with the database and to formulate your answers. Always ensure that your query is correct before executing. If you encounter an error during the execution of an INSERT query, revise the query and try again.
If the question does not seem related to inserting data into the database, just return "I don't know" as the answer.
Here are some examples of user inputs and their corresponding SQL INSERT queries:
        """

    def load_examples(self):
        """ Load example queries and inputs for the agent """
        return [
            {
            "input": "| **Course Code** | **Course Title**                         | **Credits** | **Days** | **Time**       | **Section** |\n| CSC 212         | Fundamentals of Computer Programming II | 3           | MWF      | 4:00-5:00 PM   | D           |",
        "query": "INSERT INTO courses (course_code, course_name, section, time) VALUES ('CSC 212', 'Fundamentals of Computer Programming II', 'D', '4:00-5:00 PM');",
        },
        {
            "input": "| **Course Code** | **Course Title**                         | **Credits** | **Days** | **Time**       | **Section** |\n| MAT 211         | Discrete Mathematics                     | 3           | MWF      | 9:00-10:00 AM  | C           |",
            "query": "INSERT INTO courses (course_code, course_name, section, time) VALUES ('MAT 211', 'Discrete Mathematics', 'C', '9:00-10:00 AM');",
        },
        {
            "input": "| **Course Code** | **Course Title**                         | **Credits** | **Days** | **Time**       | **Section** |\n| MAT 213         | Calculus III                             | 3           | TTH      | 9:30-11:00 AM  | C           |",
            "query": "INSERT INTO courses (course_code, course_name, section, time) VALUES ('MAT 213', 'Calculus III', 'C', '9:30-11:00 AM');",
        },
        {
            "input": "| **Course Code** | **Course Title**                         | **Credits** | **Days** | **Time**       | **Section** |\n| MAT 215         | Linear Algebra I                         | 3           | TTH      | 3:00-4:30 PM   | B           |",
            "query": "INSERT INTO courses (course_code, course_name, section, time) VALUES ('MAT 215', 'Linear Algebra I', 'B', '3:00-4:30 PM');",
        },
        {
            "input": "| **Course Code** | **Course Title**                         | **Credits** | **Days** | **Time**       | **Section** |\n| REG 212         | (Liberal Arts Curriculum - Group 2)     | 3           | TBA      | TBA            | TBA         |",
            "query": "INSERT INTO courses (course_code, course_name, section, time) VALUES ('REG 212', '(Liberal Arts Curriculum - Group 2)', 'TBA', 'TBA');",
        },
        {
            "input": "| **Course Code** | **Course Title**                         | **Credits** | **Days** | **Time**       | **Section** |\n| PHY 301         | Quantum Mechanics                      | 4           | MWF      | 1:00-2:00 PM   | A           |",
            "query": "INSERT INTO courses (course_code, course_name, section, time) VALUES ('PHY 301', 'Quantum Mechanics', 'A', '1:00-2:00 PM');",
        },
        {
            "input": "| **Course Code** | **Course Title**                         | **Credits** | **Days** | **Time**       | **Section** |\n| ENG 204         | Modern World Literature                | 3           | TTH      | 11:00 AM-12:30 PM | E           |",
            "query": "INSERT INTO courses (course_code, course_name, section, time) VALUES ('ENG 204', 'Modern World Literature', 'E', '11:00 AM-12:30 PM');",
        },
        {
            "input": "| **Course Code** | **Course Title**                         | **Credits** | **Days** | **Time**       | **Section** |\n| BIO 107         | Marine Biology                          | 3           | MWF      | 9:00-10:00 AM  | B           |",
            "query": "INSERT INTO courses (course_code, course_name, section, time) VALUES ('BIO 107', 'Marine Biology', 'B', '9:00-10:00 AM');",
        },
        {
            "input": "| **Course Code** | **Course Title**                         | **Credits** | **Days** | **Time**       | **Section** |\n| ART 150         | History of Western Art                 | 3           | TTH      | 2:00-3:30 PM   | C           |",
            "query": "INSERT INTO courses (course_code, course_name, section, time) VALUES ('ART 150', 'History of Western Art', 'C', '2:00-3:30 PM');",
        },
        {
            "input": "| **Course Code** | **Course Title**                         | **Credits** | **Days** | **Time**       | **Section** |\n| PHI 230         | Ethics in the Modern World              | 3           | MWF      | 3:00-4:00 PM   | F           |",
            "query": "INSERT INTO courses (course_code, course_name, section, time) VALUES ('PHI 230', 'Ethics in the Modern World', 'F', '3:00-4:00 PM');",
        }
        ]

    def schedule_class(self, input_text):
        """ Schedule a class by invoking the agent """
        return self.agent.invoke({"input": input_text})

# Example usage:
# scheduler = CourseScheduler()
# result = scheduler.schedule_class("| **Course Code** | **Course Title**                         | **Credits** | **Days** | **Time**       | **Section** |\n| PHI 230         | Ethics in the Modern World              | 3           | MWF      | 3:00-4:00 PM   | F           |")
# print(result)
