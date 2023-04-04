import redis


r = redis.Redis(host='redis', port=6379, db=1)


def get_status(user_id: int) -> bool:
    return bool(int(r.get(user_id)))

def set_status(user_id: int, status: bool):
    r.set(user_id, int(status))


