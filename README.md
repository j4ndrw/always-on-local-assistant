# Lola - My Always-On Local Assistant

> [!WARNING]
> This software is designed to work exclusively on my mobile device and is not intended to be used as a service or consumer application. You can do whatever you want with it, but be aware that it might not work as expected for your use case.

I created this software because I wanted an alternative to assistants like Google Assistant (or Gemini), Alexa, and others that operates offline and that I can control myself. I don't feel comfortable using a voice assistant, or any AI-based tool for that matter, without visibility into how data is transferred to third parties.

Additionally, this software represents a learning experience for me, as it has provided hands-on experience with:

- The Android SDK (which I don't particularly like, but it's beneficial to understand how things work now)
- Making an LLM agentic via tools and function calling
- Implementing text-to-speech and speech-to-text using open-source models, rather than built-in capabilities:
    - [Vosk](https://github.com/alphacep/vosk) was used for speech to text
    - [Piper](https://github.com/rhasspy/piper) was used for text to speech

Also, note that the architecture of this software is not great - I cut a lot of corners and disregarded lots of edge cases. Since I'm the only user of this software,
I don't really case what issues other people discover. If I discover issues, I will fix them myself on the spot.
