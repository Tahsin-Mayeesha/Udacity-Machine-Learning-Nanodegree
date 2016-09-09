import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        
        # TODO: Initialize any additional variables here
        self.correct_actions  = ["forward","left","right",None]
        
        # add the previous state, action and reward variables for updating Q-values
        
        self.previous_state = None
        self.previous_action = None
        self.previous_reward = None
        
        # Add parameters for the Q-table
        
        self.gamma = 0.3
        self.alpha = 0.6
        self.epsilon = 0.1
        self.Q = {} 
        self.default_Q_val = 14
        

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        
        self.previous_state = None
        self.previous_action = None
        self.previous_reward = None

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        
        
        
        self.state = (("light",inputs["light"]),("oncoming",inputs["oncoming"]),("waypoint",self.next_waypoint))
        
        
        
        #1st Q. Implement a basic agent that chooses action randomly
        # action = random.choice(self.correct_actions)
        # what if the next_waypoint was chosen as the action?
        #action = self.next_waypoint 
        
        
        # TO DO: Choose action on basis of Q-learning
        
        if self.state in self.Q: # if we have been into this state before 
            if random.random() > self.epsilon: # epsilon should be a small number so that we use the learned values of Q-table most of the time
                # choose the action that has the max Q-value, can be greater than one if most of the actions has just been initialized
                potential_actions = {a:v for a,v in self.Q[self.state].items() if v==max(self.Q[self.state].values())}
                action = random.choice(potential_actions.keys())
            else:
                action = random.choice(self.correct_actions)
            
            
        else:
            # if we have not been into this state before then initialize the Q-values for each valid action
            self.Q[self.state] = {action:self.default_Q_val for action in self.correct_actions}
            # then choose a random action from the set of valid action
            action = random.choice(self.correct_actions)

        
        
        
        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward/ Updating Q-table values
        
        if self.previous_state != None:
            # Complete the equation after rewatching the videos 
            self.Q[self.previous_state][self.previous_action] = (1-self.alpha)*self.Q[self.previous_state][self.previous_action] + \
                                                            self.alpha*(self.previous_reward + self.gamma*max(self.Q[self.state].values()))
        
        
        
        
        self.previous_state = self.state
        self.previous_action = action
        self.previous_reward = reward
        
        
        

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  #[debug]
        print "State = {}".format(self.state) 

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.1, display=False,live_plot = True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line
    

if __name__ == '__main__':
    run()
