from cmath import inf
from pacai.agents.learning.value import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate=0.9, iters=100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters

        # A dictionary which holds the q-values for each state.
        # Each state starts with value 0.0
        self.values = {}
        for state in self.mdp.getStates():
            self.values[state] = 0.0

        # Set the q-value for each state over iters iterations
        for _ in range(iters):
            values = dict(self.values)
            for state in self.mdp.getStates():
                bestAction = self.getPolicy(state)
                if not bestAction:  # terminal state, value stays 0.0
                    continue
                values[state] = self.getQValue(state, bestAction)
            self.values = values

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values.get(state, 0.0)

    def getPolicy(self, state):
        """
        returns the best action according to computed values
        """

        # return none if so no legal actions remain
        if self.mdp.isTerminal(state):
            return None

        bestValue = -inf
        bestAction = None

        # return action that has the highest q-value
        for action in self.mdp.getPossibleActions(state):
            value = self.getQValue(state, action)
            if bestValue < value:
                bestValue = value
                bestAction = action
        return bestAction

    def getQValue(self, state, action):
        """
        returns the q-value of the (state, action) pair.
        """

        # Q = sum(probabilty(s,a) * (reward(s, a, s') + discountRate * values[s']))
        Q = 0
        for transitionState, probabilty in self.mdp.getTransitionStatesAndProbs(state, action):
            reward = self.mdp.getReward(state, action, transitionState)
            Q += probabilty * \
                (reward + (self.discountRate * self.values[transitionState]))

        return Q

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)
