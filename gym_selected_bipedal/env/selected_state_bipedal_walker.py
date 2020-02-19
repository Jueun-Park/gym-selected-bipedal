import gym
import numpy as np
from gym.envs.box2d.bipedal_walker import BipedalWalkerHardcore, TERRAIN_HEIGHT, TERRAIN_STARTPAD, TERRAIN_LENGTH, TERRAIN_STEP, TERRAIN_GRASS, SCALE

GRASS, STUMP, STAIRS, PIT, _STATES_ = range(5)


class SelectedStateBipedalWalker(BipedalWalkerHardcore):
    def __init__(self, selected_state):
        self.selected_state = selected_state
        super().__init__()

    def _generate_terrain(self, hardcore):
        state = GRASS
        velocity = 0.0
        y = TERRAIN_HEIGHT
        counter = TERRAIN_STARTPAD
        oneshot = False
        self.terrain = []
        self.terrain_x = []
        self.terrain_y = []
        for i in range(TERRAIN_LENGTH):
            x = i*TERRAIN_STEP
            self.terrain_x.append(x)

            if state == GRASS and not oneshot:
                velocity = 0.8*velocity + 0.01*np.sign(TERRAIN_HEIGHT - y)
                if i > TERRAIN_STARTPAD:
                    velocity += self.np_random.uniform(-1, 1)/SCALE  # 1
                y += velocity

            elif state == PIT and oneshot:
                counter = self.np_random.randint(3, 5)
                poly = [
                    (x,              y),
                    (x+TERRAIN_STEP, y),
                    (x+TERRAIN_STEP, y-4*TERRAIN_STEP),
                    (x,              y-4*TERRAIN_STEP),
                ]
                self.fd_polygon.shape.vertices = poly
                t = self.world.CreateStaticBody(
                    fixtures=self.fd_polygon)
                t.color1, t.color2 = (1, 1, 1), (0.6, 0.6, 0.6)
                self.terrain.append(t)

                self.fd_polygon.shape.vertices = [
                    (p[0]+TERRAIN_STEP*counter, p[1]) for p in poly]
                t = self.world.CreateStaticBody(
                    fixtures=self.fd_polygon)
                t.color1, t.color2 = (1, 1, 1), (0.6, 0.6, 0.6)
                self.terrain.append(t)
                counter += 2
                original_y = y

            elif state == PIT and not oneshot:
                y = original_y
                if counter > 1:
                    y -= 4*TERRAIN_STEP

            elif state == STUMP and oneshot:
                counter = self.np_random.randint(1, 3)
                poly = [
                    (x,                      y),
                    (x+counter*TERRAIN_STEP, y),
                    (x+counter*TERRAIN_STEP, y+counter*TERRAIN_STEP),
                    (x,                      y+counter*TERRAIN_STEP),
                ]
                self.fd_polygon.shape.vertices = poly
                t = self.world.CreateStaticBody(
                    fixtures=self.fd_polygon)
                t.color1, t.color2 = (1, 1, 1), (0.6, 0.6, 0.6)
                self.terrain.append(t)

            elif state == STAIRS and oneshot:
                stair_height = +1 if self.np_random.rand() > 0.5 else -1
                stair_width = self.np_random.randint(4, 5)
                stair_steps = self.np_random.randint(3, 5)
                original_y = y
                for s in range(stair_steps):
                    poly = [
                        (x+(s*stair_width)*TERRAIN_STEP,
                         y+(s*stair_height)*TERRAIN_STEP),
                        (x+((1+s)*stair_width)*TERRAIN_STEP,
                         y+(s*stair_height)*TERRAIN_STEP),
                        (x+((1+s)*stair_width)*TERRAIN_STEP,
                         y+(-1+s*stair_height)*TERRAIN_STEP),
                        (x+(s*stair_width)*TERRAIN_STEP, y +
                         (-1+s*stair_height)*TERRAIN_STEP),
                    ]
                    self.fd_polygon.shape.vertices = poly
                    t = self.world.CreateStaticBody(
                        fixtures=self.fd_polygon)
                    t.color1, t.color2 = (1, 1, 1), (0.6, 0.6, 0.6)
                    self.terrain.append(t)
                counter = stair_steps*stair_width

            elif state == STAIRS and not oneshot:
                s = stair_steps*stair_width - counter - stair_height
                n = s/stair_width
                y = original_y + (n*stair_height)*TERRAIN_STEP

            oneshot = False
            self.terrain_y.append(y)
            counter -= 1
            if counter == 0:
                counter = self.np_random.randint(
                    TERRAIN_GRASS/2, TERRAIN_GRASS)
                if state == GRASS and hardcore:
                    state = self.selected_state
                    oneshot = True
                else:
                    state = GRASS
                    oneshot = True

        self.terrain_poly = []
        for i in range(TERRAIN_LENGTH-1):
            poly = [
                (self.terrain_x[i],   self.terrain_y[i]),
                (self.terrain_x[i+1], self.terrain_y[i+1])
            ]
            self.fd_edge.shape.vertices = poly
            t = self.world.CreateStaticBody(
                fixtures=self.fd_edge)
            color = (0.3, 1.0 if i % 2 == 0 else 0.8, 0.3)
            t.color1 = color
            t.color2 = color
            self.terrain.append(t)
            color = (0.4, 0.6, 0.3)
            poly += [(poly[1][0], 0), (poly[0][0], 0)]
            self.terrain_poly.append((poly, color))
        self.terrain.reverse()


