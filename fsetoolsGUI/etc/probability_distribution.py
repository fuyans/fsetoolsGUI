import numpy as np
import scipy.optimize as optimize
import scipy.stats as stats


def general_purpose_dist_func(x0, arg):
    # Extract variables that are used in the method to be optimised
    dist_name = arg[0]
    *_, mean, sd = arg[1:]

    # Work out loss
    dist_func = getattr(stats, dist_name)(*x0)
    loss = (dist_func.mean() - mean) ** 2 + (dist_func.std() - sd) ** 2

    return loss


def solve_loc_scale(dist_name, *args, **kwargs):
    if dist_name == 'lognorm':
        if len(args) == 2:
            s = args[-1]
            args = [s] + list(args)
        if 'bounds' in kwargs:
            bounds = kwargs['bounds']
        else:
            bounds = [[1e-5, 1e10], [0, 0], [1e-5, 1e10]]

    else:
        if 'bounds' in kwargs:
            bounds = kwargs['bounds']
        else:
            bounds = [[-1e10, 1e10], [1e-5, 1e10]]

    optimized_result = optimize.minimize(general_purpose_dist_func, x0=args, args=[dist_name] + list(args),
                                         bounds=bounds)

    return optimized_result


def solve_loc_scale_stats(optimize_result):
    if optimize_result.success:
        fitted_params = optimize_result.x
        result_dist = getattr(stats, dist_name)(*optimize_result.x)
        mean_, var_, skew_, kurt_ = result_dist.stats(moments='mvsk')
        std_, median_ = result_dist.std(), result_dist.median()

        print(f'Resolved *args: {[round(i, 3) for i in fitted_params]}')
        print(f'Resolved stats: mean   {mean_:<10.4g}')
        print(f'                std    {std_:<10.4g}')
        print(f'                median {median_:<10.4g}')
        print(f'                var    {var_:<10.4g}')
        print(f'                skew   {skew_:<10.4g}')
        print(f'                kurt   {kurt_:<10.4g}')
    else:
        raise ValueError(optimize_result.message)


def _test_gumbel_r():
    dist_name = 'gumbel_r'
    mean = 420
    sd = 126
    result = solve_loc_scale(dist_name, mean, sd)

    # result_dist = getattr(stats, dist_name)(*result.x)
    # for i in zip(np.linspace(0, 1, 5), result_dist.cdf(np.linspace(0, 1, 5))):
    #     print('{:<10} {:<10}'.format(*i))

    # sns.lineplot(np.linspace(0,1,100), result_dist.pdf(np.linspace(0,1,100)))
    # sns.lineplot(np.linspace(0, 1, 100), result_dist.cdf(np.linspace(0, 1, 100)))


def _test_lognorm():
    dist_name = 'lognorm'
    s = 0.2
    mean = 0.2
    sd = 0.2

    result = solve_loc_scale(dist_name, s, mean, sd, bounds=[[0.00001, np.inf], [0, 0], [0.00001, np.inf]])
    print(stats.lognorm.cdf(0.2, *result.x))

    # result_dist = getattr(stats, dist_name)(*result.x)
    # for i in zip(np.linspace(0, 1, 5), result_dist.cdf(np.linspace(0, 1, 5))):
    #     print('{:<10} {:<10}'.format(*i))

    # sns.lineplot(np.linspace(0,1,100), result_dist.pdf(np.linspace(0,1,100)))
    # sns.lineplot(np.linspace(0, 1, 100), result_dist.cdf(np.linspace(0, 1, 100)))


def _test_norm():
    dist_name = 'norm'
    mean = 5
    sd = 1.2

    result = solve_loc_scale(dist_name, mean, sd)

    print(stats.norm.cdf(5, *result.x))

    # result_dist = getattr(stats, dist_name)(*result.x)
    # for i in zip(np.linspace(0, 1, 5), result_dist.cdf(np.linspace(0, 1, 5))):
    #     print('{:<10} {:<10}'.format(*i))

    # sns.lineplot(np.linspace(0,1,100), result_dist.pdf(np.linspace(0,1,100)))
    # sns.lineplot(np.linspace(0, 1, 100), result_dist.cdf(np.linspace(0, 1, 100)))


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    dist_name = 'lognorm'

    s = 0.2
    mean = 0.2
    sd = 0.2

    result_ = solve_loc_scale(dist_name, s, mean, sd, bounds=[[0.00001, np.inf], [0, 0], [0.00001, np.inf]])

    solve_loc_scale_stats(result_)

    dist_ = stats.lognorm(*result_.x)

    print(dist_.ppf(0.2))

    _test_gumbel_r()
    _test_lognorm()
    _test_norm()

    plt.plot(np.linspace(0, 1, 1000), dist_.cdf(np.linspace(0, 1, 1000)))

    plt.show()
