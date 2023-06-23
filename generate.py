import openai

def generate_response(prompt): 
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt= prompt,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
) 
        return response
    