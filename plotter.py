import matplotlib.pyplot as plt

def plot1(time, thrust, acceleration, velocity, position):
    plt.subplot(2, 2, 1)
    plt.title("Thrust")
    plt.plot(time, thrust)
    plt.legend(['Thrust(N)'])
    plt.grid()

    plt.subplot(2, 2, 2)
    plt.title("Acceleration - Velocity")
    plt.plot(time, acceleration)
    plt.plot(time, velocity)
    plt.legend(['Vertical Acceleration(m/s^2)', 'Vertical Velocity(m/s)'])
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.title("Position")
    plt.plot(time, position)
    plt.legend(['Vertical position(m)'])
    plt.grid()

    plt.subplots_adjust(0.09, 0.05, 0.97, 0.93, 0.2, 0.24)
    plt.show()