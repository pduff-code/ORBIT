"""
Jake Nunemaker
National Renewable Energy Lab
01/26/2020

A reconstruction of turbine related tasks using Marmot.
"""


from marmot import process

from ORBIT.core import Cargo
from ORBIT.core._defaults import process_times as pt


class TowerSection(Cargo):
    """"""

    def __init__(self, length=None, weight=None, deck_space=None, **kwargs):
        """
        Creates an instance of `TowerSection`.
        """

        self.length = length
        self.weight = weight
        self.deck_space = deck_space

    @staticmethod
    def fasten(**kwargs):
        """Returns time required to fasten a tower section at port."""

        key = "tower_section_fasten_time"
        time = kwargs.get(key, pt[key])

        return "Fasten Tower Section", time

    @staticmethod
    def release(**kwargs):
        """Returns time required to release tower section from fastenings."""

        key = "tower_section_release_time"
        time = kwargs.get(key, pt[key])

        return "Release Tower Section", time


class Nacelle(Cargo):
    """"""

    def __init__(self, weight=None, deck_space=None, **kwargs):
        """
        Creates an instance of `Nacelle`.
        """

        self.weight = weight
        self.deck_space = deck_space

    @staticmethod
    def fasten(**kwargs):
        """Returns time required to fasten a nacelle at port."""

        key = "nacelle_fasten_time"
        time = kwargs.get(key, pt[key])

        return "Fasten Nacelle", time

    @staticmethod
    def release(**kwargs):
        """Returns time required to release nacelle from fastenings."""

        key = "nacelle_release_time"
        time = kwargs.get(key, pt[key])

        return "Release Nacelle", time


class Blade(Cargo):
    """"""

    def __init__(self, length=None, weight=None, deck_space=None, **kwargs):
        """
        Creates an instance of `Blade`.
        """

        self.length = length
        self.weight = weight
        self.deck_space = deck_space

    @staticmethod
    def fasten(**kwargs):
        """Returns time required to fasten a blade at port."""

        key = "blade_fasten_time"
        time = kwargs.get(key, pt[key])

        return "Fasten Blade", time

    @staticmethod
    def release(**kwargs):
        """Returns time required to release blade from fastenings."""

        key = "blade_release_time"
        time = kwargs.get(key, pt[key])

        return "Release Blade", time


@process
def lift_nacelle(vessel, constraints={}, **kwargs):
    """
    Calculates time required to lift nacelle to hub height.

    Parameters
    ----------
    vessel : Vessel
        Vessel to perform action.
    hub_height : int | float
        Hub height above MSL (m).

    Yields
    ------
    lift_time : float
        Time required to lift nacelle to hub height (h).
    """

    hub_height = kwargs.get("hub_height", None)
    crane_rate = vessel.crane.crane_rate(**kwargs)
    lift_time = hub_height / crane_rate

    yield vessel.task("Lift Nacelle", lift_time, constraints=constraints)


@process
def attach_nacelle(vessel, constraints={}, **kwargs):
    """
    Returns time required to attach nacelle to tower.

    Parameters
    ----------
    vessel : Vessel
        Vessel to perform action.
    nacelle_attach_time : int | float
        Time required to attach nacelle.

    Returns
    -------
    nacelle_attach_time : float
        Time required to attach nacelle (h).
    """

    _ = vessel.crane
    key = "nacelle_attach_time"
    attach_time = kwargs.get(key, pt[key])

    yield vessel.task("Attach Nacelle", attach_time, constraints=constraints)


@process
def lift_turbine_blade(vessel, constraints={}, **kwargs):
    """
    Calculates time required to lift turbine blade to hub height.

    Parameters
    ----------
    vessel : Vessel
        Vessel to perform action.
    hub_height : int | float
        Hub height above MSL (m).

    Returns
    -------
    blade_lift_time : float
        Time required to lift blade to hub height (h).
    """

    hub_height = kwargs.get("hub_height", None)
    crane_rate = vessel.crane.crane_rate(**kwargs)
    lift_time = hub_height / crane_rate

    yield vessel.task("Lift Blade", lift_time, constraints=constraints)


@process
def attach_turbine_blade(vessel, constraints={}, **kwargs):
    """
    Returns time required to attach turbine blade to hub.

    Parameters
    ----------
    vessel : Vessel
        Vessel to perform action.
    blade_attach_time : int | float
        Time required to attach turbine blade.

    Returns
    -------
    blade_attach_time : float
        Time required to attach turbine blade (h).
    """

    _ = vessel.crane
    key = "blade_attach_time"
    attach_time = kwargs.get(key, pt[key])

    yield vessel.task("Attach Blade", attach_time, constraints=constraints)


@process
def lift_tower_section(vessel, height, constraints={}, **kwargs):
    """
    Calculates time required to lift tower section at site.

    Parameters
    ----------
    vessel : Vessel
        Vessel to perform action.
    height : int | float
        Height above MSL (m) required for lift.

    Returns
    -------
    section_lift_time : float
        Time required to lift tower section (h).
    """

    crane_rate = vessel.crane.crane_rate(**kwargs)
    lift_time = height / crane_rate

    yield vessel.task("Lift Tower Section", lift_time, constraints=constraints)


@process
def attach_tower_section(vessel, constraints={}, **kwargs):
    """
    Returns time required to attach tower section at site.

    Parameters
    ----------
    vessel : Vessel
        Vessel to perform action.
    section_attach_time : int | float
        Time required to attach tower section (h).

    Returns
    -------
    section_attach_time : float
        Time required to attach tower section (h).
    """

    _ = vessel.crane
    key = "tower_section_attach_time"
    attach_time = kwargs.get(key, pt[key])

    yield vessel.task(
        "Attach Tower Section", attach_time, constraints=constraints
    )


@process
def install_tower_section(vessel, section, height, **kwargs):
    """
    Process logic for installing a tower at site.

    Subprocesses:

    - Lift tower,  ``tasks.lift_tower()``
    - Attach tower, ``tasks.attach_tower()``

    Parameters
    ----------
    vessel : Vessel
    tower : dict
    """
    yield lift_tower_section(
        vessel, height, constraints=vessel.operational_limits, **kwargs
    )

    yield attach_tower_section(
        vessel, constraints=vessel.operational_limits, **kwargs
    )


@process
def install_nacelle(vessel, nacelle, **kwargs):
    """
    Process logic for installing a nacelle on a pre-installed tower.

    Subprocesses:

    - Lift nacelle, ``tasks.lift_nacelle()``
    - Attach nacelle, ``tasks.attach_nacelle()``

    Parameters
    ----------
    vessel : Vessel
    tower : dictå
    """

    yield lift_nacelle(vessel, constraints=vessel.operational_limits, **kwargs)

    yield attach_nacelle(
        vessel, constraints=vessel.operational_limits, **kwargs
    )


@process
def install_turbine_blade(vessel, blade, **kwargs):
    """
    Process logic for installing a turbine blade on a pre-installed tower and
    nacelle assembly.

    Subprocesses:

    - Lift blade, ``tasks.lift_turbine_blade()``
    - Attach blade, ``tasks.attach_turbine_blade()``

    Parameters
    ----------
    vessel : Vessel
    tower : dict
    """

    yield lift_turbine_blade(
        vessel, constraints=vessel.operational_limits, **kwargs
    )

    yield attach_turbine_blade(
        vessel, constraints=vessel.operational_limits, **kwargs
    )
