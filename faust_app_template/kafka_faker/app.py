import faust
from mode import get_logger
from simple_settings import settings

app = faust.App(
    # https://faust.readthedocs.io/en/latest/userguide/settings.html
    id="kafka_faker",
    debug=settings.DEBUG,
    autodiscover=["agents"], # https://faust.readthedocs.io/en/latest/userguide/settings.html#autodiscover
    broker=settings.KAFKA_BOOTSTRAP_SERVER,
    store=settings.STORE_URI,
    topic_allow_declare=settings.TOPIC_ALLOW_DECLARE,
    topic_disable_leader=settings.TOPIC_DISABLE_LEADER,
    broker_credentials=settings.BROKER_CREDENTIALS,
    topic_replication_factor=3,
    broker_max_poll_records=100,
    broker_max_poll_interval=300,
    agent_supervisor="mode.CrashingSupervisor", # https://faust.readthedocs.io/en/latest/userguide/settings.html#agent-supervisor

)







