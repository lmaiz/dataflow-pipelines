from functools import cached_property
from datetime import datetime, timezone
from typing import Optional


class SessionStartTransformer:
    def __init__(self, event):
        self._event = event
        self._data = {}
        if event.get("events"):
            self._data = event.get("events")[0].get("data", {})

    def get_session_id(self) -> int:
        if self._data.get("session_id"):
            return int(self._data.get("session_id"))
        return None

    @cached_property
    def session_id(self) -> int:
        """
        Get session_id attribute
        """
        return self.get_session_id()

    def get_mpid(self) -> int:
        return self._event.get("mpid")

    @cached_property
    def mpid(self) -> int:
        """
        Get mpid attribute
        """
        return self.get_mpid()

    def get_session_start_time(self) -> str:
        if self._data.get("session_start_unixtime_ms"):
            return datetime.fromtimestamp(
                int(self._data.get("session_start_unixtime_ms")) / 1000, timezone.utc
            ).strftime("%Y-%m-%dT%H:%M:%S")
        return datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S")

    @cached_property
    def session_start_time(self) -> str:
        """
        Get session_start_time attribute
        """
        return self.get_session_start_time()

    def get_session_end_time(self) -> Optional[str]:
        return None

    @cached_property
    def session_end_time(self) -> str:
        """
        Get session_end_time attribute
        """
        return self.get_session_end_time()

    def get_session_duration(self) -> Optional[int]:
        return None

    @cached_property
    def session_duration(self) -> int:
        """
        Get session_duration attribute
        """
        return self.get_session_duration()

    def get_ip(self) -> str:
        return self._event.get("ip")

    @cached_property
    def ip(self) -> str:
        """
        Get ip attribute
        """
        return self.get_ip()

    def get_country_iso2(self) -> Optional[str]:
        return None

    @cached_property
    def country_iso2(self) -> str:
        """
        Get country_iso2 attribute
        """
        return self.get_country_iso2()

    def get_store_code(self) -> Optional[str]:
        return None

    @cached_property
    def store_code(self) -> str:
        """
        Get store_code attribute
        """
        return self.get_store_code()

    def get_dispatch_id(self) -> Optional[str]:
        return None

    @cached_property
    def dispatch_id(self) -> str:
        """
        Get dispatch_id attribute
        """
        return self.get_dispatch_id()

    def get_variant_id(self) -> Optional[str]:
        return None

    @cached_property
    def variant_id(self) -> str:
        """
        Get variant_id attribute
        """
        return self.get_variant_id()

    def get_utm_campaign(self) -> Optional[str]:
        return None

    @cached_property
    def utm_campaign(self) -> str:
        """
        Get utm_campaign attribute
        """
        return self.get_utm_campaign()

    def get_utm_medium(self) -> Optional[str]:
        return None

    @cached_property
    def utm_medium(self) -> str:
        """
        Get utm_medium attribute
        """
        return self.get_utm_medium()

    def get_utm_source(self) -> Optional[str]:
        return None

    @cached_property
    def utm_source(self) -> str:
        """
        Get utm_source attribute
        """
        return self.get_utm_source()

    def get_activity_platform(self) -> str:
        unique_id = self._event.get("unique_id", "")

        if "Web" in unique_id:
            return "Web"
        elif "Ecom App" in unique_id:
            return "Ecom app"
        elif "Training App" in unique_id:
            return "Training app"
        else:
            return None

    @cached_property
    def activity_platform(self) -> str:
        """
        Get activity_platform attribute
        """
        return self.get_activity_platform()

    def get_operating_system(self) -> str:
        if self._event.get("application_info"):
            return self._event.get("application_info", {}).get("os")
        return None

    @cached_property
    def operating_system(self) -> str:
        """
        Get operating_system attribute
        """
        return self.get_operating_system()

    def get_update_date(self) -> str:
        return datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S")

    @cached_property
    def update_date(self) -> str:
        """
        Get update_date attribute
        """
        return self.get_update_date()


