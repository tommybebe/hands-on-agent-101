## Tools
LLM의 한계를 극복하기 위해, ADK는 에이전트가 외부 시스템과 상호작용할 수 있는 도구(tool)를 제공합니다. 도구는 LLM의 기능을 확장하여 API 호출, 데이터베이스 쿼리, 계산 등 다양한 작업을 수행할 수 있게 합니다.

### Types of Tools in ADK
- Funcion Tools: Python 함수를 도구로 변환하여 LLM이 이해하고 실행할 수 있도록 합니다.
- Built-in Tools: ADK에서 제공하는 기본 도구로, LLM이 외부 API와 상호작용할 수 있게 합니다.
- Third-party Tools: LangChain, Crew AI와 연동합니다. 
- Google Cloud Tools: Google Cloud의 다양한 서비스와 통합하여 사용할 수 있습니다.
- MCP Tools: MCP 사용할 수 있습니다.


### Decorators
`@tool` 데코레이터(decorator) 또는 어노테이션(annotation)을 사용하여 함수를 도구로 변환할 수 있습니다. ADK는 이 함수를 LLM이 이해하고 실행할 수 있는 형식으로 자동 변환합니다.

```python
from adk.tools import tool

@tool
def get_current_weather(location: str, unit: str = "celsius") -> str:
    """
    Get the current weather for a given location.

    Args:
        location: The city and state, e.g. San Francisco, CA
        unit: The unit to use for the temperature, e.g. celsius or fahrenheit
    """
    # 이 함수는 실제 날씨 API를 호출할 수 있습니다.
    return f"The weather in {location} is 22 degrees {unit}."

agent = Agent(
    # ...
    tools=[get_current_weather]
)
```
