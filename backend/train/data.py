from dataclasses import dataclass


# Always change together with Android `Train.ServerData`.
@dataclass
class ServerData:
    status: str
    session_id: int | None
    port: int | None