if __name__=="__main__":
    # Heurisic: suboptimal, have no notion of balance.
    def test(env):
        env.reset()
        steps = 0
        total_reward = 0
        a = np.array([0.0, 0.0, 0.0, 0.0])
        STAY_ON_ONE_LEG, PUT_OTHER_DOWN, PUSH_OFF = 1,2,3
        SPEED = 0.29  # Will fall forward on higher speed
        state = STAY_ON_ONE_LEG
        moving_leg = 0
        supporting_leg = 1 - moving_leg
        SUPPORT_KNEE_ANGLE = +0.1
        supporting_knee_angle = SUPPORT_KNEE_ANGLE
        while True:
            s, r, done, info = env.step(a)
            total_reward += r
            if steps % 20 == 0 or done:
                print("\naction " + str(["{:+0.2f}".format(x) for x in a]))
                print("step {} total_reward {:+0.2f}".format(steps, total_reward))
                print("hull " + str(["{:+0.2f}".format(x) for x in s[0:4] ]))
                print("leg0 " + str(["{:+0.2f}".format(x) for x in s[4:9] ]))
                print("leg1 " + str(["{:+0.2f}".format(x) for x in s[9:14]]))
            steps += 1

            contact0 = s[8]
            contact1 = s[13]
            moving_s_base = 4 + 5*moving_leg
            supporting_s_base = 4 + 5*supporting_leg

            hip_targ  = [None,None]   # -0.8 .. +1.1
            knee_targ = [None,None]   # -0.6 .. +0.9
            hip_todo  = [0.0, 0.0]
            knee_todo = [0.0, 0.0]

            if state==STAY_ON_ONE_LEG:
                hip_targ[moving_leg]  = 1.1
                knee_targ[moving_leg] = -0.6
                supporting_knee_angle += 0.03
                if s[2] > SPEED: supporting_knee_angle += 0.03
                supporting_knee_angle = min( supporting_knee_angle, SUPPORT_KNEE_ANGLE )
                knee_targ[supporting_leg] = supporting_knee_angle
                if s[supporting_s_base+0] < 0.10: # supporting leg is behind
                    state = PUT_OTHER_DOWN
            if state==PUT_OTHER_DOWN:
                hip_targ[moving_leg]  = +0.1
                knee_targ[moving_leg] = SUPPORT_KNEE_ANGLE
                knee_targ[supporting_leg] = supporting_knee_angle
                if s[moving_s_base+4]:
                    state = PUSH_OFF
                    supporting_knee_angle = min( s[moving_s_base+2], SUPPORT_KNEE_ANGLE )
            if state==PUSH_OFF:
                knee_targ[moving_leg] = supporting_knee_angle
                knee_targ[supporting_leg] = +1.0
                if s[supporting_s_base+2] > 0.88 or s[2] > 1.2*SPEED:
                    state = STAY_ON_ONE_LEG
                    moving_leg = 1 - moving_leg
                    supporting_leg = 1 - moving_leg

            if hip_targ[0]: hip_todo[0] = 0.9*(hip_targ[0] - s[4]) - 0.25*s[5]
            if hip_targ[1]: hip_todo[1] = 0.9*(hip_targ[1] - s[9]) - 0.25*s[10]
            if knee_targ[0]: knee_todo[0] = 4.0*(knee_targ[0] - s[6])  - 0.25*s[7]
            if knee_targ[1]: knee_todo[1] = 4.0*(knee_targ[1] - s[11]) - 0.25*s[12]

            hip_todo[0] -= 0.9*(0-s[0]) - 1.5*s[1] # PID to keep head strait
            hip_todo[1] -= 0.9*(0-s[0]) - 1.5*s[1]
            knee_todo[0] -= 15.0*s[3]  # vertical speed, to damp oscillations
            knee_todo[1] -= 15.0*s[3]

            a[0] = hip_todo[0]
            a[1] = knee_todo[0]
            a[2] = hip_todo[1]
            a[3] = knee_todo[1]
            a = np.clip(0.5*a, -1.0, 1.0)

            env.render()
            if done:
                env.close()
                break

    for state in range(_STATES_):
        env = SelectedStateBipedalWalker(selected_state=state)
        test(env)
