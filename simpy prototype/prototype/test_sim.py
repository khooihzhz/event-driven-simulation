import simpy  # For Simulation
import random  # This is for generating random number


RANDOM_SEED = 42


# Simulate customer arrival
def customer(env, cashier):
    with cashier.request() as req:
        yield req
        start = env.now
        serving_duration = 5
        print("Serving Customer.... at %d" % start)
        yield env.process(serving_customer(env, serving_duration))


# serve customer function
def serving_customer(env, serving_duration):
    yield env.timeout(serving_duration)
    print("Done Serving customer at %d" % env.now)


# generate new customer
def customer_generator(env, cashier):
    for i in range(5):
        yield env.timeout(random.randint(1, 3))
        print("Customer arrived at %d"  % env.now)
        env.process(customer(env, cashier))


# Start simulation
env = simpy.Environment()
random.seed(RANDOM_SEED)

# Resources for the simulation
cashier = simpy.Resource(env, capacity=1)
env.process(customer_generator(env, cashier))
env.run(until=30)