#!/usr/bin/python

import numpy as np

class Body():
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = np.asarray(position)
        self.velocity = np.asarray(velocity)

class Integrator():
    def __init__(self, timestep=0.01):
        self.timestep = timestep

        f = np.power(2.0, 1/3)
        w1 = 1/(2 - f)
        w0 = -f*w1

        self.c = [w1/2, (w0 + w1)/2, (w0 + w1)/2, w1/2]
        self.d = [w1, w0, w1]

    def calc_acceleration(self, bodies, body):
        acc = 0.0*body.position

        for b in bodies:
            if b is not body:
                # distance from b to body
                dist = np.sqrt((b.position[0] - body.position[0])**2 +
                               (b.position[1] - body.position[1])**2 +
                               (b.position[2] - body.position[2])**2)

                acc = acc + b.mass*(b.position - body.position)/dist**3

        return acc

    def do_timestep(self, bodies):
        ## # Kick
        ## for body in bodies:
        ##     a = self.calc_acceleration(bodies, body)
        ##     body.velocity = body.velocity + 0.5*self.timestep*a

        ## # Drift
        ## for body in bodies:
        ##     body.position = body.position + self.timestep*body.velocity

        ## # Kick
        ## for body in bodies:
        ##     a = self.calc_acceleration(bodies, body)
        ##     body.velocity = body.velocity + 0.5*self.timestep*a

        dt = self.timestep

        # Drift
        for body in bodies:
            body.position = body.position + self.c[0]*dt*body.velocity

        # Kick
        for body in bodies:
            a = self.calc_acceleration(bodies, body)
            body.velocity = body.velocity + self.d[0]*dt*a

        # Drift
        for body in bodies:
            body.position = body.position + self.c[1]*dt*body.velocity

        # Kick
        for body in bodies:
            a = self.calc_acceleration(bodies, body)
            body.velocity = body.velocity + self.d[1]*dt*a

        # Drift
        for body in bodies:
            body.position = body.position + self.c[2]*dt*body.velocity

        # Kick
        for body in bodies:
            a = self.calc_acceleration(bodies, body)
            body.velocity = body.velocity + self.d[2]*dt*a

        # Drift
        for body in bodies:
            body.position = body.position + self.c[3]*dt*body.velocity

class Orbit():
    def __init__(self,
                 semi_major=1,
                 eccentricity=0,
                 mass1=1, mass2=0,
                 n_sample=100,
                 substeps=10):
        mtot = mass1 + mass2
        a = semi_major*(mtot/mass1)**1
        e = eccentricity

        p = a*(1 - e*e)

        r = a*(1 - e)
        v = np.sqrt(mtot/p)*(1 + e)

        self.star_pos = [np.asarray([-mass2*r/mtot, 0.0, 0.0])]
        self.star_vel = [np.asarray([0.0, -mass2*v/mtot, 0.0])]

        self.plan_pos = [np.asarray([mass1*r/mtot, 0.0, 0.0])]
        self.plan_vel = [np.asarray([0.0, mass1*v/mtot, 0.0])]

        self.star = Body(mass1, self.star_pos[0], self.star_vel[0])
        self.plan = Body(mass2, self.plan_pos[0], self.plan_vel[0])

        period = 2.0*np.pi*np.sqrt(a*a*a/mtot)

        intg = Integrator(timestep=period/(substeps*n_sample))

        self.time = np.linspace(0, period, n_sample)

        for i in range(1, n_sample):
            for j in range(0, substeps):
                intg.do_timestep([self.star, self.plan])

            self.star_pos.append(self.star.position)
            self.star_vel.append(self.star.velocity)

            self.plan_pos.append(self.plan.position)
            self.plan_vel.append(self.plan.velocity)