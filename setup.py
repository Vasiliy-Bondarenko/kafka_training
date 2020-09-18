from setuptools import setup

setup(
    # ...
    entry_points={
        'console_scripts': [
            'example = example.app:main',
        ],
        'faust.codecs': [
            'avro_users = codec:avro_user_codec',
            'avro_trades = codec:avro_trade_codec',
        ],
    },
)
