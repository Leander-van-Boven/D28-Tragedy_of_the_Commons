# Proposal Agent resource function
Take, for some simulation $S$, the set of all epochs $T_S$ and the set of all agents $A_S$. We want to define a function $f$, such that:
$$f : T_S \times A_S \mapsto [0,1]$$
In other words, $f$ denotes the fraction of the available energy an agent $a_S\in A_S$ will take, based on the epoch $t_S\in T_S$. The maximum amount of energy an agent will take is a pre-defined parameter $\epsilon_{max}\in\mathbb{N}$. However, we need to make sure this amount of energy is available in the current epoch. We denote this value as $\epsilon_{t_S}\in\mathbb{N}$. The true amount of energy an agent will take at a certain epoch can then be described by the function $E : T_S \times A_S \mapsto \mathbb{N}$ such that:
$$E(t_s, a_s) = \min(f(t_s, a_s) \cdot \epsilon_{max}, \epsilon_{t_S})$$
We only need to define $f$. The output of this function is influenced by different behaviours that an agent can emit. The agent acts on the current state of the simulation, and a behaviour defines how to act. However, multiple behaviours exist and these can have conflicting outcomes. In our simulation, the influence a behaviour can have on the outcome of $f$ depends on the agent's social value orientation, or $svo_a\in [0,1]$. The total collection of $n$ behaviours can be defined as a tuple 
$$\beta ={\langle B, \Mu\rangle, } $$
Where $B$ is an orderedset of $n$ behaviour functions $b_i\in B : T_S \times A_S \mapsto [0,1]$, that 'vote' for the fraction of energy they 'advice' the agent to take. $\Mu$ is an ordered set of values ${\mu_i\in \Mu}$ that defines the 'optimal' social value orientation value for function $b_i$. First, we need to get for each behaviour, its distance from its optimal svo. Thus we define 
$$D = \{d(\mu, svo_a) | \mu \in \Mu\}$$
For some pre-determined distance function, such as: absolute, quadratic, etc. 
We can now define $f$ as
$$f(t_S, a_S) = \text{combine}(B(t_S, a_S), D))$$
Where $B(t_S, a_S) = \{b(t_S, a_S)|b\in B\}$, and $\text{combine} : [0,1]\times M \mapsto [0,1]$ is a function that combines all the behaviours based on the values in $\Mu$. This can be done in multiple ways, for instance by taking the weighted average of $B$ with $1-D$ as weights, or by taking the behaviour with the smallest distance. 

The behaviours we've currently implemented can each be converted into a $b\in B$ with a corresponding $\mu\in\Mu$. Aport from this making the impacts continuous instead of discrete, I also think this will scale very well if we want to add behaviours later on. Additionally, this will make the behaviours not mutually exclusive, which I think is more realistic and will result in more complex and interesting results. 