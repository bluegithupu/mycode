import gradio as gr

def calculator(a, b, operation):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b != 0:
            return a / b
        else:
            return "Error: Division by zero"

iface = gr.Interface(
    fn=calculator,
    inputs=["number", "number", gr.inputs.Dropdown(["add", "subtract", "multiply", "divide"])],
    outputs="text"
)

iface.launch()