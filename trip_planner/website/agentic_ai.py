from agents import Runner, SQLiteSession, InputGuardrailTripwireTriggered
from website.agentsdk.logging_hooks import LoggingHooks
from website.agentsdk.agents_tp import (profile_agent, planner_agent, test_agent, 
    safety_guard_agent, auth_guard_agent, 
    TripProfile, PlanItems, SafetyCheckOut)
from django.conf import settings
from pathlib import Path


class AgenticAI:
    def __init__(self):
        self._HOOKS = LoggingHooks()
        self.Profile = None
        self.PlanItems = None

    def Process(self, conversation_id, prompt):
        try:
            AGENT_DB = Path(settings.BASE_DIR) / "agent_sessions.sqlite3"
            session = SQLiteSession(conversation_id, AGENT_DB)

            # test
            # result = Runner.run_sync(test_agent, "call broken tool", session=session, hooks=self._HOOKS)
            # output = result.final_output

            result = Runner.run_sync(auth_guard_agent, prompt, session=session, hooks=self._HOOKS)
            guardrail = result.final_output_as(SafetyCheckOut)
            if guardrail.is_safe_and_relavant:
                result = Runner.run_sync(safety_guard_agent, prompt, session=session, hooks=self._HOOKS)
                guardrail = result.final_output_as(SafetyCheckOut)

                if guardrail.is_safe_and_relavant:
                    result = Runner.run_sync(profile_agent, prompt, session=session, hooks=self._HOOKS)
                    self.Profile = result.final_output_as(TripProfile)
                    if self.Profile.ctrl_status == "COMPLETE":
                        self.build_trip(session)
                else:
                    self.Profile = TripProfile(ctrl_status="NOTCOMPLETE", ctrl_instructions=f"Inappropriate Prompt: {guardrail.reasoning}",
                        data_city="", data_budget="", data_interests=[])
            else:
                self.Profile = TripProfile(ctrl_status="NOTCOMPLETE", ctrl_instructions=f"Auth Guardrail: {guardrail.reasoning}",
                    data_city="", data_budget="", data_interests=[])
        except BaseException as ex:
            self.Profile = TripProfile(ctrl_status="NOTCOMPLETE", ctrl_instructions=f"Caught a BaseException: {type(ex).__name__} - {ex}",
                data_city="", data_budget="", data_interests=[])

    def build_trip(self, session):
        prompt = (
            f"Plan a 1-day trip to {self.Profile.data_city} with a budget of {self.Profile.data_budget} USD. "
            f"The traveler is interested in {', '.join(self.Profile.data_interests)} "
        )

        result = Runner.run_sync(planner_agent, prompt, session=session, hooks=self._HOOKS, context=self.Profile.model_dump())
        self.PlanItems = result.final_output_as(PlanItems)