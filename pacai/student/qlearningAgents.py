from cmath import inf
from random import choice
from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.util import reflection, probability


class QLearningAgent(ReinforcementAgent):
    """
    A Q-Learning agent.

    Some functions that may be useful:

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getAlpha`:
    Get the learning rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getDiscountRate`:
    Get the discount rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`:
    Get the exploration probability.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getLegalActions`:
    Get the legal actions for a reinforcement agent.

    `pacai.util.probability.flipCoin`:
    Flip a coin (get a binary value) with some probability.

    `random.choice`:
    Pick randomly from a list.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Compute the action to take in the current state.
    With probability `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`,
    we should take a random action and take the best policy action otherwise.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should choose None as the action.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    The parent class calls this to observe a state transition and reward.
    You should do your Q-Value update here.
    Note that you should never call this function, it will be called on your behalf.

    DESCRIPTION: <Write something here so we know what you did.>
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

        # A dictionary which holds the q-values for each state.
        self.values = {}

    def getQValue(self, state, action):
        """
        Get the Q-Value for a `pacai.core.gamestate.AbstractGameState`
        and `pacai.core.directions.Directions`.
        Should return 0.0 if the (state, action) pair has never been seen.
        """

        if action is None:
            return 0.0

        if not (state, action) in self.values:
            self.values[state, action] = 0.0

        return self.values[state, action]

    def getValue(self, state):
        """
        Return the value of the best action in a state.
        I.E., the value of the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of 0.0.

        This method pairs with `QLearningAgent.getPolicy`,
        which returns the actual best action.
        Whereas this method returns the value of the best action.
        """

        return self.getQValue(state, self.getPolicy(state))

    def getPolicy(self, state):
        """
        Return the best action in a state.
        I.E., the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of None.

        This method pairs with `QLearningAgent.getValue`,
        which returns the value of the best action.
        Whereas this method returns the best action itself.
        """

        bestValue = -inf
        bestAction = None

        # return action that has the highest q-value
        for action in ReinforcementAgent.getLegalActions(self, state):
            value = self.getQValue(state, action)
            if bestValue < value:
                bestValue = value
                bestAction = action
        return bestAction

    def getAction(self, state):
        """
        Returns the epsilon-greedy action selection
        """

        if probability.flipCoin(ReinforcementAgent.getEpsilon(self)):
            return choice(ReinforcementAgent.getLegalActions(self, state))
        return self.getPolicy(state)

    def update(self, state, action, nextState, reward):
        """
        This class will call this function after observing a transition and reward.
        """

        # sample = reward + discount * value(s', a')
        # Q(s,a) = (1-a) * Q(s,a) + a * sample

        alpha = ReinforcementAgent.getAlpha(self)
        discountRate = ReinforcementAgent.getDiscountRate(self)

        sample = reward + (discountRate * self.getValue(nextState))
        self.values[state, action] = (1 - alpha) * \
            self.getQValue(state, action) + (alpha * sample)

        return None


class PacmanQAgent(QLearningAgent):
    """
    Exactly the same as `QLearningAgent`, but with different default parameters.
    """

    def __init__(self, index, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, **kwargs):
        kwargs['epsilon'] = epsilon
        kwargs['gamma'] = gamma
        kwargs['alpha'] = alpha
        kwargs['numTraining'] = numTraining

        super().__init__(index, **kwargs)

    def getAction(self, state):
        """
        Simply calls the super getAction method and then informs the parent of an action for Pacman.
        Do not change or remove this method.
        """

        action = super().getAction(state)
        self.doAction(state, action)

        return action


class ApproximateQAgent(PacmanQAgent):
    """
    An approximate Q-learning agent.

    You should only have to overwrite `QLearningAgent.getQValue`
    and `pacai.agents.learning.reinforcement.ReinforcementAgent.update`.
    All other `QLearningAgent` functions should work as is.

    Additional methods to implement:

    `QLearningAgent.getQValue`:
    Should return `Q(state, action) = w * featureVector`,
    where `*` is the dotProduct operator.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    Should update your weights based on transition.

    DESCRIPTION: <Write something here so we know what you did.>
    """

    def __init__(self, index,
                 extractor='pacai.core.featureExtractors.IdentityExtractor', **kwargs):
        super().__init__(index, **kwargs)
        self.featExtractor = reflection.qualifiedImport(extractor)

        # A dictionary which holds the weights.
        self.weights = {}

    def getQValue(self, state, action):
        """
        Get the Q-Value for a `pacai.core.gamestate.AbstractGameState`
        and `pacai.core.directions.Directions`.
        Should return 0.0 if the (state, action) pair has never been seen.
        """

        if action is None:
            return 0.0

        features = self.featExtractor.getFeatures(self, state, action)

        # Return q-value for each feature key, set weight to 0 on first pass
        Q = 0
        for feature in features:
            if feature not in self.weights:
                self.weights[feature] = 0.0
            Q += features[feature] * self.weights[feature]
        return Q

    def update(self, state, action, nextState, reward):
        """
        This class will call this function after observing a transition and reward.
        """

        # correction = (reward + discountRate * value(s', a')) - Q
        # weight = weight + (alpha * correction * feature)

        alpha = ReinforcementAgent.getAlpha(self)
        discountRate = ReinforcementAgent.getDiscountRate(self)

        correction = (reward + (discountRate * self.getValue(nextState))
                      ) - self.getQValue(state, action)

        features = self.featExtractor.getFeatures(self, state, action)

        # Set weight for each feature key
        for feature in features:
            self.weights[feature] = self.weights[feature] + \
                (alpha * correction * features[feature])

        return None

    def final(self, state):
        """
        Called at the end of each game.
        """

        # Call the super-class final method.
        super().final(state)

        return None
