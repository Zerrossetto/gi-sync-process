
from asyncio import get_event_loop, coroutine
from gestionaleimmobiliare.sync_agenzia.agent import SyncAgenziaAgent


@coroutine
def main():

    agent = SyncAgenziaAgent()
    agent.synchronize_wordpress()
    print(agent)


if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(main())
