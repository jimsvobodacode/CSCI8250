from agents import Runner, SQLiteSession  #, InputGuardrailTripwireTriggered
from website.agentsdk.logging_hooks import LoggingHooks
from website.agentsdk.agents_tp import (profile_agent, planner_agent, safety_guard_agent, formatter_agent, 
    test_agent, auth_guard_agent,
    TripProfile, PlanItems, HTMLOutput, SafetyCheckOut)
from django.conf import settings
from pydantic import BaseModel
from pathlib import Path

class HTMLOutput(BaseModel):
    html: str

class AgenticAI:
    def __init__(self, request):
        self._HOOKS = LoggingHooks()
        self._session = request.session
        self.Profile = None
        self.PlanItems = None
        self.PlanHTML = None

    def Process(self, conversation_id, prompt):
        try:
            AGENT_DB = Path(settings.BASE_DIR) / "agent_sessions.sqlite3"
            ai_session = SQLiteSession(conversation_id, AGENT_DB)

            if self._session.get("auth_guardrail") is None:
                if str(prompt).upper() == "CSCI8250":
                    self._session["auth_guardrail"] = True
                    prompt = ""
            
            if self._session.get("auth_guardrail"):
                result = Runner.run_sync(safety_guard_agent, prompt, session=ai_session, hooks=self._HOOKS)
                guardrail = result.final_output_as(SafetyCheckOut)

                if guardrail.is_safe_and_relavant:
                    result = Runner.run_sync(profile_agent, prompt, session=ai_session, hooks=self._HOOKS)
                    self.Profile = result.final_output_as(TripProfile)
                    if self.Profile.ctrl_status == "COMPLETE":
                        self.build_trip(ai_session)
                else:
                    self.Profile = TripProfile(ctrl_status="NOTCOMPLETE", ctrl_instructions=f"Inappropriate Prompt: {guardrail.reasoning}",
                        data_city="", data_budget="", data_interests=[])
            else:
                self.Profile = TripProfile(ctrl_status="NOTCOMPLETE", ctrl_instructions=f"Auth Guardrail: Auth guardrail invalid",
                    data_city="", data_budget="", data_interests=[])
        except BaseException as ex:
            self.Profile = TripProfile(ctrl_status="NOTCOMPLETE", ctrl_instructions=f"Caught a BaseException: {type(ex).__name__} - {ex}",
                data_city="", data_budget="", data_interests=[])

    def build_trip(self, ai_session):
        prompt = (
            f"Plan a 1-day trip to {self.Profile.data_city} with a budget of {self.Profile.data_budget} USD. "
            f"The traveler is interested in {', '.join(self.Profile.data_interests)} "
        )

        result = Runner.run_sync(planner_agent, prompt, session=ai_session, hooks=self._HOOKS, context=self.Profile.model_dump())
        self.PlanItems = result.final_output_as(PlanItems)

        result = Runner.run_sync(formatter_agent, prompt, session=ai_session, hooks=self._HOOKS, context=self.PlanItems.model_dump())
        self.PlanHTML = result.final_output_as(HTMLOutput)


  # test
            # result = Runner.run_sync(test_agent, "call broken tool", session=session, hooks=self._HOOKS)
            # output = result.final_output
            # if self._session.get("auth_guardrail") is None:
            #     result = Runner.run_sync(auth_guard_agent, prompt, session=session, hooks=self._HOOKS)
            #     auth_guardrail = result.final_output_as(SafetyCheckOut)
            #     self._session["auth_guardrail"] = auth_guardrail