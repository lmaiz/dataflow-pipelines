import apache_beam as beam

from .transformers import SessionStartTransformer, SessionEndTransformer
import logging


class SessionStartTemplate(beam.DoFn):
    def __init__(self, service_account_email):
        self.service_account_email = service_account_email

    def process(self, event):
        try:
            transformer = SessionStartTransformer(event)

            return {
                "session_id": transformer.session_id,
                "mpid": transformer.mpid,
                "session_start_time": transformer.session_start_time,
                "session_end_time": transformer.session_end_time,
                "session_duration": transformer.session_duration,
                "ip": transformer.ip,
                "country_iso2": transformer.country_iso2,
                "store_code": transformer.store_code,
                "dispatch_id": transformer.dispatch_id,
                "variant_id": transformer.variant_id,
                "utm_campaign": transformer.utm_campaign,
                "utm_medium": transformer.utm_medium,
                "utm_source": transformer.utm_source,
                "activity_platform": transformer.activity_platform,
                "operating_system": transformer.operating_system,
                "update_date": transformer.update_date,
                "update_user": self.service_account_email,
                "_CHANGE_TYPE": "UPSERT",
            }
        except Exception as e:
            logging.error(
                "The following error occuried while creating SessionStartTemplate : ",
                str(e),
            )


class SessionEndTemplate(beam.DoFn):
    def __init__(self, service_account_email):
        self.service_account_email = service_account_email

    def process(self, event):
        try:
            transformer = SessionEndTransformer(event)

            return {
                "session_id": transformer.session_id,
                "mpid": transformer.mpid,
                "session_start_time": transformer.session_start_time,
                "session_end_time": transformer.session_end_time,
                "session_duration": transformer.session_duration,
                "ip": transformer.ip,
                "country_iso2": transformer.country_iso2,
                "store_code": transformer.store_code,
                "dispatch_id": transformer.dispatch_id,
                "variant_id": transformer.variant_id,
                "utm_campaign": transformer.utm_campaign,
                "utm_medium": transformer.utm_medium,
                "utm_source": transformer.utm_source,
                "activity_platform": transformer.activity_platform,
                "operating_system": transformer.operating_system,
                "update_date": transformer.update_date,
                "update_user": self.service_account_email,
                "_CHANGE_TYPE": "UPSERT",
            }
        except Exception as e:
            logging.error(
                "The following error occuried while creating SessionEndTemplate : ",
                str(e),
            )
