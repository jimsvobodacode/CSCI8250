from agents import Runner, SQLiteSession, InputGuardrailTripwireTriggered
from website.agentsdk.logging_hooks import LoggingHooks
from website.agentsdk.agents_tp import (profile_agent, safety_guard_agent, auth_guard_agent, 
    TripProfile, SafetyCheckOut)
from django.conf import settings
from pathlib import Path


class AgenticAI:
    def __init__(self):
        self._HOOKS = LoggingHooks()
        self.Profile = None

    def Process(self, conversation_id, prompt):
        try:
            AGENT_DB = Path(settings.BASE_DIR) / "agent_sessions.sqlite3"
            session = SQLiteSession(conversation_id, AGENT_DB)

            result = Runner.run_sync(auth_guard_agent, prompt, session=session, hooks=self._HOOKS)
            guardrail = result.final_output_as(SafetyCheckOut)
            if guardrail.is_safe_and_relavant:
                result = Runner.run_sync(safety_guard_agent, prompt, session=session, hooks=self._HOOKS)
                guardrail = result.final_output_as(SafetyCheckOut)

                if guardrail.is_safe_and_relavant:
                    result = Runner.run_sync(profile_agent, prompt, session=session, hooks=self._HOOKS)
                    self.Profile = result.final_output_as(TripProfile)
                else:
                    self.Profile = TripProfile(ctrl_status="NOTCOMPLETE", ctrl_instructions=f"Inappropriate Prompt: {guardrail.reasoning}",
                        data_city="", data_budget="")
            else:
                self.Profile = TripProfile(ctrl_status="NOTCOMPLETE", ctrl_instructions=f"Auth Guardrail: {guardrail.reasoning}",
                    data_city="", data_budget="")
        except BaseException as ex:
            self.Profile = TripProfile(ctrl_status="NOTCOMPLETE", ctrl_instructions=f"Caught a BaseException: {type(ex).__name__} - {ex}",
                data_city="", data_budget="")
            