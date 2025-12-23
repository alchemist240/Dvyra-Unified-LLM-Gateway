import os
import requests
import asyncio
from typing import Optional, Dict, Any
from litellm.integrations.custom_logger import CustomLogger

# Ensure you have this environment variable set
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

class SlackAlertLogger(CustomLogger):
    def __init__(self):
        if not SLACK_WEBHOOK_URL:
            print("⚠️ SLACK_WEBHOOK_URL not set. Custom alerts will not fire.")

    #### 1. SUCCESS HOOK (High Latency Alerts) ####
    async def async_post_call_success_hook(self, **kwargs):
        """
        Uses **kwargs to accept any arguments LiteLLM sends, 
        preventing 'missing positional arguments' errors.
        """
        if not SLACK_WEBHOOK_URL:
            return

        try:
            # Extract arguments safely from the dictionary
            start_time = kwargs.get("start_time")
            end_time = kwargs.get("end_time")
            model = kwargs.get("model")
            
            # We check if we have the timing data needed
            if start_time is None or end_time is None:
                return

            # FIX: Calculate total seconds correctly
            time_diff = end_time - start_time
            latency = round(time_diff.total_seconds(), 2)

            # Trigger only if latency > 2.0s
            if latency > 2.0:
                await self._send_alert(
                    f"⚠️ *High Latency Detected*\n"
                    f"*Model:* `{model}`\n"
                    f"*Latency:* `{latency}s`"
                )
        except Exception as e:
            print(f"Error in success hook: {e}")

    #### 2. FAILURE HOOK (Error Alerts) ####
    async def async_post_call_failure_hook(self, **kwargs):
        if not SLACK_WEBHOOK_URL:
            return

        try:
            # Extract specific arguments for failure
            model = kwargs.get("model")
            original_exception = kwargs.get("original_exception")
            # Fallback if 'original_exception' is named differently (e.g. 'error')
            if not original_exception:
                original_exception = kwargs.get("error", "Unknown Error")

            await self._send_alert(
                f"🚨 *LiteLLM Provider Failure*\n"
                f"*Model:* `{model}`\n"
                f"*Error:* `{str(original_exception)}`"
            )
        except Exception as e:
            print(f"Error in failure hook: {e}")

    #### HELPER ####
    async def _send_alert(self, message: str):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            lambda: requests.post(
                SLACK_WEBHOOK_URL,
                json={"text": message},
                timeout=5,
            ),
        )

# ==========================================
# INSTANTIATE THE OBJECT
# ==========================================
proxy_handler_instance = SlackAlertLogger()