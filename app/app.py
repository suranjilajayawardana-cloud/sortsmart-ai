import gradio as gr
import sys
import os

# Ensure the src folder can be imported correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.services.ai_service import generate_response

def chat_interface(user_input):
    return generate_response(user_input)

# UI Implementation
with gr.Blocks(title="SortSmart: AI Recycling Guide") as demo:
    gr.Markdown("# ♻️ SortSmart")
    gr.Markdown("Describe a waste item, and AI will check local rules to tell you how to sort it.")
    
    with gr.Row():
        with gr.Column():
            item_input = gr.Textbox(label="What do you want to throw away?", placeholder="e.g., greasy pizza box, empty yogurt cup")
            submit_btn = gr.Button("Find Waste Category")
        with gr.Column():
            output_display = gr.Textbox(label="Sorting Instructions", interactive=False, lines=4)
            
    submit_btn.click(fn=chat_interface, inputs=item_input, outputs=output_display)
    item_input.submit(fn=chat_interface, inputs=item_input, outputs=output_display)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)