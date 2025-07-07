import functools
from typing import Callable, Awaitable, Any

from opentelemetry import trace
try:
    from langfuse import Langfuse
except Exception:
    Langfuse = None  # type: ignore

tracer = trace.get_tracer(__name__)


def traced_llm_call(name: str) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    """Decorator to trace LLM calls using OpenTelemetry and Langfuse.

    If Langfuse is unavailable, tracing still occurs via OpenTelemetry.
    Failures are swallowed to avoid impacting the main application flow.
    """

    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            with tracer.start_as_current_span(name):
                try:
                    lf = Langfuse() if Langfuse else None
                    if lf:
                        lf.trace_start(name)
                except Exception:
                    lf = None
                try:
                    result = await func(*args, **kwargs)
                    if lf:
                        try:
                            lf.trace_success(result)
                        except Exception:
                            pass
                    return result
                except Exception as e:
                    if lf:
                        try:
                            lf.trace_error(e)
                        except Exception:
                            pass
                    raise
        return wrapper

    return decorator
