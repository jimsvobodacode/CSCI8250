from agents import Agent, Runner, GuardrailFunctionOutput, input_guardrail
from pydantic import BaseModel

class TripProfile(BaseModel):
    ctrl_status: str
    ctrl_instructions: str
    data_city: str
    data_budget: str


# start input guardrail
class SafetyCheckOut(BaseModel):
    is_safe_and_relavant: bool
    reasoning: str


safety_guard_agent = Agent(
    name="guardrail",
    instructions=(
        "If the user text contains harassment, hate speech, illegal requests, or the word purple, "
        "set is_safe_and_relavant = False and explain briefly in reasoning. Otherwise set is_safe_and_relavant = True."
    ),
    output_type=SafetyCheckOut,
    model="gpt-5.6-luna",
)

@input_guardrail
async def safety_guardrail(ctx, agent, input_data):
    result = await Runner.run(safety_guard_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(SafetyCheckOut)
    return GuardrailFunctionOutput(
        output_info=final_output.reasoning,
        tripwire_triggered=not final_output.is_safe_and_relavant,
    )
# end guardrail


profile_agent = Agent(
    name="profile",
    instructions=(
        "You are a friendly and helpful travel assistant.\n"
        "Your goal is to collect a complete travel profile from the user by asking questions.\n"
        "Ask questions ONE AT A TIME until all of the following fields are known:\n"
        "- Destination city\n"
        "- Total budget in USD\n"
        "Consolidated details into a TripProfile object.\n"
        "Additional instructions should be placed in the ctrl_instructions field\n"
        "If you have all the necessary information ctrl_status should be COMPLETE, otherwise ctrl_status is NOTCOMPLETE."
    ),
    output_type=TripProfile,
    input_guardrails=[safety_guardrail],
    model="gpt-5.6-luna",
)





