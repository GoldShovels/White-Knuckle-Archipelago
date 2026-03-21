from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import APQuestWorld

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: APQuestWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


# I've defined "regions" as the "biomes" that can appear. They are organized via the larger areas they belong to
# and in the order they appear. Some are mutually exclusive.
# Event regions are not included. I'm not sure if I'll add them.
def create_all_regions(world: APQuestWorld) -> None:

    # Silos regions
    deep_storage = Region("Silos: Deep Storage", world.player, world.multiworld)
    air_exchange = Region("Silos: Air Exchange", world.player, world.multiworld)
    shattered_chambers = Region("Silos: Shattered Chambers", world.player, world.multiworld)

    # Pipeworks regions
    drainage_system = Region("Pipeworks: Drainage System", world.player, world.multiworld)
    pipe_organ = Region("Pipeworks: Pipe Organ", world.player, world.multiworld)
    waste_heap = Region("Pipeworks: Waste Heap", world.player, world.multiworld)

    # Habitation regions
    forlorn_gateway = Region("Habitation: Forlorn Gateway", world.player, world.multiworld)
    service_shaft = Region("Habitation: Service Shaft", world.player, world.multiworld)
    haunted_pier = Region("Habitation: Haunted Pier", world.player, world.multiworld)
    delta_labs = Region("Habitation: Delta Labs", world.player, world.multiworld)

    # The Abyss regions
    transit_scafold = Region("The Abyss: Transit Scaffold", world.player, world.multiworld)
    deadmans_handle = Region("The Abyss: Deadman's Handle", world.player, world.multiworld)
    hanging_gardens = Region("The Abyss: Hanging Gardens", world.player, world.multiworld)

    # Interludes
    interlude_lockdown = Region("Interlude: Lockdown", world.player, world.multiworld)
    interlude_ascent = Region("Interlude: Ascent", world.player, world.multiworld)
    interlude_evacuation = Region("Interlude: Evacuation", world.player, world.multiworld)

    # Other
    silos_break_room = Region("Silos: Break Room", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [deep_storage, silos_break_room, air_exchange, shattered_chambers, drainage_system, pipe_organ, waste_heap,
               forlorn_gateway, service_shaft, haunted_pier, delta_labs, transit_scafold, deadmans_handle,
               hanging_gardens, interlude_lockdown, interlude_ascent, interlude_evacuation]

    # Some regions may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # TODO: Potentially add regions for events / challenge levels?
    if world.options.hammer:
        top_middle_room = Region("Top Middle Room", world.player, world.multiworld)
        regions.append(top_middle_room)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: APQuestWorld) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    deep_storage = world.get_region("Silos: Deep Storage")
    air_exchange = world.get_region("Silos: Air Exchange")
    shattered_chambers = world.get_region("Silos: Shattered Chambers")
    drainage_system = world.get_region("Pipeworks: Drainage System")
    pipe_organ = world.get_region("Pipeworks: Pipe Organ")
    waste_heap = world.get_region("Pipeworks: Waste Heap")
    forlorn_gateway = world.get_region("Habitation: Forlorn Gateway")
    service_shaft = world.get_region("Habitation: Service Shaft")
    haunted_pier = world.get_region("Habitation: Haunted Pier")
    delta_labs = world.get_region("Habitation: Delta Labs")
    transit_scafold = world.get_region("The Abyss: Transit Scaffold")
    deadmans_handle = world.get_region("The Abyss: Deadman's Handle")
    hanging_gardens = world.get_region("The Abyss: Hanging Gardens")
    interlude_lockdown = world.get_region("Interlude: Lockdown")
    interlude_ascent = world.get_region("Interlude: Ascent")
    interlude_evacuation = world.get_region("Interlude: Evacuation")
    silos_break_room = world.get_region("Silos: Break Room")

    # Okay, now we can get connecting. For this, we need to create Entrances.
    # Entrances are inherently one-way, but crucially, AP assumes you can always return to the origin region.
    # One way to create an Entrance is by calling the Entrance constructor.
    #overworld_to_bottom_right_room = Entrance(world.player, "Overworld to Bottom Right Room", parent=overworld)
    #overworld.exits.append(overworld_to_bottom_right_room)

    # You can then connect the Entrance to the target region.
    #overworld_to_bottom_right_room.connect(bottom_right_room)

    # An even easier way is to use the region.connect helper.
    #overworld.connect(right_room, "Overworld to Right Room")

    deep_storage.connect(silos_break_room, "Deep Storage to Air Exchange")
    silos_break_room.connect(air_exchange, "Silos Break Room to Deep Storage")
    silos_break_room.connect(shattered_chambers, "Silos Break Room to Shattered Chambers")

    deep_storage.connect(interlude_lockdown, "Deep Storage to Interlude Lockdown")
    air_exchange.connect(interlude_lockdown, "Air Exchange to Interlude Lockdown")

    interlude_lockdown.connect(drainage_system, "Interlude Lockdown to Drainage System")
    drainage_system.connect(waste_heap, "Drainage System to Waste Heap")
    drainage_system.connect(pipe_organ, "Drainage System to Pipe Organ")
    waste_heap.connect(interlude_ascent, "Waste Heap to Pipe Organ")

    interlude_ascent.connect(forlorn_gateway, "Pipe Organ to Forlorn Gateway")
    forlorn_gateway.connect(service_shaft, "Forlorn Gateway to Service Shaft")
    service_shaft.connect(haunted_pier, "Forlorn Gateway to Haunted Pier")
    haunted_pier.connect(delta_labs, "Haunted Pier to Delta Labs")

    delta_labs.connect(interlude_evacuation, "Delta Labs to Interlude Ascent")

    interlude_evacuation.connect(transit_scafold, "Interlude Ascent to Transit Scaffold")
    transit_scafold.connect(deadmans_handle, "Transit Scaffold to Deadman's Handle")
    deadmans_handle.connect(hanging_gardens, "Deadman's Handle to Hanging Gardens")




    # The region.connect helper even allows adding a rule immediately.
    # We'll talk more about rule creation in the set_all_rules() function in rules.py.
    #overworld.connect(top_left_room, "Overworld to Top Left Room", lambda state: state.has("Key", world.player))

    # Some Entrances may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # In this case, we previously created an extra "Top Middle Room" region that we now need to connect to Overworld.
    '''
    if world.options.hammer:
        top_middle_room = world.get_region("Top Middle Room")
        overworld.connect(top_middle_room, "Overworld to Top Middle Room")
    '''
