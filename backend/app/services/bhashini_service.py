# bhashini_service.py
"""
BHASHINI Service
================
Connects to BHASHINI's ULCA Pipeline Config API and orchestrates:
    ASR (Speech -> Text)  ->  Translation  ->  TTS (Text -> Speech)

Reads credentials from environment (.env):
    BHASHINI_USER_ID
    BHASHINI_ULCA_API_KEY
    BHASHINI_INFERENCE_API_KEY
    BHASHINI_PIPELINE_ID       (optional)
    BHASHINI_ASR_SERVICE_ID    (optional)
    BHASHINI_TRANSLATION_SERVICE_ID (optional)
    BHASHINI_TTS_SERVICE_ID    (optional)

Author: (you)
"""

import os
import json
import base64
import logging
import requests
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PIPELINE_CONFIG_URL = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class PipelineEndpoints:
    """Resolved model endpoints for a given language pair / task."""
    asr: Optional[Dict[str, Any]] = None
    translation: Optional[Dict[str, Any]] = None
    tts: Optional[Dict[str, Any]] = None
    raw_response: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------

class BhashiniService:
    def __init__(
        self,
        user_id: Optional[str] = None,
        ulca_api_key: Optional[str] = None,
        inference_api_key: Optional[str] = None,
        pipeline_id: Optional[str] = None,
    ):
        self.user_id = user_id or os.getenv("BHASHINI_USER_ID")
        self.ulca_api_key = ulca_api_key or os.getenv("BHASHINI_ULCA_API_KEY")
        self.inference_api_key = inference_api_key or os.getenv("BHASHINI_INFERENCE_API_KEY")
        self.pipeline_id = pipeline_id or os.getenv("BHASHINI_PIPELINE_ID")

        if not all([self.user_id, self.ulca_api_key, self.inference_api_key]):
            raise ValueError(
                "Missing BHASHINI credentials. Set BHASHINI_USER_ID, "
                "BHASHINI_ULCA_API_KEY and BHASHINI_INFERENCE_API_KEY in .env"
            )

    # ------------------------------------------------------------------
    # Pipeline Config API
    # ------------------------------------------------------------------
    def get_pipeline_config(
        self,
        source_lang: str = "en",
        target_lang: str = "hi",
        asr_service_id: Optional[str] = None,
        translation_service_id: Optional[str] = None,
        tts_service_id: Optional[str] = None,
    ) -> PipelineEndpoints:
        """
        Calls BHASHINI's pipeline config API to discover which ASR /
        Translation / TTS models to use for this language pair.
        """
        headers = {
            "userID": self.user_id,
            "ulcaApiKey": self.ulca_api_key,
            "Content-Type": "application/json",
        }

        tasks: List[Dict[str, Any]] = []
        tasks.append({
            "taskType": "asr",
            "config": {"language": {"sourceLanguage": source_lang}},
        })
        tasks.append({
            "taskType": "translation",
            "config": {
                "language": {
                    "sourceLanguage": source_lang,
                    "targetLanguage": target_lang,
                }
            },
        })
        tasks.append({
            "taskType": "tts",
            "config": {"language": {"sourceLanguage": target_lang}},
        })

        payload = {
            "pipelineTasks": tasks,
            "pipelineRequestConfig": {
                "pipelineId": self.pipeline_id or "64392f96daac500b55c543cd"
            },
        }

        logger.info("Requesting pipeline config for %s -> %s", source_lang, target_lang)
        r = requests.post(PIPELINE_CONFIG_URL, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()

        return self._parse_pipeline_response(
            data,
            asr_service_id=asr_service_id,
            translation_service_id=translation_service_id,
            tts_service_id=tts_service_id,
        )

    # ------------------------------------------------------------------
    # Response parsing
    # ------------------------------------------------------------------
    def _parse_pipeline_response(
        self,
        data: Dict[str, Any],
        asr_service_id: Optional[str] = None,
        translation_service_id: Optional[str] = None,
        tts_service_id: Optional[str] = None,
    ) -> PipelineEndpoints:
        endpoints = PipelineEndpoints(raw_response=data)

        # Callback URL + auth header come from the top level
        callback_url = (
            data.get("pipelineInferenceAPIEndPoint", {})
            .get("callbackUrl")
        )
        inference_key_name = (
            data.get("pipelineInferenceAPIEndPoint", {})
            .get("inferenceApiKey", {})
            .get("name", "Authorization")
        )
        inference_key_value = (
            data.get("pipelineInferenceAPIEndPoint", {})
            .get("inferenceApiKey", {})
            .get("value", self.inference_api_key)
        )

        common = {
            "callback_url": callback_url,
            "auth_header_name": inference_key_name,
            "auth_header_value": inference_key_value,
        }

        for task in data.get("pipelineResponseConfig", []):
            task_type = task.get("taskType")
            configs = task.get("config", [])
            if not configs:
                continue

            # Pick requested serviceId if provided, otherwise first
            chosen = None
            wanted = {
                "asr": asr_service_id,
                "translation": translation_service_id,
                "tts": tts_service_id,
            }.get(task_type)

            for c in configs:
                if wanted and c.get("serviceId") == wanted:
                    chosen = c
                    break
            if chosen is None:
                chosen = configs[0]

            endpoint = {
                **common,
                "service_id": chosen.get("serviceId"),
                "language": chosen.get("language"),
                "supported_languages": [
                    s.get("langCode") for s in chosen.get("supportedLanguages", [])
                ] if chosen.get("supportedLanguages") else None,
            }

            if task_type == "asr":
                endpoints.asr = endpoint
            elif task_type == "translation":
                endpoints.translation = endpoint
            elif task_type == "tts":
                endpoints.tts = endpoint

        return endpoints

    # ------------------------------------------------------------------
    # Inference helpers
    # ------------------------------------------------------------------
    def _headers_for(self, endpoint: Dict[str, Any]) -> Dict[str, str]:
        return {
            endpoint.get("auth_header_name", "Authorization"): endpoint.get(
                "auth_header_value", self.inference_api_key
            ),
            "Content-Type": "application/json",
        }

    def speech_to_text(
        self,
        audio_bytes: bytes,
        endpoint: Dict[str, Any],
        source_lang: str = "en",
        audio_format: str = "wav",
        sampling_rate: int = 16000,
    ) -> str:
        """ASR: speech -> text."""
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        payload = {
            "pipelineTasks": [
                {
                    "taskType": "asr",
                    "config": {
                        "language": {"sourceLanguage": source_lang},
                        "audioFormat": audio_format,
                        "samplingRate": sampling_rate,
                    },
                }
            ],
            "inputData": {
                "audio": [{"audioContent": audio_b64}]
            },
        }

        r = requests.post(
            endpoint["callback_url"],
            headers=self._headers_for(endpoint),
            json=payload,
            timeout=60,
        )
        r.raise_for_status()
        result = r.json()

        try:
            return result["pipelineResponse"][0]["output"][0]["source"]
        except (KeyError, IndexError) as e:
            logger.error("ASR parse failed: %s | raw=%s", e, result)
            raise RuntimeError("Failed to parse ASR response") from e

    def translate(
        self,
        text: str,
        endpoint: Dict[str, Any],
        source_lang: str = "en",
        target_lang: str = "hi",
    ) -> str:
        """NMT: text -> translated text."""
        payload = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": source_lang,
                            "targetLanguage": target_lang,
                        }
                    },
                }
            ],
            "inputData": {
                "input": [{"source": text}]
            },
        }

        r = requests.post(
            endpoint["callback_url"],
            headers=self._headers_for(endpoint),
            json=payload,
            timeout=60,
        )
        r.raise_for_status()
        result = r.json()

        try:
            return result["pipelineResponse"][0]["output"][0]["target"]
        except (KeyError, IndexError) as e:
            logger.error("Translation parse failed: %s | raw=%s", e, result)
            raise RuntimeError("Failed to parse translation response") from e

    def text_to_speech(
        self,
        text: str,
        endpoint: Dict[str, Any],
        target_lang: str = "hi",
        gender: str = "female",
    ) -> bytes:
        """TTS: text -> wav bytes."""
        payload = {
            "pipelineTasks": [
                {
                    "taskType": "tts",
                    "config": {
                        "language": {"sourceLanguage": target_lang},
                        "gender": gender,
                    },
                }
            ],
            "inputData": {
                "input": [{"source": text}]
            },
        }

        r = requests.post(
            endpoint["callback_url"],
            headers=self._headers_for(endpoint),
            json=payload,
            timeout=60,
        )
        r.raise_for_status()
        result = r.json()

        try:
            audio_b64 = result["pipelineResponse"][0]["audio"][0]["audioContent"]
            return base64.b64decode(audio_b64)
        except (KeyError, IndexError) as e:
            logger.error("TTS parse failed: %s | raw=%s", e, result)
            raise RuntimeError("Failed to parse TTS response") from e

    # ------------------------------------------------------------------
    # Full voice pipeline
    # ------------------------------------------------------------------
    def voice_pipeline(
        self,
        audio_bytes: bytes,
        source_lang: str = "en",
        target_lang: str = "hi",
        audio_format: str = "wav",
        sampling_rate: int = 16000,
        gender: str = "female",
    ) -> Dict[str, Any]:
        """
        End-to-end: audio(in source_lang) -> text -> translated text -> audio(out target_lang)
        Returns dict with asr_text, translated_text, and tts audio bytes.
        """
        endpoints = self.get_pipeline_config(source_lang, target_lang)

        if not endpoints.asr or not endpoints.translation or not endpoints.tts:
            raise RuntimeError("Incomplete pipeline endpoints resolved from BHASHINI")

        asr_text = self.speech_to_text(
            audio_bytes, endpoints.asr, source_lang, audio_format, sampling_rate
        )
        translated = self.translate(
            asr_text, endpoints.translation, source_lang, target_lang
        )
        audio_out = self.text_to_speech(
            translated, endpoints.tts, target_lang, gender
        )

        return {
            "source_language": source_lang,
            "target_language": target_lang,
            "asr_text": asr_text,
            "translated_text": translated,
            "audio_bytes": audio_out,
        }