import numpy as np

k = 3.0
k_prime = 5.0
mu = 2.0
nu = 1.0
chi = (k**2 - 1.0) / (k**2 + 1.0)
chi_prime = (k_prime ** (1.0 / mu) - 1.0) / (k_prime ** (1.0 / mu) + 1.0)


def contact_distance_cartesian(u1_hat, u2_hat, r_hat, sigma0=1.0):
    r_u1 = r_hat.dot(u1_hat)
    r_u2 = r_hat.dot(u2_hat)
    u1_u2 = u1_hat.dot(u2_hat)
    return (
        sigma0
        * (
            1.0
            - (chi / 2.0)
            * (
                ((r_u1 + r_u2) ** 2 / (1.0 + chi * u1_u2))
                + ((r_u1 - r_u2) ** 2 / (1.0 - chi * u1_u2))
            )
        )
        ** -0.5
    )


def well_depth_cartesian(u1_hat, u2_hat, r_hat, epsilon0=1.0):
    r_u1 = r_hat.dot(u1_hat)
    r_u2 = r_hat.dot(u2_hat)
    u1_u2 = u1_hat.dot(u2_hat)
    return (
        epsilon0
        * (1.0 - chi_prime**2 * u1_u2) ** (-nu / 2.0)
        * (
            1.0
            - (chi_prime / 2.0)
            * (
                ((r_u1 + r_u2) ** 2 / (1.0 + chi_prime * u1_u2))
                + ((r_u1 - r_u2) ** 2 / (1.0 - chi_prime * u1_u2))
            )
        )
        ** mu
    )


# General formulation in cartesian coordinates
def gay_berne_general_cartesian(r_v, u1_hat, u2_hat, sigma0=1.0):
    r = np.linalg.norm(r_v)
    r_hat = r_v / r
    r_star = sigma0 / (r - contact_distance_cartesian(u1_hat, u2_hat, r_hat) + sigma0)
    return 4.0 * well_depth_cartesian(u1_hat, u2_hat, r_hat) * (r_star**12 - r_star**6)


def contact_distance_polar(theta, delta_phi, sigma0=1.0):
    r_u1 = np.cos(theta)
    r_u2 = np.cos(theta - delta_phi)
    u1_u2 = np.cos(delta_phi)

    return sigma0 / np.sqrt(
        1.0
        - (chi / 2.0)
        * (
            (r_u1 + r_u2) ** 2 / (1.0 + chi * u1_u2)
            + (r_u1 - r_u2) ** 2 / (1.0 - chi * u1_u2)
        )
    )


def well_depth_polar(theta, delta_phi, epsilon0=1.0):
    r_u1 = np.cos(theta)
    r_u2 = np.cos(theta - delta_phi)
    u1_u2 = np.cos(delta_phi)

    eps1 = (1.0 - chi**2 * u1_u2**2) ** (-nu / 2.0)

    eps2 = (
        1.0
        - (chi_prime / 2.0)
        * (
            (r_u1 + r_u2) ** 2 / (1.0 + chi_prime * u1_u2)
            + (r_u1 - r_u2) ** 2 / (1.0 - chi_prime * u1_u2)
        )
    ) ** mu

    return epsilon0 * eps1 * eps2


def gay_berne_general_polar(r, theta, delta_phi, sigma0=1.0, epsilon_0=1.0):
    sigma = contact_distance_polar(theta, delta_phi, sigma0)
    epsilon = well_depth_polar(theta, delta_phi)
    rho = sigma0 / (r - sigma + sigma0)
    return 4.0 * epsilon_0 * epsilon * (rho**12 - rho**6)


# Little helper for angle computation
def angle_between(a, b):
    cos_angle = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return np.arccos(cos_angle)


def main():
    p1 = np.array((0.0, 0.0, 0.0))  # Absolute position of the first particle
    p2 = np.array((2.0, 0.0, 0.0))  # Absolute position of the second particle
    u1 = np.array((1.0, 0.0, 0.0))  # Unit orientation vector of the first particle
    u2 = np.array((0.0, 1.0, 0.0))  # Unit orientation vector of the second particle

    delta_p = (
        p2 - p1
    )  # Relative position of the second particle w.r.t. the first particle

    px = np.array((1.0, 0.0, 0.0))
    theta = angle_between(px, delta_p)

    phi1 = angle_between(px, u1)
    phi2 = angle_between(px, u2)
    delta_phi = phi2 - phi1

    r = delta_p
    r_hat = np.linalg.norm(r)

    print(
        gay_berne_general_cartesian(
            r,
            u1,
            u2,
        )
    )

    print(
        gay_berne_general_polar(
            r_hat,
            theta,
            delta_phi,
        )
    )

    print(contact_distance_polar(0.0, 0.0))
    print(contact_distance_polar(np.pi / 2.0, 0.0))
    print(contact_distance_polar(np.pi, 0.0))
    print(contact_distance_polar(np.pi * 3.0 / 2.0, 0.0))


if __name__ == "__main__":
    main()
