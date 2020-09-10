agent_parameters = {
    "metabolism" : 2,               # The 'cost' of staying alive per epoch (in energy)
    "procreateReq" : 16,            # The amount of energy an agent needs to have before it can create offspring
    "procreateCost" : 10,           # The amount of energy it costs to create a new child
    "maxmimum_age" : 100,           # The maximum age for the agent, the agent gets 'removed' when its age exceeds this parameter
}

resource_parameters = {
    "start_amount" : 100,           # The starting amount of units of the common resource
    "max_amount": 100,              # The maximum amount units there can be at one epoch
    "growth_rate" : 0.5,            # The growth rate (in units) of the common resource
    "energy_per_unit" : 5,          # The amount of energy one unit provides
}

environment_parameters = {
    "initial_agents_count" : 100,  

}