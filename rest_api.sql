--!jinja2

{% set branch = DEPLOYMENT_TYPE %}

{% if DEPLOYMENT_TYPE == 'main' %}
	{% set database = 'DWH' %}
    {% set eai_suffix = '' %}
{% elif DEPLOYMENT_TYPE == 'dev' %}
	{% set database = 'DWH_DEV' %}
    {% set eai_suffix = '_DEV' %}
{% endif %}
	
create or replace function {{ database }}.STP.call_aqs(job_name string)
returns string
language python
runtime_version = 3.10
handler = 'rest_api.main'
external_access_integrations = (AQS{{ eai_suffix }}_ACCESS_INTEGRATION)
packages = ('requests','pyyaml')
imports= (
    '@{{ database }}.STP.GIT_REPOSITORY/branches/{{ branch }}/rest_api.py'
    )
secrets = (
    'aqs_url' = {{ database }}.STP.AQS_URL,
    'aqs_sas_token' = {{ database }}.STP.SAS_TOKEN
    )
;
