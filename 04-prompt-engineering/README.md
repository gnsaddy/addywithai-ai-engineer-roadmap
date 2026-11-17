# Prompt Engineering: code from the video (AI Engineer Roadmap, Episode 4)
Three tiny Python demos. No packages and no API key needed (Python 3.9+, standard library only).

## Run
```
python prompt_template.py
python structured_output.py
python function_calling.py
```

## Files
- `prompt_template.py`: a reusable prompt template. A system prompt, two few-shot examples and a user template
  with one `$message` slot, built into a chat `messages` list (the format every chat API uses).
- `structured_output.py`: asks for JSON only, then checks the reply with `json.loads()` plus a small schema
  (keys, types, allowed values). Tested on three sample replies (no model call).
- `function_calling.py`: a tool description in JSON schema, the real Python function, and the tool loop:
  model asks for a tool, your code checks and runs it, the result goes back, the model answers.

## Notes
- `stand_in_model()` in `function_calling.py` is an offline stand-in that returns fixed replies, so the demo runs
  without a key. In a real app, replace it with your provider's chat call and pass `TOOLS` as its tools.
- Many APIs can enforce a JSON schema for you ("structured outputs"). Still validate the result in your code.
- Never let the model run any function it names: only the ones in your `FUNCTIONS` allow-list.
