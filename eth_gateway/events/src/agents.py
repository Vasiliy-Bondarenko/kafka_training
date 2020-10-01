import logging
from app import app

logger = logging.getLogger(__name__)

# this counter exists in-memory only,
# so will be wiped when the worker restarts.
count = [0]


@app.page('/count/')
async def get_count(self, request):
    # update the counter
    count[0] += 1
    # and return it.
    return self.json({
        'count': count[0],
    })
