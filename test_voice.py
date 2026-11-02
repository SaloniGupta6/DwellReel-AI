from backend.app.services.voice_generator import generate_voice

script = """
Welcome to The Grand Residence, an exceptional living
experience in Chandigarh. Discover a beautifully designed
three-bedroom apartment with spacious interiors and a
modern modular kitchen. Contact us today to schedule your visit.
"""

output = generate_voice(
    text=script,
    output_path="backend/outputs/test_narration.mp3",
    voice="en-IN-NeerjaNeural",
    style="luxury",
    speed="normal",
)

print("Voice generated successfully!")
print("Audio file:", output)