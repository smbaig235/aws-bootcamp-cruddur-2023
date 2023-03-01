from datetime import datetime, timedelta, timezone
from aws_xray_sdk.core import xray_recorder


class UserActivities:
  def run(user_handle):

    # X-Ray---
    segment = xray_recorder.begin_segment('user_activities_start')

    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['blank_user_handle']
    else:
      now = datetime.now()
      results = [{
        'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
        'handle':  'Andrew Brown',
        'message': 'Cloud is fun!',
        'created_at': (now - timedelta(days=1)).isoformat(),
        'expires_at': (now + timedelta(days=31)).isoformat()
      }]
      model['data'] = results

    # X-Ray---
    subsegment = xray_recorder.begin_subsegment('user_activities_sub')

    dict = {

     "now": now.isoformat(),
     "result-size": len(model['data'])
    }
    # segment.put_metadata('key', dict, 'namespace')
    subsegment.put_metadata('key', dict, 'namespace')

    return model