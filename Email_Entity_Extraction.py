# import json
# from typing import Dict, List
# from langchain_groq import ChatGroq
# from langchain.prompts import PromptTemplate
# from langchain.schema import StrOutputParser
# import os 
# from dotenv import load_dotenv
# load_dotenv()
# class EmailAnalyzer:
#     def __init__(self, api_key: str, model: str = "llama-3.2-90b-vision-preview"):
#         # Initialize Grok model with LangChain
#         self.llm = ChatGroq(
#             groq_api_key=api_key,
#             model_name=model,
#             temperature=0.2,
#             max_tokens=1500
#         )
#         self.output_parser = StrOutputParser()

#     def analyze_email_for_transactions(self, email: Dict) -> List[Dict]:
#         """
#         Use LLM to analyze an email and identify which transaction(s) it belongs to
#         Returns a list of transaction details extracted from the email
#         """
#         # Extract email content
#         subject = email.get('email_subject', 'No Subject')
#         content = email.get('latest_message', '')
#         email_id = email.get('_id', '')
#         email_date = email.get('email_date', '')

#         if not content:
#             return []

#         # Prepare the prompt for the LLM with UN/LOCODE added
#         prompt_template = PromptTemplate(
#             input_variables=["subject", "content"],
#             template="""
#             Analyze this freight forwarding email and identify which transaction(s) it belongs to.

#             SUBJECT: {subject}

#             CONTENT:
#             {content}

#             TASK:
#             1. Identify any specific transaction identifiers (order numbers, quote references, booking numbers, etc.)
#             2. Determine if this email is about a new transaction or an existing one
#             3. Extract key details about the transaction (type, status, origin, destination, cargo, etc.)
#             4. If the email mentions multiple transactions, identify each one separately
#             5. For origin and destination, include the UN/LOCODE (United Nations Code for Trade and Transport Locations) if identifiable, otherwise use "N/A"

#             FORMAT YOUR RESPONSE AS JSON:
#             {{
#                 "transactions": [
#                     {{
#                         "transaction_type": "order" or "quote" or "booking" or "inquiry",
#                         "raw_transaction_id": "extracted identifier or generated if none exists",
#                         "is_new_transaction": true/false,
#                         "status": "inquiry", "quote_requested", "quote_provided", "order_placed", "in_progress", "completed", etc.,
#                         "confidence": 0-100 (how confident you are this is a distinct transaction),
#                         "reference_numbers": ["list", "of", "reference", "numbers"],
#                         "route": {{
#                             "origin": "Location or N/A",
#                             "origin_unlocode": "UN/LOCODE or N/A",
#                             "destination": "Location or N/A",
#                             "destination_unlocode": "UN/LOCODE or N/A"
#                         }},
#                         "cargo_details": {{
#                             "Boooking ID":"Booking id if have any od N/A",
#                             "cargo_type": "Description or N/A",
#                             "container_type": "Type or N/A",
#                             "quantity": "Amount or N/A"
#                         }},
#                         "key_points": [
#                             "Important point about this transaction"
#                         ],
#                         "summary": "Brief summary of what this email says about this transaction"
#                     }}
#                 ]
#             }}

#             IMPORTANT GUIDELINES:
#             - If no clear transaction is identified, return an empty transactions array
#             - If multiple distinct transactions are mentioned, include each as a separate object in the transactions array
#             - For raw_transaction_id, extract any explicit reference numbers. If none exist, generate a descriptive ID based on the cargo, route, and date
#             - The confidence score should reflect how certain you are that this is a distinct transaction
#             - Include ALL reference numbers you can find (booking numbers, job numbers, container numbers, etc.) in the reference_numbers array
#             - For UN/LOCODE, use standard 5-character codes (e.g., "AEDXB" for Dubai, UAE) if the location can be confidently identified; otherwise, use "N/A"
#             """
#         )

#         # Create the chain
#         chain = prompt_template | self.llm | self.output_parser

#         # Invoke the chain with limited content length
#         try:
#             response = chain.invoke({
#                 "subject": subject,
#                 "content": content[:4000]  # Limit content length to avoid token limits
#             })

#             # Parse the response
#             analysis = json.loads(response)

#             # Add email_id and date to each transaction for reference
#             for transaction in analysis.get("transactions", []):
#                 transaction["email_ids"] = [email_id]
#                 transaction["email_dates"] = [email_date]

#                 # Add dates structure
#                 transaction["dates"] = {
#                     "first_contact": email_date,
#                     "last_update": email_date
#                 }

#                 # Add status history
#                 transaction["status_history"] = [
#                     {
#                         "status": transaction.get("status", "unknown"),
#                         "date": email_date,
#                         "email_id": email_id
#                     }
#                 ]

#             return analysis.get("transactions", [])

#         except json.JSONDecodeError as e:
#             print(f"Error parsing JSON response: {e}")
#             print(f"Raw response: {response}")
#             return []
#         except Exception as e:
#             print(f"Error analyzing email: {e}")
#             return []

# def main():
  
#     # Get email input from terminal
#     print("Please paste the email JSON and press Enter twice (blank line) when done:")
#     email_lines = []
#     while True:
#         line = input()
#         if line.strip() == "":  # Check for a blank line
#             break
#         email_lines.append(line)
    
#     try:
#         email_input = "".join(email_lines)
#         email = json.loads(email_input)
#     except json.JSONDecodeError as e:
#         print(f"Error: Invalid JSON input - {e}")
#         return

