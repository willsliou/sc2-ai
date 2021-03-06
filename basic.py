from sc2.bot_ai import BotAI # parent class to inherit
from sc2.data import Race, Difficulty
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2 import maps
from sc2.ids.unit_typeid import UnitTypeId
import random as random

class WorkerRushBot(BotAI):
    async def on_step(self, iteration: int):
        print(f"{iteration}, n_workers: {self.workers.amount}, n_idle_workers: {self.workers.idle.amount},", \
        f"minerals: {self.minerals}, gas: {self.vespene}, cannons: {self.structures(UnitTypeId.PHOTONCANNON).amount},", \
        f"pylons: {self.structures(UnitTypeId.PYLON).amount}, nexus: {self.structures(UnitTypeId.NEXUS).amount}", \
        f"gateways: {self.structures(UnitTypeId.GATEWAY).amount}, cybernetics cores: {self.structures(UnitTypeId.CYBERNETICSCORE).amount}", \
        f"stargates: {self.structures(UnitTypeId.STARGATE).amount}, voidrays: {self.units(UnitTypeId.VOIDRAY).amount}, supply: {self.supply_used}/{self.supply_cap}")
    
        await self.distribute_workers()

        # If we have a Nexus
        if self.townhalls:
            nexus = self.townhalls.random

            # Train Probes
            if nexus.is_idle and self.can_afford(UnitTypeId.PROBE):
                nexus.train(UnitTypeId.PROBE)

            # Build Pylons
            # If we don't have a Pylon and a pylon is not being built
            elif not self.structures(UnitTypeId.PYLON) and self.already_pending(UnitTypeId.PYLON) == 0:
                # If we can afford a pylon, build a pylon near nexus
                if self.can_afford(UnitTypeId.PYLON):
                    await self.build(UnitTypeId.PYLON, near=nexus)
            
            # If we have less than 5 pylons, build more
            elif self.structures(UnitTypeId.PYLON).amount < 5:
                if self.can_afford(UnitTypeId.PYLON):
                    # Build Pylon near enemy start location
                    target_pylon = self.structures(UnitTypeId.PYLON).closest_to(self.enemy_start_locations[0])
                    pos = target_pylon.position.towards(self.enemy_start_locations[0], random.randrange(8,15))
                    await self.build(UnitTypeId.PYLON, near=pos)


            # Build cannon
            elif not self.structures(UnitTypeId.FORGE):
                # If we can afford a forge, build one near the Nexus
                if self.can_afford(UnitTypeId.FORGE):
                    await self.build(UnitTypeId.FORGE, near = self.structures(UnitTypeId.PYLON).closest_to(nexus))

            elif self.structures(UnitTypeId.FORGE).ready and self.structures(UnitTypeId.PHOTONCANNON.amount) < 3:
                if self.can_afford(UnitTypeId.PHOTONCANNON):
                    await self.build(UnitTypeId.PHOTONCANNON, near = nexus)

        # If we don't have a Nexus
        else:
            if self.can_afford(UnitTypeId.NEXUS):
                await self.expand_now


run_game(maps.get("AcropolisLE"), 
    [
    Bot(Race.Protoss, WorkerRushBot()),
    Computer(Race.Zerg, Difficulty.Medium)], 
    realtime=False)