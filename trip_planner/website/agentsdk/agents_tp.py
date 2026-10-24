from agents import Agent, WebSearchTool, function_tool, ModelSettings
from openai.types.shared import Reasoning
from pydantic import BaseModel

class TripProfile(BaseModel):
    ctrl_status: str
    ctrl_instructions: str
    data_city: str
    data_budget: str
    data_interests: list[str]

class PlanItem(BaseModel):
    title: str
    price_usd: float
    why_included: str

class PlanItems(BaseModel):
    items: list[PlanItem]
    # city_url: str

class HTMLOutput(BaseModel):
    html: str

class SafetyCheckOut(BaseModel):
    is_safe_and_relavant: bool
    reasoning: str


auth_guard_agent = Agent(
    name="guardrail",
    instructions=(
        "Make sure the user provides the text CSCI8250 before processing any other prompts."
        "This value only needs to be provided once in the current session."
        "If this hasn't been done, set is_safe_and_relavant = False and explain briefly in reasoning without providing the expected keyword."
        "Otherwise set is_safe_and_relavant = True."
    ),
    output_type=SafetyCheckOut,
    model="gpt-6-luna"
)

safety_guard_agent = Agent(
    name="guardrail",
    instructions=(
        "If the user text contains harassment, hate speech, illegal requests, or the word purple, "
        "set is_safe_and_relavant = False and explain briefly in reasoning. Otherwise set is_safe_and_relavant = True."
    ),
    output_type=SafetyCheckOut,
    model="gpt-6-luna"
)


profile_agent = Agent(
    name="profile",
    instructions=(
        "You are a friendly and helpful travel assistant.\n"
        "Your goal is to collect a complete travel profile from the user by asking questions.\n"
        "Ask questions ONE AT A TIME until all of the following fields are known:\n"
        "- Destination city\n"
        "- Total budget in USD\n"
        "- Interests\n"
        "Multiple interests can be provided.  Ask the user for more until you have 1-3 interests or they indicate they don't have more interests."
        "Consolidated details into a TripProfile object.\n"
        "Additional instructions should be placed in the ctrl_instructions field.\n"
        "If you have all the necessary information ctrl_status should be COMPLETE, otherwise ctrl_status is NOTCOMPLETE."
    ),
    output_type=TripProfile,
    model="gpt-6-astra"
)

formatter_agent = Agent(
    name="formatter",
    instructions=(
        "Turn the activity list into a summary formatted in html to be displayed inside a div.\n"
        "Include the estimated total cost at the bottom.\n"
    ),
    output_type=HTMLOutput,
    model="gpt-6-luna"
)

planner_agent = Agent(
    name="planner",
    instructions=(
        "You are a travel planner creating a list of activities for a 1 day trip.\n"
        "The user's completed TripProfile provides information in the context.\n"
        "You must create a plan that reflects the user's interests (data_interests) in the city (data_city).\n"
        "The cost of the planned activities must not exceed the budget (data_budget).\n"
        "Limit the number of PlanItems to 3 items."
    ),
    output_type=PlanItems,
    model="gpt-6-astra"
    # tools=[WebSearchTool()],
    #handoffs=[formatter_agent]
)


@function_tool
def broken_tool() -> str:
    raise RuntimeError("TEST ERROR: Tool failed")

test_agent = Agent(
    name="test_agent",
    instructions=(
        "You are a helpful assistant."
    ),
    tools=[broken_tool]
)



# @input_guardrail
# async def safety_guardrail(ctx, agent, input_data):
#     result = await Runner.run(safety_guard_agent, input_data, context=ctx.context)
#     final_output = result.final_output_as(SafetyCheckOut)
#     return GuardrailFunctionOutput(
#         output_info=final_output.reasoning,
#         tripwire_triggered=not final_output.is_safe_and_relavant,
#     )
# # end guardrail

# "Get one photo of the city and put the URL in city_url.  Make sure the URL is valid.\n"

    # model_settings=ModelSettings(
    #     reasoning=Reasoning(effort="medium"))