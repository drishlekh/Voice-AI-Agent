
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any, Callable

import pandas as pd
from livekit.agents.metrics import LLMMetrics, STTMetrics, TTSMetrics, EOUMetrics
from livekit.plugins import groq, deepgram, elevenlabs

# --- Configuration & State ---
METRICS_FILE = "all_metrics.csv"
_all_metrics_data: List[Dict] = []  # Internal state

# Map for renaming columns with their units
_COLUMN_UNITS_MAP = {
    'ttft': 'ttft_s',
    'duration': 'processing_duration_s',
    'audio_duration': 'audio_duration_s',
    'end_of_utterance_delay': 'eou_delay_s',
    'transcription_delay': 'transcription_delay_s',
    'ttfb': 'ttfb_s'
}

# --- Internal Helper Functions ---

def _format_llm_metrics(metrics: LLMMetrics) -> str:
    return (
        "🧠 LLM Metrics:\n"
        f"  Prompt Tokens: {metrics.prompt_tokens}\n"
        f"  Completion Tokens: {metrics.completion_tokens}\n"
        f"  Tokens/s: {metrics.tokens_per_second:.1f}\n"
        f"  TTFT: {metrics.ttft:.3f}s"
    )

def _format_stt_metrics(metrics: STTMetrics) -> str:
    return (
        "🎤 STT Metrics:\n"
        f"  Processing: {metrics.duration:.3f}s\n"
        f"  Audio Duration: {metrics.audio_duration:.3f}s\n"
        f"  Streamed: {'✅' if metrics.streamed else '❌'}"
    )

def _format_eou_metrics(metrics: EOUMetrics) -> str:
    return (
        "⏹️  EOU Metrics:\n"
        f"  Silence Delay: {metrics.end_of_utterance_delay:.3f}s\n"
        f"  Transcription Delay: {metrics.transcription_delay:.3f}s"
    )

def _format_tts_metrics(metrics: TTSMetrics) -> str:
    return (
        "🔊 TTS Metrics:\n"
        f"  TTFB: {metrics.ttfb:.3f}s\n"
        f"  Processing: {metrics.duration:.3f}s\n"
        f"  Audio Duration: {metrics.audio_duration:.3f}s\n"
        f"  Streamed: {'✅' if metrics.streamed else '❌'}"
    )

async def _handle_and_save_metric(
    metrics: Any,
    metric_type: str,
    formatter: Callable[[Any], str]
):
    """Internal handler to process, format, and save a single metric event."""
    logging.info(formatter(metrics))

    data = vars(metrics)
    data = {
        key: round(value, 3) if isinstance(value, float) else value
        for key, value in data.items()
    }
    data['timestamp'] = datetime.now().isoformat()
    data['metric_type'] = metric_type

    _all_metrics_data.append(data)

    try:
        df = pd.DataFrame(_all_metrics_data)
        df = df.rename(columns=_COLUMN_UNITS_MAP)

        preferred_order = ['timestamp', 'metric_type']
        all_cols = df.columns.tolist()
        final_cols = preferred_order + [col for col in all_cols if col not in preferred_order]
        df = df[final_cols]

        df.to_csv(METRICS_FILE, index=False)
        logging.info(f"Updated {METRICS_FILE}")
    except Exception as e:
        logging.error(f"Failed to write metrics to CSV: {e}")

# --- Public API Function ---

def setup_metrics_logging(llm: groq.LLM, stt: deepgram.STT, tts: elevenlabs.TTS):
    """
    Wires up the metrics event listeners for the agent's services to the CSV logger.
    """
    logging.info("Setting up metrics logging to CSV...")
    
    llm.on("metrics_collected", lambda m: asyncio.create_task(
        _handle_and_save_metric(m, "LLM", _format_llm_metrics)
    ))
    stt.on("metrics_collected", lambda m: asyncio.create_task(
        _handle_and_save_metric(m, "STT", _format_stt_metrics)
    ))
    stt.on("eou_metrics_collected", lambda m: asyncio.create_task(
        _handle_and_save_metric(m, "EOU", _format_eou_metrics)
    ))
    tts.on("metrics_collected", lambda m: asyncio.create_task(
        _handle_and_save_metric(m, "TTS", _format_tts_metrics)
    ))