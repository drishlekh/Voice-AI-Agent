import asyncio
from dotenv import load_dotenv
import logging

load_dotenv()

from livekit.agents import Agent, AgentSession, cli, WorkerOptions, JobContext
from livekit.plugins import groq, elevenlabs, deepgram, silero


from metrics_logger import setup_metrics_logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logging.getLogger("livekit").setLevel(logging.WARNING) 


async def entrypoint(ctx: JobContext):
    """The main entrypoint for the voice agent."""
    logging.info("Agent job starting...")
    await ctx.connect()
    logging.info("Connected to the room.")

    # 1. Initialize all the services for the agent
    stt = deepgram.STT()
    llm = groq.LLM()
    tts = elevenlabs.TTS()
    vad = silero.VAD.load()

    # 2. Set up the metrics logging by passing the services to our logger module
    #    This single call replaces all the individual .on() calls here.
    setup_metrics_logging(llm=llm, stt=stt, tts=tts)

    # 3. Create the agent session
    session = AgentSession(
        stt=stt,
        llm=llm,
        tts=tts,
        vad=vad,
    )

    # 4. Define the agent's identity and behavior
    agent = Agent(
        instructions="You are a helpful AI voice assistant. Keep responses short and conversational."
    )
    
    # 5. Start the agent session
    logging.info("Starting agent session...")
    await session.start(room=ctx.room, agent=agent)
    logging.info("Agent session finished.")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))