from agents import Runner, SQLiteSession, InputGuardrailTripwireTriggered
from logging_hooks import LoggingHooks
from agents_tp import profile_agent, TripProfile

HOOKS = LoggingHooks()

# NOTE: you will need to set the environment variable OPENAI_API_KEY on your PC for this to work
def main():
    session = SQLiteSession("trip_planner_chat")
    print("Trip Planner - Please tell me about your trip. I need city and budget.")

    while True:
        try:
            prompt = input("> ").strip()
            if not prompt:
                continue

            try:
                result = Runner.run_sync(profile_agent, prompt, session=session, hooks=HOOKS)

                profile = result.final_output_as(TripProfile)
                
                print(profile)
                

            except InputGuardrailTripwireTriggered:
                print("Input guardrail tripwire triggered.")
                print(f"Please provide relevant information about your trip.")
                continue
            

        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            break


if __name__ == "__main__":
    main()