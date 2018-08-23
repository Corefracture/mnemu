import ip_filter


class IpFilterManager:
    """
    Manages, updates, and periodically checks the current netem settings
    for the IP's that have been filtered.
    """
    def __init__(self):
        self._master_control = []
        return
