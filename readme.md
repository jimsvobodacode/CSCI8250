# Milestone Summary

M1. For Milestone 1 we created a basic console application to explore the functionality of the OpenAI Agent SDK.  Two agents were used.  One was a guardrail agent to ensure input was contextually appropriate and the other was a profile agent that would gather basic travel profile information.
The Azure infrasture was created for M1. IIS was configured to run Python/Django websites.  The DNS and TLS certificate were configured.

M2. We refined the prototype to focus on the conversational interaction between the user and the AI assistant. The updated design introduces processing feedback, follow-up questions, profile confirmation, and error-recovery options. Rather than presenting the complete trip itinerary immediately, the assistant first gathers and confirms the information needed to create an appropriate travel plan.
The initial website was built and published to Azure for M2.  An additional guardrail agent was created to make sure only authorized users were allowed.  Session logic was added.  The profile collector agent was configured to collect two data fields.

M3. The logic for the diagnostic information was enhance to display more details more clearly.  The profile agent was modifed to collect a third data point - "interests".  A planner agent was added to take the profile data points (city/budget/interests) and identify/suggest activities (just dispalyed in the diagnostics area).

M4. The authentication agent was removed and simplified to just be an if/then statment.  The AI models were updated to used gpt-6-luna (from 5.6-luna).  A formatter agent was added to display the trip activities in a decent format.


# Need help? Jim is happy to help! Send Jim an email or text to schedule a time.

1. Make sure you have VS Code and Python installed.
2. Clone the code from the GitHub repository to a local folder.
3. To run the website code, press **F5**. the chrome web browser should open with the running website
4. To run the console code, change `launch.json` to point to `agentic_ai/app.py`.
