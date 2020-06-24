from fsetools.lib.fse_thermal_radiation_3d import heat_flux_to_temperature


def __calculate_heat_flux(heat_flux, t1):
    return heat_flux_to_temperature(heat_flux, t1)


if __name__ == '__main__':
    print(__calculate_heat_flux(125 * 1e3, 293.15))
