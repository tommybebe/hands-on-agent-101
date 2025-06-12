## Agent

Agent를 효과적으로 구축하려면 몇 가지 구성 요소를 정의해야 합니다.
1. Identity: 에이전트에게 고유한 이름과 설명을 부여하고, 기반이 될 LLM을 지정합니다.
2. model: 에이전트가 사용할 LLM Model을 지정합니다.
3. description: 에이전트의 목적과 기능을 설명합니다.
4. Instructions: 에이전트가 따라야 할 지침을 제공합니다.
5. Tools: 에이전트가 외부와 상호 작용하거나 계산을 수행하는 등 LLM의 능력을 확장할 수 있도록 도구를 갖추게 합니다.

### Reference 
- [https://google.github.io/adk-docs/agents/](https://google.github.io/adk-docs/agents/)

### Agent 생성하기
ADK를 사용하여 에이전트를 생성하려면, `Agent` 클래스를 사용하여 ID, 설명 및 모델을 지정해야 합니다.
```python
from adk.agents import Agent

root_agent = Agent(
    name="hello_world_agnet",
    model="gemini-2.0-flash",
    description=(
        "Just a simple agent that says hello to the user. "
        "It does not use any tools or advanced features, just a basic interaction"
    ),
    instruction=(
        "whatever user says, just say hello back."
    )
)
```


| 구성요소 | 목적 (Purpose) | 비유 (Analogy) | 내용 예시 (Example Content) |
| :--- | :--- | :--- | :--- |
| **`name (id)`** | Agent를 고유하게 식별하는 이름 | **주민등록번호, 사원번호** | `"weather-booking-agent"` |
| **`model`** | 추론과 생성을 담당하는 Agent의 두뇌 역할 | **두뇌 (Brain)** | `"gemini-1.5-pro"` |
| **`description`** | Agent가 **'무엇'**인지, 그 정체성과 핵심 기능을 정의 | **직무 기술서 (Job Description)** | `"날씨 정보를 알려주고 항공편을 예약하는 Agent"` |
| **`instruction`** | Agent가 **'어떻게'** 행동해야 하는지 상세한 규칙과 방식을 지시 | **업무 매뉴얼 (Work Manual)** | `"당신은 친절한 비서입니다. 날씨를 먼저 확인한 후 예약 가능 여부를 알려주세요."` |
| **`tools`** | 외부 시스템과 상호작용하며 실제 행동을 수행하는 능력 확장 | **팔과 다리, 도구 상자 (Toolbox)** | `[get_weather, book_flight]` |

#### Model 
ADK는 Google Gemini 모델을 기본적으로 사용합니다.
```python
from google.adk.agents import LlmAgent

agent = LlmAgent(
    model="gemini-2.0-flash",
    name="gemini_flash_agent",
    # ... other agent parameters
)
```
그 외 다른 모델의 사용은 liteLLM을 통해 가능합니다. 
```
pip install litellm
```

```python
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

agent_openai = LlmAgent(
    model=LiteLlm(model="openai/gpt-4o"),
    name="openai_agent",
    instruction="You are a helpful assistant powered by GPT-4o.",
    # ... other agent parameters
)
```

#### Description
에이전트의 설명은 에이전트가 수행할 수 있는 작업과 기능을 명확하게 정의해야 합니다. 이는 에이전트의 목적과 사용 사례를 이해하는 데 도움이 됩니다. 설명은 간결하고 명확해야 하며, 에이전트가 어떤 문제를 해결할 수 있는지 또는 어떤 서비스를 제공할 수 있는지를 강조해야 합니다.


#### Instruction

Description과 달리 Instruction은 Agent의 행동과 결과에 직접적인 영향을 미치는 지침입니다. 이는 에이전트가 사용자와 상호 작용할 때 따르는 규칙과 절차를 정의합니다. 좋은 지침은 에이전트가 일관되게 행동하고, 사용자에게 유용한 정보를 제공하며, 예상치 못한 상황에서도 올바르게 대응할 수 있도록 합니다.

지침에는 다음 요소들이 포함될 수 있습니다:

* 핵심 과업: 에이전트가 수행해야 할 주요 기능이나 목표를 설명합니다.
* 성격: 에이전트가 응답할 때 채택해야 할 목소리와 톤을 정의합니다. (예: "당신은 친절하고 도움이 되는 비서입니다.")
* 제약 조건: 에이전트가 따라야 할 규칙이나 제한 사항을 명시합니다. (예: "절대로 개인 정보를 묻지 마세요.")
* 도구 사용법: 에이전트가 사용 가능한 도구를 언제 어떻게 사용해야 하는지 안내합니다.

```python
from adk.agents import Agent

agent = Agent(
    # ...
    instructions=(
        "You are a helpful assistant that can answer questions and use tools. "
        "- If you can answer a question without using a tool, do so. "
        "- If you need to use a tool, explain which tool you are using and why. "
        "- If you don't know the answer, say so. "
    )
)
```

### Hands-on Example
- 새로운 폴더를 생성해 새 에이전트를 위한 코드를 작성합니다.
- [agent.py](agent.py)를 참조하세요. 
