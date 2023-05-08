import openai


openai.api_key = "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"
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "你是?"}
    ]
)

result = ""
for choice in response.choices:  
    result += choice.message.content
print(result)