#     # Initialize the analyzer with your Grok API key
#     analyzer = EmailAnalyzer(
#         api_key = os.getenv("GROQ_API_KEY"),
#         model = os.getenv("model_name")
#     )

#     # Analyze the email
#     result = analyzer.analyze_email_for_transactions(email)

#     # Pretty print the result to terminal
#     print("\nAnalysis Result:")
#     print(json.dumps(result, indent=4))

# if __name__ == "__main__":
#     main()






import json
import os
from typing import Dict, List
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
import os 
from dotenv import load_dotenv
load_dotenv()
class EmailAnalyzer:
    def __init__(self, api_key: str, model: str = "llama-3.2-90b-vision-preview"):
        # Initialize Grok model with LangChain
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model,
            temperature=0.2,
            max_tokens=1500
        )
        self.output_parser = StrOutputParser()

    def analyze_email_for_transactions(self, email: Dict) -> List[Dict]:
        """
        Use LLM to analyze an email and identify which transaction(s) it belongs to
        Returns a list of transaction details extracted from the email
        """
        # Extract email content
        subject = email.get('email_subject', 'No Subject')
        content = email.get('latest_message', '')
        email_id = email.get('_id', '')
        email_date = email.get('email_date', '')

        if not content:
            return []

        # Prepare the prompt for the LLM with UN/LOCODE
        prompt_template = PromptTemplate(
            input_variables=["subject", "content"],
            template="""
            Analyze this freight forwarding email and identify which transaction(s) it belongs to.

            SUBJECT: {subject}

            CONTENT:
            {content}

            TASK:
            1. Identify any specific transaction identifiers (order numbers, quote references, booking numbers, etc.)
            2. Determine if this email is about a new transaction or an existing one
            3. Extract key details about the transaction (type, status, origin, destination, cargo, etc.)
            4. If the email mentions multiple transactions, identify each one separately
            5. For origin and destination, include the UN/LOCODE (United Nations Code for Trade and Transport Locations) if identifiable, otherwise use "N/A"

            FORMAT YOUR RESPONSE AS JSON:
            {{
                "transactions": [
                    {{
                        "transaction_type": "order" or "quote" or "booking" or "inquiry",
                        "raw_transaction_id": "extracted identifier or if doesnt exist N/A",
                        "is_new_transaction": true/false,
                        "status": "inquiry", "quote_requested", "quote_provided", "order_placed", "in_progress", "completed", etc.,
                        "confidence": 0-100 (how confident you are this is a distinct transaction),
                        "reference_numbers": ["list", "of", "reference", "numbers"],
                        "route": {{
                            "origin": "Location or N/A",
                            "origin_unlocode": "UN/LOCODE or N/A",
                            "destination": "Location or N/A",
                            "destination_unlocode": "UN/LOCODE or N/A"
                        }},
                        "cargo_details": {{
                            "cargo_type": "Description or N/A",
                            "container_type": "Type or N/A",
                            "quantity": "Amount or N/A"
                        }},
                        "key_points": [
                            "Important point about this transaction"
                        ],
                        "summary": "Brief summary of what this email says about this transaction"
                    }}
                ]
            }}

            IMPORTANT GUIDELINES:
            - If no clear transaction is identified, return an empty transactions array
            - If multiple distinct transactions are mentioned, include each as a separate object in the transactions array
            - For raw_transaction_id, extract any explicit reference numbers. If none exist, generate a descriptive ID based on the cargo, route, and date
            - The confidence score should reflect how certain you are that this is a distinct transaction
            - Include ALL reference numbers you can find (booking numbers, job numbers, container numbers, etc.) in the reference_numbers array
            - For UN/LOCODE, use standard 5-character codes (e.g., "AEDXB" for Dubai, UAE) if the location can be confidently identified; otherwise, use "N/A"
            """
        )

        # Create the chain
        chain = prompt_template | self.llm | self.output_parser

        # Invoke the chain with limited content length
        try:
            response = chain.invoke({
                "subject": subject,
                "content": content[:4000]  # Limit content length to avoid token limits
            })

            # Parse the response
            analysis = json.loads(response)

            # Add email_id and date to each transaction for reference
            for transaction in analysis.get("transactions", []):
                transaction["email_ids"] = [email_id]
                transaction["email_dates"] = [email_date]

                # Add dates structure
                transaction["dates"] = {
                    "first_contact": email_date,
                    "last_update": email_date
                }

                # Add status history
                transaction["status_history"] = [
                    {
                        "status": transaction.get("status", "unknown"),
                        "date": email_date,
                        "email_id": email_id
                    }
                ]

            return analysis.get("transactions", [])

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response: {response}")
            return []
        except Exception as e:
            print(f"Error analyzing email: {e}")
            return []

def process_folder(input_folder: str, output_folder: str, analyzer: 'EmailAnalyzer'):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Read the input JSON file
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    email = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: Invalid JSON - {e}")
                continue
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue

            # Analyze the email
            result = analyzer.analyze_email_for_transactions(email)

            # Save the result to a new JSON file
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=4)
                print(f"Processed {filename} -> Output saved to {output_path}")
            except Exception as e:
                print(f"Error writing output for {filename}: {e}")

def main():
    # Define input and output folders
    input_folder = "ucf.ae"
    output_folder = "output"

    # Check if input folder exists
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return

    # Initialize the analyzer with your Grok API key
    analyzer = EmailAnalyzer(
        api_key = os.getenv("GROQ_API_KEY"),
        model = os.getenv("model_name")
        
    )

    # Process all JSON files in the folder
    process_folder(input_folder, output_folder, analyzer)

if __name__ == "__main__":
    main()