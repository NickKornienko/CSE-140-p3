"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None


def question2():
    """
    To get the agent to cross the bridge noise was lowered to 0. 
    The agent will avoid crossing the bridge with higher noise as it has
    a large probabilty of failure due to going north/south. Lower values such as
    0.01 also will often work as the probabilty of unitended behaviour is low.
    """

    answerDiscount = 0.9
    answerNoise = 0.0

    return answerDiscount, answerNoise


def question3a():
    """
    To get the agent to perfer the close exit living reward should be at a
    minimum to get the agent to not seek further exits. 
    
    Discount should also be at a minimum to lower values enough
    that the agent doesn't seek further rewards.

    Noise should be at a minimum for the agent to risk the cliff as
    there will be minimal risk of going south due to unintended behaviour
    """

    answerDiscount = 0.1
    answerNoise = 0.0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward


def question3b():
    """
    Answer discount and living reward need to be raised slightly to allow
    the agent to take the longer path and avoid the cliff, 
    but not so much that it goes for the futher exit.

    Noise should be increased to make the longer path outweigh risking the cliff
    """

    answerDiscount = 0.3
    answerNoise = 0.2
    answerLivingReward = 0.2

    return answerDiscount, answerNoise, answerLivingReward


def question3c():
    """
    Discount and living reward should be raised enough for the agent to perfer
    the distant exit

    Noise should be low to minimize the risk of the cliff
    """

    answerDiscount = 0.3
    answerNoise = 0.0
    answerLivingReward = 0.2

    return answerDiscount, answerNoise, answerLivingReward


def question3d():
    """
    Discount should be raised to ensure the distant exit is perferred.

    Noise should be raised so the agent take the longer, safer route
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.1

    return answerDiscount, answerNoise, answerLivingReward


def question3e():
    """
    Discount should be zero so the agent doesn't attempt to go for the exits

    Noise should also be limited to avoid the change of the agent accidently
    reaching an exit.

    Living reward should be non-zero so the agent is motivated to
    """

    answerDiscount = 0.0
    answerNoise = 0.0
    answerLivingReward = 1.0

    return answerDiscount, answerNoise, answerLivingReward


def question6():
    """
    [Enter a description of what you did here.]
    """

    answerEpsilon = 0.3
    answerLearningRate = 0.5

    return answerEpsilon, answerLearningRate


if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
