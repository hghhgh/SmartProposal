from normalizer import normalize_model_output

def run():
    # 1) شبیه OpenAI Chat Completions
    raw_openai_chat = {
        "id": "chatcmpl_x",
        "choices": [{"message": {"role": "assistant", "content": "سلام! خروجی چت."}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
    }

    # 2) شبیه OpenAI tool_calls
    raw_openai_tool = {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "",
                "tool_calls": [{
                    "id": "call_1",
                    "type": "function",
                    "function": {"name": "get_weather", "arguments": "{\"city\":\"Tehran\"}"}
                }]
            }
        }],
        "usage": {"prompt_tokens": 20, "completion_tokens": 7, "total_tokens": 27}
    }

    # 3)  Anthropic content blocks
    raw_anthropic = {
        "content": [
            {"type": "text", "text": "این یک متن از مدل دیگر است."},
            {"type": "tool_use", "id": "tu_1", "name": "search", "input": {"q": "python"}}
        ],
        "usage": {"input_tokens": 12, "output_tokens": 9}
    }

    n1 = normalize_model_output(raw_openai_chat, provider="openai", model="gpt-x", request_id="r1", latency_ms=111)
    n2 = normalize_model_output(raw_openai_tool, provider="openai", model="gpt-x", request_id="r2", latency_ms=222)
    n3 = normalize_model_output(raw_anthropic, provider="anthropic", model="claude-x", request_id="r3", latency_ms=333)

    # asserts
    assert n1["output"]["text"] == "سلام! خروجی چت."
    assert n1["usage"]["total_tokens"] == 15

    assert n2["output"]["text"] == ""
    assert len(n2["output"]["tool_calls"]) == 1
    assert n2["output"]["tool_calls"][0]["name"] == "get_weather"
    assert n2["output"]["tool_calls"][0]["arguments"]["city"] == "Tehran"

    assert n3["output"]["text"].startswith("این یک متن")
    assert len(n3["output"]["tool_calls"]) == 1
    assert n3["output"]["tool_calls"][0]["name"] == "search"
    assert n3["usage"]["total_tokens"] == (12 + 9)  

    print("✅ ALL NORMALIZATION TESTS PASSED")

if __name__ == "__main__":
    run()