class SessionEndTransformer:
    def __init__(self, event):
        self._event = event
        self._data = {}
        if event.get("events"):
            self._data = event.get("events")[0].get("data", {})

    def get_session_id(self) -> int:
        if self._data.get("session_id"):
            return int(self._data.get("session_id"))
        return None

    @cached_property
    def session_id(self) -> int:
        """
        Get session_id attribute
        """
        return self.get_session_id()

    def get_mpid(self) -> int:
        return self._event.get("mpid")

    @cached_property
    def mpid(self) -> int:
        """
        Get mpid attribute
        """
        return self.get_mpid()

    def get_session_start_time(self) -> str:
        if self._data.get("session_start_unixtime_ms"):
            return datetime.fromtimestamp(
                int(self._data.get("session_start_unixtime_ms")) / 1000, timezone.utc
            ).strftime("%Y-%m-%dT%H:%M:%S")
        return datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S")

    @cached_property
    def session_start_time(self) -> str:
        """
        Get session_start_time attribute
        """
        return self.get_session_start_time()

    def get_session_end_time(self) -> Optional[str]:
        if self._data.get("timestamp_unixtime_ms"):
            return datetime.fromtimestamp(
                int(self._data.get("timestamp_unixtime_ms")) / 1000, timezone.utc
            ).strftime("%Y-%m-%dT%H:%M:%S")
        return datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S")

    @cached_property
    def session_end_time(self) -> str:
        """
        Get session_end_time attribute
        """
        return self.get_session_end_time()

    def get_session_duration(self) -> Optional[int]:
        if self._data.get("timestamp_unixtime_ms"):
            return int(int(self._data.get("timestamp_unixtime_ms")) / 1000)
        return None

    @cached_property
    def session_duration(self) -> int:
        """
        Get session_duration attribute
        """
        return self.get_session_duration()

    def get_ip(self) -> str:
        return self._event.get("ip")

    @cached_property
    def ip(self) -> str:
        """
        Get ip attribute
        """
        return self.get_ip()

    def get_country_iso2(self) -> Optional[str]:
        return self._data.get("custom_attributes", {}).get("country_code")

    @cached_property
    def country_iso2(self) -> str:
        """
        Get country_iso2 attribute
        """
        return self.get_country_iso2()

    def get_store_code(self) -> Optional[str]:
        return self._data.get("custom_attributes", {}).get("store_code")

    @cached_property
    def store_code(self) -> str:
        """
        Get store_code attribute
        """
        return self.get_store_code()

    def get_dispatch_id(self) -> Optional[str]:
        return self._data.get("custom_attributes", {}).get("dispatch_id")

    @cached_property
    def dispatch_id(self) -> str:
        """
        Get dispatch_id attribute
        """
        return self.get_dispatch_id()

    def get_variant_id(self) -> Optional[str]:
        return self._data.get("custom_attributes", {}).get("variant")

    @cached_property
    def variant_id(self) -> str:
        """
        Get variant_id attribute
        """
        return self.get_variant_id()

    def get_utm_campaign(self) -> Optional[str]:
        return self._data.get("custom_attributes", {}).get("utm_campaign")

    @cached_property
    def utm_campaign(self) -> str:
        """
        Get utm_campaign attribute
        """
        return self.get_utm_campaign()

    def get_utm_medium(self) -> Optional[str]:
        return self._data.get("custom_attributes", {}).get("utm_medium")

    @cached_property
    def utm_medium(self) -> str:
        """
        Get utm_medium attribute
        """
        return self.get_utm_medium()

    def get_utm_source(self) -> Optional[str]:
        return self._data.get("custom_attributes", {}).get("utm_source")

    @cached_property
    def utm_source(self) -> str:
        """
        Get utm_source attribute
        """
        return self.get_utm_source()

    def get_activity_platform(self) -> str:
        unique_id = self._event.get("unique_id", "")

        if "Web" in unique_id:
            return "Web"
        elif "Ecom App" in unique_id:
            return "Ecom app"
        elif "Training App" in unique_id:
            return "Training app"
        else:
            return None

    @cached_property
    def activity_platform(self) -> str:
        """
        Get activity_platform attribute
        """
        return self.get_activity_platform()

    def get_operating_system(self) -> str:
        if self._event.get("application_info"):
            return self._event.get("application_info", {}).get("os")
        return None

    @cached_property
    def operating_system(self) -> str:
        """
        Get operating_system attribute
        """
        return self.get_operating_system()

    def get_update_date(self) -> str:
        return datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S")

    @cached_property
    def update_date(self) -> str:
        """
        Get update_date attribute
        """
        return self.get_update_date()
