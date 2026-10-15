import gradio as gr
from src.services.ai_service import generate_response


def build_ui() -> gr.Blocks:
    """
    Constructs the Gradio web interface for SortSmart.

    Architectural Principle: The UI communicates strictly with `generate_response()`
    in the AI service layer and never directly with Ollama or the model client.
    """
    with gr.Blocks(title="SortSmart: AI Recycling Guide") as demo:
        gr.Markdown(
            """
            # ♻️ SortSmart: An AI Recycling Guide
            Describe a household item you want to dispose of (e.g., *"empty plastic yoghurt cup with foil lid"*, *"greasy pizza box"*, or *"used paper towel"*).
            SortSmart retrieves documented sorting rules and explains which waste category to use.
            """
        )

        with gr.Row():
            with gr.Column():
                user_input = gr.Textbox(
                    lines=3,
                    placeholder="e.g., empty plastic yoghurt cup, greasy pizza box, dead AA battery...",
                    label="What item do you want to dispose of?",
                )
                submit_btn = gr.Button("Find Waste Category", variant="primary")

            with gr.Column():
                output_box = gr.Textbox(
                    lines=8,
                    label="Sorting Guidance & Rule Source",
                    interactive=False,
                )

        submit_btn.click(
            fn=generate_response,
            inputs=user_input,
            outputs=output_box,
        )
        user_input.submit(
            fn=generate_response,
            inputs=user_input,
            outputs=output_box,
        )

    return demo