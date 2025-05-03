from datetime import datetime

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Initialize the OpenAI LLM
from ollama_def import llm


# Define the prompt template to extract and convert the date
class LeaveRequest:
    def __init__(self, llm):
        self.prompt = PromptTemplate(
            input_variables=["text", "today"],
            template="""

           You are a chatbot that extracts useful information from leave messages. Today's date is {today}. Your task is to extract details about late arrivals, leaves, work-from-home (WFH) requests, and early departures from the text provided, and convert all dates into the format YYYY-MM-DD using today as the reference.

            The reference to dates may be given according to months, weeks, or days ("today", "tomorrow", "next week," etc.).

            Output the extracted information only in JSON format.

            Instructions:

            Do NOT include any code or parsing instructions.

            If the name of the person is not specified, set the name as null.

            If the reason is not specified, set reason as null.

            Accurately process dates based on the given message and today's date.

            The office working hours are 9 am to 5 pm.

            Flag late: true ONLY if the person is arriving after 9:00 am.

            Flag early_departure: true ONLY if the person is leaving before 5:00 pm.

            Leaving early is NOT the same as arriving late.

            If multiple types (e.g., leave + WFH) are mentioned for different days, output them as separate JSON objects.

            If multiple types are mentioned for same day (e.g., WFH in first half, leave in second half), split into separate JSON objects with "leave": "Second Half" or "WFH": "First Half".

        Output fields (per object):

            "name": string or null,
            "late": true/false,
            "leave": 
                    "first_half":true/false,
                    "second_half":true/false,
                    "whole_day":true/false
            "wfh": 
                    "first_half":true/false,
                    "second_half":true/false,
                    "whole_day":true/false
            "start_date": "YYYY-MM-DD",
            "end_date": "YYYY-MM-DD" or null,
            "early_departure": true/false,
            "reason": string or null
            "partially_unavailable":true/false

        Examples:

        Input:
        XYZ: @channel I'll be working remotely as I moved to Imadol last night. I'm not feeling well, so I'll be taking breaks to rest throughout the day.
        Date: 2024-01-08

        Date: 2024-01-08

        Expected Output in JSON format:

                "name": "XYZ",
                "late": false,
                "leave": 
                    "first_half":false,
                    "second_half":false,
                    "whole_day":false
                 "wfh": 
                    "first_half":false,
                    "second_half":false,
                    "whole_day":true
                "start_date": "2024-01-08",
                "end_date": null,
                "early_departure": false,
                "reason": "Moved to Imadol"
                "partially_unavailable": false,

        Input:
        JOHN: @channel I will be leaving at around 4:30 pm"
        Date: 2024-03-08

        Expected Output:
                
                "name": "JOHN",
                "late": false,
                "leave": 
                    "first_half":false,
                    "second_half":false,
                    "whole_day":false
                 "wfh": 
                    "first_half":false,
                    "second_half":false,
                    "whole_day":false
                "start_date": "2024-03-08",
                "end_date": null,
                "early_departure": true,
                "reason": null
                "partially_unavailable": true
                


        Input:
        RAM: @channel I will take a leave tomorrow as I have to visit a hospital. Also, I will be working from home the day after tomorrow.
        Date: 2024-03-12

        Expected Output:
                [
                    "name": "RAM",
                    "late": false,
                    "leave": 
                        "first_half":false,
                        "second_half":false,
                        "whole_day":true
                    "wfh": 
                        "first_half":false,
                        "second_half":false,
                        "whole_day":false
                    "start_date": "2024-03-13",
                    "end_date": null,
                    "early_departure": false,
                    "reason": "To visit hospital"
                    "partially_unavailable": true
                ,
                
                    "name": "RAM",
                    "late": false,
                    "leave": 
                        "first_half":false,
                        "second_half":false,
                        "whole_day":false
                    "wfh": 
                        "first_half":false,
                        "second_half":false,
                        "whole_day":true
                    "start_date": "2024-03-14",
                    "end_date": null,
                    "early_departure": false,
                    "reason": null,
                    "partially_unavailable": true
                
                ]


        Input:
        SNDSED: @channel I will be working from home today in the first half and will be on leave on the second half. I will also be on leave for 3 days starting tomorrow.
        Date: 2024-02-12

        Expected Output:
                [
                
                    "name": "SNDSED",
                    "late": false,
                   "leave": 
                        "first_half":false,
                        "second_half":true,
                        "whole_day":false
                    "wfh": 
                        "first_half":true,
                        "second_half":false,
                        "whole_day":false
                    "start_date": "2024-02-12",
                    "end_date": null,
                    "early_departure": false,
                    "reason": null
                ,
                
                    "name": "SNDSED",
                    "late": false,
                    "leave": 
                        "first_half":false,
                        "second_half":true,
                        "whole_day":true
                    "wfh": 
                        "first_half":false,
                        "second_half":false,
                        "whole_day":false
                    "start_date": "2024-02-13",
                    "end_date": "2024-02-15",
                    "early_departure": false,
                    "reason": null
                


        Now, extract the information from the following message text: {text}

            """,
        )

        self.parser = JsonOutputParser()

        # Create an LLMChain using the LLM and the prompt template
        self.llm_chain = self.prompt | llm | self.parser
        self.llm = llm

    # Function to get today's date
    def get_today(self):
        return datetime.now().strftime("%Y-%m-%d")

    # Define a function to parse dates using LLM
    def get_results(self, text):
        today = self.get_today()
        return self.llm_chain.invoke({"text": text, "today": today})


leave_request_parser = LeaveRequest(llm)
