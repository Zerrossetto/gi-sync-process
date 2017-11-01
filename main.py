import yaml

from asyncio import get_event_loop, coroutine

import configuration
from gestionaleimmobiliare.sync_agenzia.agent import SyncAgenziaAgent


@coroutine
def main():

    verona_agent = SyncAgenziaAgent(configuration.get().agencies_configuration[0])

    verona_agent.synchronize_wordpress()
    print(verona_agent)


if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(main())
