import numpy as np
import scipy.optimize as optimize
import scipy.stats as stats

from fsetoolsGUI import logger


def general_purpose_dist_func(x0, arg):
    # Extract variables that are used in the method to be optimised
    dist_name = arg[0]
    *_, mean, sd = arg[1:]

    # Work out loss
    dist_func = getattr(stats, dist_name)(*x0)
    loss = (dist_func.mean() - mean) ** 2 + (dist_func.std() - sd) ** 2

    logger.debug(f'{dist_func.mean()}, {mean}, {dist_func.std()}, {sd}')

    return loss


def solve_dist_for_mean_std(dist_name, *args, **kwargs):
    if dist_name == 'lognorm':
        # for lognorm distribution, the s, loc and scale parameters are calculated deterministically

        def lognorm_(mean: float, sd: float, **_):
            cov = sd / mean
            sigma_ln = np.sqrt(np.log(1 + cov ** 2))
            miu_ln = np.log(mean) - 1 / 2 * sigma_ln ** 2
            s = sigma_ln
            loc = 0
            scale = np.exp(miu_ln)
            return dict(s=s, loc=loc, scale=scale)

        if len(args) == 2:
            args = lognorm_(*args)
            args = [args['s'], args['loc'], args['scale']]
        else:
            raise NotImplementedError()

        # if 'bounds' in kwargs:
        #     bounds = kwargs['bounds']
        # else:
        #     bounds = [[1e-5, 1e10], [0, 1e10], [1e-5, 1e10]]

        class FakeDistFit:
            x = args

        optimized_result = FakeDistFit

    else:
        if 'bounds' in kwargs:
            bounds = kwargs['bounds']
        else:
            bounds = [[-1e10, 1e10], [1e-5, 1e10]]

        optimized_result = optimize.minimize(
            general_purpose_dist_func,
            x0=args,
            args=[dist_name] + list(args),
            bounds=bounds
        )

    return optimized_result


def solve_loc_scale_stats(optimize_result, dist_name):
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


def test_gumbel_r():
    dist_name = 'gumbel_r'
    mean = 420
    sd = 126
    result = solve_dist_for_mean_std(dist_name, mean, sd)

    dist_fitted = getattr(stats, dist_name)(*result.x)

    assert abs(mean - dist_fitted.mean()) < 1e-5
    assert abs(sd - dist_fitted.std()) < 1e-5


def test_lognorm():
    dist_name = 'lognorm'
    s = 0.2
    mean = 0.2
    sd = 0.2

    result = solve_dist_for_mean_std(dist_name, s, mean, sd, bounds=[[0.00001, np.inf], [0, 0], [0.00001, np.inf]])

    dist_fitted = getattr(stats, dist_name)(*result.x)

    assert abs(mean - dist_fitted.mean()) < 1e-5
    assert abs(sd - dist_fitted.std()) < 1e-5


def test_norm():
    dist_name = 'norm'
    mean = 5
    sd = 1.2

    result = solve_dist_for_mean_std(dist_name, mean, sd)

    dist_fitted = getattr(stats, dist_name)(*result.x)

    assert abs(mean - dist_fitted.mean()) < 1e-5
    assert abs(sd - dist_fitted.std()) < 1e-5


if __name__ == '__main__':
    # import matplotlib.pyplot as plt
    #
    # dist_name = 'lognorm'
    #
    # s = 0.2
    # mean = 0.2
    # sd = 0.2
    #
    # result_ = solve_loc_scale(dist_name, s, mean, sd, bounds=[[0.00001, np.inf], [0, 0], [0.00001, np.inf]])
    #
    # solve_loc_scale_stats(result_)
    #
    # dist_ = stats.lognorm(*result_.x)
    #
    # print(dist_.ppf(0.2))
    #
    # test_gumbel_r()
    # test_lognorm()
    # test_norm()
    #
    # plt.plot(np.linspace(0, 1, 1000), dist_.cdf(np.linspace(0, 1, 1000)))
    #
    # plt.show()

    pass
