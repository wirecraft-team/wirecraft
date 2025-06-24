from ipaddress import IPv4Address

from .base import Level, Task
from .tests import CableConnectionTest, DevicePresenceTest, PingTest

levels = [
    Level(
        id=0,
        tasks=[
            Task(
                name="(1/3) Ajoutez des appareils",
                description="Ajoutez un PC nommé pc1.",
                tests=[DevicePresenceTest(name="pc1", type="pc")],
            ),
            Task(
                name="(2/3) Ajoutez des appareils",
                description="Ajoutez un PC nommé pc2.",
                tests=[DevicePresenceTest(name="pc2", type="pc")],
            ),
            Task(
                name="(3/3) Ajoutez des appareils",
                description="Ajoutez un switch nommé switch.",
                tests=[DevicePresenceTest(name="switch", type="switch")],
            ),
            Task(
                name="(1/2) Liez les appareils",
                description="Ajoutez un câble entre pc1 et switch.",
                tests=[CableConnectionTest(source="pc1", destination="switch")],
            ),
            Task(
                name="(2/2) Liez les appareils",
                description="Ajoutez un câble entre pc2 et switch.",
                tests=[CableConnectionTest(source="pc2", destination="switch")],
            ),
        ],
    ),
    Level(
        id=1,
        tasks=[
            Task(
                name="(1/2) Ping !",
                description=(
                    "Il faut que pc1 puisse ping pc2 sur l'IP 192.168.0.3\nDonnez l'adresse IP 192.168.0.3 à pc2"
                ),
                tests=[PingTest(source="pc1", destination=IPv4Address("192.168.0.3"))],
            ),
            Task(
                name="(2/2) Pong !",
                description="Il faut que pc2 puisse ping pc1 sur l'IP 192.168.0.2\nDonnez la bonne adresse IP à pc1 !",
                tests=[PingTest(source="pc2", destination=IPv4Address("192.168.0.2"))],
            ),
        ],
    ),
    Level(
        id=1,
        tasks=[
            Task(
                name="Fin de la démo",
                description="Achetez la version complète du jeu pour avoir plus de niveaux !",
                tests=[DevicePresenceTest(name="", type="")],
            ),
        ],
    ),
]
