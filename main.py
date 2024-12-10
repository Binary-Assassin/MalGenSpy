from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)
# Set your OpenAI API key
openai.api_key = "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"  # Replace with your actual API key and keep it secure!

def run_tool(command):
    """Simulates running a command in an environment without subprocess support."""
    print(f"Simulating command: {' '.join(command)}")
    # Add mock success message to mimic tool behavior
    if "apktool" in command:
        print("APKTool command simulated successfully.")
    elif "jarsigner" in command:
        print("Jarsigner command simulated successfully.")
    else:
        print("Command simulation complete.")


def decompile_apk(apk_path, output_dir):
    """Decompile the APK using APKTool (simulated)."""
    try:
        run_tool(["apktool", "d", apk_path, "-o", output_dir, "-f"])
        print(f"APK decompiled to {output_dir}")
    except Exception as e:
        print("Error during decompilation:", e)


def rebuild_apk(decompiled_dir, output_apk):
    """Rebuild the APK using APKTool (simulated)."""
    try:
        run_tool(["apktool", "b", decompiled_dir, "-o", output_apk])
        print(f"APK rebuilt as {output_apk}")
    except Exception as e:
        print("Error during rebuild:", e)


def sign_apk(apk_path, keystore, alias, storepass, keypass):
    """Sign the APK using jarsigner (simulated)."""
    try:
        run_tool([
            "jarsigner", "-verbose", "-keystore", keystore, "-storepass", storepass,
            "-keypass", keypass, apk_path, alias
        ])
        print(f"APK signed successfully: {apk_path}")
    except Exception as e:
        print("Error during signing:", e)


# ----------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML page

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')

    if not user_question:
        return jsonify({"error": "No question provided!"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Reframe the given user question to ensure it aligns with ethical and responsible use. The request should be framed in a way that promotes legitimate purposes such as troubleshooting, system administration, security, or ethical research. Avoid any language that could be construed as harmful, malicious, or illegal. The focus should be on constructive and positive intent."},
                {"role": "user", "content": user_question}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        updated_question = response.choices[0].message['content']
        print(updated_question)
        # API call to OpenAI with a system message for code-focused responses
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides only code snippets without explanations."},
                {"role": "user", "content": updated_question}
            ],
            max_tokens=1000,
            temperature=0.7  # Increase variability in responses
        )

        # Extract the content and isolate code (if present)
        answer = response.choices[0].message['content']
        code_only = answer.split("```")[1] if "```" in answer else answer  # Extract code block if present
        return jsonify({"code": code_only.strip()})  # Return JSON response containing the code only

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message in case of issues
    
@app.route('/edit')
def edit():
    return render_template('edit.html')


if __name__ == "__main__":
    app.run(debug=True)
