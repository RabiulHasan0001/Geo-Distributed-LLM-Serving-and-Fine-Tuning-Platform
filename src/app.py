from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

# ✅ Your IP Address and Port
LOCAL_IP = "192.168.0.103"
PORT = 8001  # Keep the same or change as needed

# ✅ Load GPT-2 Medium (Better Model)
MODEL_NAME = "gpt2-medium"  # Upgraded model for better responses
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# ✅ Improved Web Interface (HTML)
@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Chatbot</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f4f4f4;
            }}
            h1 {{
                color: #333;
            }}
            textarea {{
                width: 80%;
                height: 120px;
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }}
            button {{
                padding: 10px 20px;
                font-size: 18px;
                margin-top: 10px;
                cursor: pointer;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
            }}
            button:hover {{
                background-color: #0056b3;
            }}
            #response {{
                margin-top: 20px;
                font-size: 18px;
                background: #fff;
                padding: 15px;
                border-radius: 5px;
                width: 80%;
                text-align: left;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            }}
            .loader {{
                display: none;
                border: 4px solid #f3f3f3;
                border-top: 4px solid #007BFF;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                margin: 10px auto;
            }}
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        </style>
    </head>
    <body>
        <h1>AI Chatbot</h1>
        <p>Enter your text below and click submit:</p>
        <textarea id="user_input" placeholder="Type something..."></textarea><br>
        <button onclick="sendRequest()">Submit</button>
        <div class="loader" id="loading"></div>
        <div id="response"></div>

        <script>
            async function sendRequest() {{
                const inputText = document.getElementById("user_input").value;
                const responseDiv = document.getElementById("response");
                const loader = document.getElementById("loading");

                if (inputText.trim() === "") {{
                    responseDiv.innerHTML = "<strong style='color:red;'>Please enter some text.</strong>";
                    return;
                }}

                responseDiv.innerHTML = "";
                loader.style.display = "block";
                
                const response = await fetch("http://{LOCAL_IP}:{PORT}/predict/", {{
                    method: "POST",
                    headers: {{
                        "Content-Type": "application/json"
                    }},
                    body: JSON.stringify({{"prompt": inputText}})
                }});

                loader.style.display = "none";
                const result = await response.json();
                responseDiv.innerHTML = "<strong>Response:</strong> " + result.response;
            }}
        </script>
    </body>
    </html>
    """

# ✅ Improved Response Generation
@app.post("/predict/")
async def generate_text(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_length=80,  # ⬅️ Extended but limited to avoid excessive repetition
        num_return_sequences=1,
        temperature=0.6,  # ⬅️ Lower temp for more structured responses
        top_p=0.85,  # ⬅️ Better word selection with nucleus sampling
        repetition_penalty=1.3  # ⬅️ Stronger penalty to prevent looping
    )
    
    return {"response": tokenizer.decode(outputs[0], skip_special_tokens=True)}

# ✅ Run the FastAPI Server with Your IP and Port
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=LOCAL_IP, port=PORT)
