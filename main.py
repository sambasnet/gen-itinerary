import os
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from a .env file
# This ensures sensitive data like API keys are not hardcoded in the script
load_dotenv('.env', override=True)

# Initialize the OpenAI client using the API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_journal(file_path):
    """
    Reads the content of a journal text file.
    
    Args:
        file_path (str): Path to the journal file.
    
    Returns:
        str: Entire text content of the journal file.
    """
    with open(file_path, 'r') as file:
        journal = file.read()
    return journal


def get_llm_response(prompt):
    """
    Sends a prompt to the OpenAI chat model and retrieves a response.
    
    Args:
        prompt (str): The user input or instruction to send to the LLM.
    
    Returns:
        str: The assistant's text response.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use lightweight GPT-4o-mini for faster responses
        messages=[
            {"role": "system", "content": "You are a helpful but terse AI assistant"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,  # Lower temperature → more focused & deterministic answers
    )
    return response.choices[0].message.content


def main():
    """
    Main function to generate a travel itinerary:
    - Reads a journal file for restaurant suggestions.
    - Takes arrival and departure dates as user input.
    - Sends a structured prompt to the LLM.
    - Prints the generated itinerary.
    """
    # File containing personal journal with restaurant notes
    file_path = 'tokyo.txt'
    journal = read_journal(file_path)

    # Destination details (hardcoded for now, can be parameterized later)
    city = 'Tokyo'
    country = 'Japan'

    # Ask the user for trip dates
    arrival = input("Enter arrival date (YYYY-MM-DD): ")
    departure = input("Enter departure date (YYYY-MM-DD): ")

    # Build the prompt for the LLM
    prompt = f'''
    I will visit {city}, {country} from {arrival} to {departure}. 
    Create a daily itinerary with detailed activities. 
    Designate times for breakfast, lunch, and dinner. 

    I want to visit the restaurants listed in the journal entry without repeating any place.
    Make sure to mention the specialty that I should try at each of them.

    Journal entry:
    {journal}
    '''

    # Get itinerary from the LLM
    response = get_llm_response(prompt)

    # Display the itinerary
    print(response)


# Run the program only if executed directly (not imported as a module)
if __name__ == "__main__":
    main()
